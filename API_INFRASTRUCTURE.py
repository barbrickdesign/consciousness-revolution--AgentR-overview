#!/usr/bin/env python3
"""
API INFRASTRUCTURE LAYER
Connection pooling, request validation, rate limiting.

Prevents:
- Connection exhaustion (max 10 concurrent → pooled)
- SQL injection attacks (input validation)
- DoS attacks (rate limiting)
- Invalid queries (parameter validation)
"""

import sqlite3
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from functools import wraps
from collections import defaultdict
from typing import Tuple, Optional

# ============================================================================
# CONNECTION POOL
# ============================================================================

class SQLiteConnectionPool:
    """Thread-safe connection pool for SQLite database."""

    def __init__(self, db_path: str, pool_size: int = 10, timeout: float = 5.0):
        self.db_path = db_path
        self.pool_size = pool_size
        self.timeout = timeout
        self.connections = []
        self.available = []
        self.lock = threading.Lock()

        # Initialize pool
        for i in range(pool_size):
            try:
                conn = sqlite3.connect(db_path, check_same_thread=False, timeout=timeout)
                conn.row_factory = sqlite3.Row
                self.connections.append(conn)
                self.available.append(conn)
            except Exception as e:
                print(f"[POOL] Connection {i} initialization failed: {e}")

        print(f"[POOL] Initialized {len(self.available)}/{pool_size} connections")

    def acquire(self, timeout: Optional[float] = None) -> sqlite3.Connection:
        """Get connection from pool (waits if necessary)."""
        timeout = timeout or self.timeout
        start = time.time()

        while True:
            with self.lock:
                if self.available:
                    conn = self.available.pop()
                    return conn

            if time.time() - start > timeout:
                raise TimeoutError(f"No available connections after {timeout}s")

            time.sleep(0.01)

    def release(self, conn: sqlite3.Connection):
        """Return connection to pool."""
        with self.lock:
            if conn not in self.available:
                self.available.append(conn)

    def close_all(self):
        """Close all connections."""
        with self.lock:
            for conn in self.connections:
                try:
                    conn.close()
                except:
                    pass
            self.connections.clear()
            self.available.clear()

    def get_stats(self) -> dict:
        """Get pool statistics."""
        with self.lock:
            return {
                'total_connections': len(self.connections),
                'available_connections': len(self.available),
                'in_use': len(self.connections) - len(self.available)
            }


# ============================================================================
# REQUEST VALIDATION
# ============================================================================

class RequestValidator:
    """Validate API requests for security and correctness."""

    # Whitelist valid characters in queries
    QUERY_WHITELIST = set(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ' _-.,!?:\'"%*()+/&='
    )

    # Blacklist SQL injection patterns
    INJECTION_PATTERNS = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'EXEC', 'UNION', 'SELECT',
        '--', ';', '/*', '*/', 'xp_', 'sp_'
    ]

    @staticmethod
    def validate_query(query: str, max_length: int = 1000) -> Tuple[bool, Optional[str]]:
        """Validate search query for injection attacks."""
        if not query:
            return False, "Query cannot be empty"

        if len(query) > max_length:
            return False, f"Query exceeds {max_length} characters"

        # Check for injection patterns
        query_upper = query.upper()
        for pattern in RequestValidator.INJECTION_PATTERNS:
            if pattern in query_upper:
                return False, f"Invalid pattern detected: {pattern}"

        # Check for control characters
        if any(ord(c) < 32 for c in query):
            return False, "Invalid control characters"

        return True, None

    @staticmethod
    def validate_limit(limit_str: str) -> Tuple[bool, Optional[str]]:
        """Validate LIMIT parameter."""
        try:
            limit = int(limit_str)
            if limit < 1 or limit > 1000:
                return False, "Limit must be between 1 and 1000"
            return True, None
        except ValueError:
            return False, "Limit must be an integer"

    @staticmethod
    def validate_offset(offset_str: str) -> Tuple[bool, Optional[str]]:
        """Validate OFFSET parameter."""
        try:
            offset = int(offset_str)
            if offset < 0:
                return False, "Offset must be >= 0"
            if offset > 1000000:
                return False, "Offset too large"
            return True, None
        except ValueError:
            return False, "Offset must be an integer"

    @staticmethod
    def validate_atom_id(atom_id: str) -> Tuple[bool, Optional[str]]:
        """Validate atom ID format."""
        if not atom_id:
            return False, "Atom ID required"

        if len(atom_id) > 64:
            return False, "Atom ID too long (max 64 chars)"

        # Only alphanumeric + underscore + hyphen
        if not all(c.isalnum() or c in '_-' for c in atom_id):
            return False, "Invalid atom ID format"

        return True, None

    @staticmethod
    def validate_atom_type(atom_type: str) -> Tuple[bool, Optional[str]]:
        """Validate atom type."""
        valid_types = {'concept', 'fact', 'decision', 'insight', 'pattern', 'action'}

        if atom_type not in valid_types:
            return False, f"Invalid type. Must be one of: {', '.join(valid_types)}"

        return True, None


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Rate limit API requests by client IP address."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, ip: str) -> Tuple[bool, Optional[str]]:
        """Check if request from IP is allowed."""
        with self.lock:
            now = time.time()
            cutoff = now - self.window_seconds

            # Clean old requests
            self.requests[ip] = [t for t in self.requests[ip] if t > cutoff]

            # Check limit
            if len(self.requests[ip]) >= self.max_requests:
                return False, f"Rate limit exceeded ({self.max_requests}/{self.window_seconds}s)"

            # Add request
            self.requests[ip].append(now)
            return True, None

    def get_stats(self, ip: str) -> dict:
        """Get rate limit stats for IP."""
        with self.lock:
            now = time.time()
            cutoff = now - self.window_seconds
            count = sum(1 for t in self.requests[ip] if t > cutoff)
            remaining = max(0, self.max_requests - count)
            reset_in = self.window_seconds - (now % self.window_seconds)

            return {
                'requests': count,
                'max_requests': self.max_requests,
                'remaining': remaining,
                'window_seconds': self.window_seconds,
                'reset_in': int(reset_in)
            }


