#!/usr/bin/env python3
"""
ERROR RECOVERY SYSTEM
Automatic retry, fallback, and recovery from failures.
Resolves foundational issue: no_error_recovery
"""

import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Callable, Any, Optional, List
from functools import wraps

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
ERROR_LOG = CONSCIOUSNESS / "error_recovery_log.json"


class RecoveryStrategy:
    """Base recovery strategy."""

    def __init__(self, name: str):
        self.name = name

    def execute(self, error: Exception, context: dict) -> Any:
        raise NotImplementedError


class RetryStrategy(RecoveryStrategy):
    """Retry with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        super().__init__("retry")
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, func: Callable, args: tuple, kwargs: dict) -> Any:
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                delay = self.base_delay * (2 ** attempt)
                print(f"  Retry {attempt + 1}/{self.max_retries} in {delay}s: {e}")
                time.sleep(delay)

        raise last_error


class FallbackStrategy(RecoveryStrategy):
    """Fall back to alternative function."""

    def __init__(self, fallback_fn: Callable):
        super().__init__("fallback")
        self.fallback_fn = fallback_fn

    def execute(self, error: Exception, context: dict) -> Any:
        return self.fallback_fn(context)


class CacheStrategy(RecoveryStrategy):
    """Return cached result on failure."""

    def __init__(self, cache_path: Path = None):
        super().__init__("cache")
        self.cache_path = cache_path or CONSCIOUSNESS / "recovery_cache.json"
        self._load_cache()

    def _load_cache(self):
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _save_cache(self):
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def store(self, key: str, value: Any):
        self.cache[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_cache()

    def execute(self, error: Exception, context: dict) -> Any:
        key = context.get("cache_key", "default")
        if key in self.cache:
            print(f"  Using cached result for {key}")
            return self.cache[key]["value"]
        raise error


class ErrorRecoverySystem:
    """Central error recovery coordinator."""

    def __init__(self):
        self.error_log = []
        self.recovery_stats = {
            "total_errors": 0,
            "recovered": 0,
            "failed": 0
        }
        self.cache_strategy = CacheStrategy()
        self._load_log()

    def _load_log(self):
        if ERROR_LOG.exists():
            with open(ERROR_LOG) as f:
                data = json.load(f)
                self.error_log = data.get("log", [])
                self.recovery_stats = data.get("stats", self.recovery_stats)

    def _save_log(self):
        with open(ERROR_LOG, 'w') as f:
            json.dump({
                "log": self.error_log[-100:],
                "stats": self.recovery_stats,
                "updated": datetime.now().isoformat()
            }, f, indent=2)

    def log_error(self, error: Exception, context: dict, recovered: bool, strategy: str):
        """Log error and recovery attempt."""
        entry = {
            "error": str(error),
            "type": type(error).__name__,
            "context": str(context)[:200],
            "recovered": recovered,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat()
        }
        self.error_log.append(entry)

        self.recovery_stats["total_errors"] += 1
        if recovered:
            self.recovery_stats["recovered"] += 1
        else:
            self.recovery_stats["failed"] += 1

        self._save_log()

    def with_recovery(self, max_retries: int = 3, fallback: Callable = None,
                     cache_key: str = None):
        """Decorator for automatic error recovery."""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                context = {
                    "function": func.__name__,
                    "args": str(args)[:100],
                    "cache_key": cache_key or func.__name__
                }

                # Try with retry
                retry = RetryStrategy(max_retries)
                try:
                    result = retry.execute(func, args, kwargs)

                    # Cache successful result
                    if cache_key:
                        self.cache_strategy.store(cache_key, result)

                    return result

                except Exception as e:
                    # Try fallback
                    if fallback:
                        try:
                            result = fallback(context)
                            self.log_error(e, context, True, "fallback")
                            return result
                        except Exception:
                            pass

                    # Try cache
                    try:
                        result = self.cache_strategy.execute(e, context)
                        self.log_error(e, context, True, "cache")
                        return result
                    except Exception:
                        pass

                    # All recovery failed
                    self.log_error(e, context, False, "none")
                    raise

            return wrapper
        return decorator

    def execute_with_recovery(self, func: Callable, *args,
                             max_retries: int = 3,
                             fallback: Callable = None,
                             cache_key: str = None,
                             **kwargs) -> Any:
        """Execute function with recovery strategies."""

        context = {
            "function": func.__name__,
            "cache_key": cache_key or func.__name__
        }

        # Strategy 1: Retry with backoff
        retry = RetryStrategy(max_retries)
        try:
            result = retry.execute(func, args, kwargs)

            # Cache on success
            if cache_key:
                self.cache_strategy.store(cache_key, result)

            return result

        except Exception as e:
            print(f"Primary execution failed: {e}")

            # Strategy 2: Fallback function
            if fallback:
                try:
                    print("  Trying fallback...")
                    result = fallback(context)
                    self.log_error(e, context, True, "fallback")
                    return result
                except Exception as fe:
                    print(f"  Fallback failed: {fe}")

            # Strategy 3: Cache
            try:
                result = self.cache_strategy.execute(e, context)
                self.log_error(e, context, True, "cache")
                return result
            except Exception:
                pass

            # All failed
            self.log_error(e, context, False, "none")
            raise

    def get_status(self) -> dict:
        """Get recovery system status."""
        recovery_rate = 0
        if self.recovery_stats["total_errors"] > 0:
            recovery_rate = (self.recovery_stats["recovered"] /
                           self.recovery_stats["total_errors"]) * 100

        return {
            "total_errors": self.recovery_stats["total_errors"],
            "recovered": self.recovery_stats["recovered"],
            "failed": self.recovery_stats["failed"],
            "recovery_rate": f"{recovery_rate:.1f}%",
            "recent_errors": [
                {
                    "type": e["type"],
                    "recovered": e["recovered"],
                    "strategy": e["strategy"]
                }
                for e in self.error_log[-5:]
            ]
        }


# Global instance
recovery_system = ErrorRecoverySystem()


def recoverable(max_retries: int = 3, fallback: Callable = None, cache_key: str = None):
    """Decorator to make function recoverable."""
    return recovery_system.with_recovery(max_retries, fallback, cache_key)


# === COMMON RECOVERY FUNCTIONS ===

def safe_json_load(file_path: Path, default: Any = None) -> Any:
    """Safely load JSON with recovery."""
    def fallback(ctx):
        return default

    return recovery_system.execute_with_recovery(
        lambda: json.load(open(file_path)),
        max_retries=1,
        fallback=fallback,
        cache_key=str(file_path)
    )


def safe_file_write(file_path: Path, content: str) -> bool:
    """Safely write file with recovery."""
    def write():
        # Backup first
        if file_path.exists():
            backup = file_path.with_suffix(file_path.suffix + '.bak')
            import shutil
            shutil.copy(file_path, backup)

        with open(file_path, 'w') as f:
            f.write(content)
        return True

    return recovery_system.execute_with_recovery(
        write,
        max_retries=3
    )


def safe_api_call(url: str, method: str = "GET", **kwargs) -> dict:
    """Safely make API call with recovery."""
    import urllib.request
    import urllib.error

    def call():
        req = urllib.request.Request(url, method=method)
        for key, value in kwargs.get("headers", {}).items():
            req.add_header(key, value)

        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read())

    def fallback(ctx):
        return {"error": "API unavailable", "cached": True}

    return recovery_system.execute_with_recovery(
        call,
        max_retries=3,
        fallback=fallback,
        cache_key=url
    )


def demo():
    """Demonstrate error recovery."""
    print("=" * 60)
    print("ERROR RECOVERY SYSTEM DEMO")
    print("=" * 60)

    recovery = ErrorRecoverySystem()

    # Test 1: Retry strategy
    print("\n1. Testing retry strategy...")

    attempt = [0]
    def flaky_function():
        attempt[0] += 1
        if attempt[0] < 3:
            raise ConnectionError(f"Attempt {attempt[0]} failed")
        return "Success after retries"

    result = recovery.execute_with_recovery(flaky_function, max_retries=3)
    print(f"   Result: {result}")

    # Test 2: Fallback strategy
    print("\n2. Testing fallback strategy...")

    def always_fails():
        raise ValueError("Always fails")

    def fallback_fn(ctx):
        return "Fallback result"

    result = recovery.execute_with_recovery(
        always_fails,
        max_retries=1,
        fallback=fallback_fn
    )
    print(f"   Result: {result}")

    # Test 3: Cache strategy
    print("\n3. Testing cache strategy...")

    # First call succeeds and caches
    def cacheable():
        return {"data": "cached_value", "time": datetime.now().isoformat()}

    result1 = recovery.execute_with_recovery(
        cacheable,
        cache_key="test_cache"
    )
    print(f"   First call: {result1}")

    # Second call fails but returns cache
    def fails_after_cache():
        raise RuntimeError("Failed after caching")

    result2 = recovery.execute_with_recovery(
        fails_after_cache,
        max_retries=1,
        cache_key="test_cache"
    )
    print(f"   Cached result: {result2}")

    # Status
    print("\n" + "=" * 60)
    print("RECOVERY STATUS")
    print("=" * 60)

    status = recovery.get_status()
    print(f"Total errors: {status['total_errors']}")
    print(f"Recovered: {status['recovered']}")
    print(f"Failed: {status['failed']}")
    print(f"Recovery rate: {status['recovery_rate']}")


def main():
    """CLI for error recovery system."""
    import sys

    recovery = ErrorRecoverySystem()

    if len(sys.argv) < 2:
        print("Error Recovery System")
        print("=" * 40)
        print("\nCommands:")
        print("  status   - Show recovery statistics")
        print("  log      - Show recent errors")
        print("  demo     - Run demo")
        print("  clear    - Clear error log")
        return

    command = sys.argv[1]

    if command == "status":
        status = recovery.get_status()
        print(f"\nRecovery Status:")
        print(f"  Total errors: {status['total_errors']}")
        print(f"  Recovered: {status['recovered']}")
        print(f"  Failed: {status['failed']}")
        print(f"  Recovery rate: {status['recovery_rate']}")

    elif command == "log":
        for entry in recovery.error_log[-10:]:
            symbol = "✅" if entry["recovered"] else "❌"
            print(f"{symbol} [{entry['type']}] {entry['strategy']}: {entry['error'][:50]}")

    elif command == "demo":
        demo()

    elif command == "clear":
        recovery.error_log = []
        recovery.recovery_stats = {"total_errors": 0, "recovered": 0, "failed": 0}
        recovery._save_log()
        print("Error log cleared")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