# ============================================================================
# MIDDLEWARE
# ============================================================================

def require_validation(f):
    """Decorator for request validation and rate limiting."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Import here to avoid circular imports
        from flask import request

        # Get client IP
        ip = request.remote_addr or '127.0.0.1'

        # Check rate limit
        allowed, error = _rate_limiter.is_allowed(ip)
        if not allowed:
            return {
                'error': error,
                'status': 429
            }, 429

        # Get rate limit stats for response headers
        stats = _rate_limiter.get_stats(ip)

        # Call decorated function
        response = f(*args, **kwargs)

        # Add rate limit headers
        if isinstance(response, tuple) and len(response) >= 2:
            data, status = response[0], response[1]
            headers = response[2] if len(response) > 2 else {}
        else:
            data = response
            status = 200
            headers = {}

        # Add rate limit headers
        headers.update({
            'X-RateLimit-Limit': str(stats['max_requests']),
            'X-RateLimit-Remaining': str(stats['remaining']),
            'X-RateLimit-Reset': str(int(time.time()) + stats['reset_in']),
            'X-RateLimit-Window': str(stats['window_seconds'])
        })

        return data, status, headers

    return decorated_function


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

_pool = None
_rate_limiter = None


def init_api_infrastructure(app=None):
    """Initialize API infrastructure (call once at startup)."""
    global _pool, _rate_limiter

    db_path = "C:/Users/dwrek/.consciousness/cyclotron_core/atoms.db"

    # Initialize connection pool
    _pool = SQLiteConnectionPool(db_path, pool_size=10, timeout=5.0)

    # Initialize rate limiter (100 requests per 60 seconds)
    _rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

    print("\n[API] Infrastructure Initialized")
    print(f"  - Connection pool size: 10")
    print(f"  - Rate limit: 100 requests/60s")
    print(f"  - Request validation: ENABLED")
    print(f"  - Connection pooling: ENABLED\n")


def get_db_connection() -> sqlite3.Connection:
    """Get database connection from pool."""
    if _pool is None:
        raise RuntimeError("API infrastructure not initialized - call init_api_infrastructure()")
    return _pool.acquire()


def release_db_connection(conn: sqlite3.Connection):
    """Return connection to pool."""
    if _pool is None:
        return
    _pool.release(conn)


def get_pool_stats() -> dict:
    """Get connection pool statistics."""
    if _pool is None:
        return {}
    return _pool.get_stats()


def get_rate_limiter_stats(ip: str) -> dict:
    """Get rate limiter stats for IP."""
    if _rate_limiter is None:
        return {}
    return _rate_limiter.get_stats(ip)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n╔════════════════════════════════════════╗")
    print("║  API INFRASTRUCTURE TEST              ║")
    print("╚════════════════════════════════════════╝\n")

    # Test validator
    print("[TEST] Request Validation")
    validator = RequestValidator()

    tests = [
        ("consciousness revolution", True, "Valid query"),
        ("'; DROP TABLE atoms; --", False, "SQL injection attempt"),
        ("test" * 300, False, "Query too long"),
        ("valid_atom_123", True, "Valid atom ID"),
        ("atom_!@#$%", False, "Invalid atom ID"),
        ("concept", True, "Valid type"),
        ("unknown_type", False, "Invalid type"),
    ]

    for query, expected, desc in tests:
        if "atom" in desc.lower() and "type" not in desc.lower():
            valid, error = validator.validate_atom_id(query)
        elif "type" in desc.lower():
            valid, error = validator.validate_atom_type(query)
        else:
            valid, error = validator.validate_query(query)

        status = "✓ PASS" if valid == expected else "✗ FAIL"
        print(f"  {status} - {desc}")
        if error:
            print(f"         Error: {error}")

    # Test rate limiter
    print("\n[TEST] Rate Limiting")
    rate_limiter = RateLimiter(max_requests=5, window_seconds=60)

    print("  Making 7 requests from same IP...")
    for i in range(7):
        allowed, error = rate_limiter.is_allowed("192.168.1.100")
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"    Request {i+1}: {status}")
        if error:
            print(f"              {error}")

    # Test connection pool
    print("\n[TEST] Connection Pool")
    print(f"  Pool stats: {_pool.get_stats() if _pool else 'Not initialized'}")

    print("\n[TEST] Complete\n")
