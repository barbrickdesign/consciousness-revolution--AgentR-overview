#!/usr/bin/env python3
"""
PATTERN CROSS-POLLINATOR v1.0
THE STAR LOOP OPTIMIZATION ENGINE

"Every time you figure out something that works for one area,
you look back at the last 200 things you created and realize
you could have used it for those - those need to be updated now."

Lug nut star pattern - crisscross optimization for even pressure.

Usage:
    python PATTERN_CROSS_POLLINATOR.py scan          # Full pattern scan
    python PATTERN_CROSS_POLLINATOR.py gaps          # Find missing patterns
    python PATTERN_CROSS_POLLINATOR.py star          # Star loop optimization
    python PATTERN_CROSS_POLLINATOR.py report        # Generate full report
    python PATTERN_CROSS_POLLINATOR.py auto          # Auto-fix safe patterns
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# =============================================================================
# PATTERN DEFINITIONS - The DNA of good code
# =============================================================================

PATTERNS = {
    # ---------------------------------------------------------------------
    # SECURITY PATTERNS
    # ---------------------------------------------------------------------
    "cors_headers": {
        "name": "CORS Headers",
        "category": "security",
        "priority": 10,
        "signature": r"Access-Control-Allow-Origin",
        "full_pattern": """const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };""",
        "applies_to": ["*.mjs", "*.js"],
        "context": "netlify/functions",
        "description": "Proper CORS headers for API functions"
    },

    "options_preflight": {
        "name": "OPTIONS Preflight Handler",
        "category": "security",
        "priority": 10,
        "signature": r"httpMethod\s*===?\s*['\"]OPTIONS['\"]",
        "full_pattern": """if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 204, headers };
    }""",
        "applies_to": ["*.mjs"],
        "context": "netlify/functions",
        "description": "Handle CORS preflight requests"
    },

    "input_validation": {
        "name": "Input Validation",
        "category": "security",
        "priority": 9,
        "signature": r"if\s*\(\s*!.*\|\|.*\)",
        "full_pattern": "if (!field1 || !field2) { return error; }",
        "applies_to": ["*.mjs", "*.js"],
        "context": "netlify/functions",
        "description": "Validate required inputs before processing"
    },

    "try_catch_handler": {
        "name": "Try-Catch Error Handler",
        "category": "security",
        "priority": 8,
        "signature": r"try\s*\{[\s\S]*?\}\s*catch\s*\(",
        "applies_to": ["*.mjs", "*.js"],
        "description": "Wrap operations in try-catch"
    },

    "no_console_secrets": {
        "name": "No Console Logging Secrets",
        "category": "security",
        "priority": 10,
        "anti_pattern": r"console\.(log|info|debug)\s*\([^)]*password",
        "description": "Never log passwords or secrets"
    },

    # ---------------------------------------------------------------------
    # UI/UX PATTERNS
    # ---------------------------------------------------------------------
    "loading_state": {
        "name": "Loading State",
        "category": "ux",
        "priority": 7,
        "signature": r"loading|Loading|isLoading|setLoading",
        "full_pattern": """<div id="loadingState" class="loading-state">
        <p>Loading...</p>
    </div>""",
        "applies_to": ["*.html"],
        "description": "Show loading state while fetching data"
    },

    "error_display": {
        "name": "Error Display",
        "category": "ux",
        "priority": 7,
        "signature": r"error-message|errorMessage|showError",
        "applies_to": ["*.html", "*.js"],
        "description": "Display errors to users clearly"
    },

    "hover_transform": {
        "name": "Hover Transform Effect",
        "category": "ux",
        "priority": 5,
        "signature": r":hover\s*\{[^}]*transform:\s*translateY",
        "full_pattern": """:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }""",
        "applies_to": ["*.html", "*.css"],
        "description": "Subtle lift effect on hover for clickable elements"
    },

    "card_component": {
        "name": "Card Component Pattern",
        "category": "ux",
        "priority": 6,
        "signature": r"\.[\w-]*card\s*\{[^}]*background:\s*rgba",
        "full_pattern": """.card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s ease;
        }""",
        "applies_to": ["*.html", "*.css"],
        "description": "Consistent card styling"
    },

    "responsive_grid": {
        "name": "Responsive Grid",
        "category": "ux",
        "priority": 6,
        "signature": r"grid-template-columns:\s*repeat\(auto-fit",
        "full_pattern": """display: grid;
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
gap: 20px;""",
        "applies_to": ["*.html", "*.css"],
        "description": "Auto-responsive grid layout"
    },

    "mobile_responsive": {
        "name": "Mobile Responsive",
        "category": "ux",
        "priority": 8,
        "signature": r"@media\s*\(\s*max-width:\s*600px",
        "applies_to": ["*.html", "*.css"],
        "description": "Mobile-first responsive breakpoints"
    },

    "gradient_text": {
        "name": "Gradient Text Effect",
        "category": "ux",
        "priority": 4,
        "signature": r"background:\s*linear-gradient[^;]+;[^}]*-webkit-background-clip:\s*text",
        "applies_to": ["*.html", "*.css"],
        "description": "Beautiful gradient text for headers"
    },

    # ---------------------------------------------------------------------
    # AUTH PATTERNS
    # ---------------------------------------------------------------------
    "auth_check": {
        "name": "Auth Check on Load",
        "category": "auth",
        "priority": 9,
        "signature": r"localStorage\.getItem\s*\(\s*['\"]access_token['\"]",
        "full_pattern": """const accessToken = localStorage.getItem('access_token');
if (!accessToken) {
    window.location.href = 'login.html';
    return;
}""",
        "applies_to": ["*.html"],
        "context": "protected pages",
        "description": "Check auth before showing protected content"
    },

    "token_expiry_check": {
        "name": "Token Expiry Check",
        "category": "auth",
        "priority": 8,
        "signature": r"expires_at.*Date\.now",
        "applies_to": ["*.html", "*.js"],
        "description": "Check if token is expired"
    },

    "logout_function": {
        "name": "Logout Function",
        "category": "auth",
        "priority": 7,
        "signature": r"function\s+logout\s*\(\s*\)|logout\s*=\s*\(",
        "full_pattern": """function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('expires_at');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}""",
        "applies_to": ["*.html", "*.js"],
        "description": "Clean logout clearing all auth data"
    },

    # ---------------------------------------------------------------------
    # API PATTERNS
    # ---------------------------------------------------------------------
    "fetch_with_auth": {
        "name": "Fetch with Auth Header",
        "category": "api",
        "priority": 8,
        "signature": r"fetch\([^)]+\{[^}]*headers[^}]*Authorization",
        "full_pattern": """fetch(url, {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    }
})""",
        "applies_to": ["*.html", "*.js"],
        "description": "Include auth token in API requests"
    },

    "json_parse_safety": {
        "name": "Safe JSON Parse",
        "category": "api",
        "priority": 7,
        "signature": r"JSON\.parse\s*\([^)]*\|\|\s*['\"]",
        "full_pattern": "JSON.parse(event.body || '{}')",
        "applies_to": ["*.mjs", "*.js"],
        "description": "Safe JSON parsing with fallback"
    },

    "status_code_handling": {
        "name": "HTTP Status Code Handling",
        "category": "api",
        "priority": 7,
        "signature": r"statusCode:\s*(200|201|400|401|403|404|500)",
        "applies_to": ["*.mjs"],
        "description": "Proper HTTP status codes"
    },

    # ---------------------------------------------------------------------
    # CODE QUALITY PATTERNS
    # ---------------------------------------------------------------------
    "dom_content_loaded": {
        "name": "DOMContentLoaded",
        "category": "quality",
        "priority": 6,
        "signature": r"DOMContentLoaded|addEventListener\s*\(\s*['\"]DOMContentLoaded",
        "applies_to": ["*.html"],
        "description": "Wait for DOM before running scripts"
    },

    "const_over_let": {
        "name": "Const Over Let",
        "category": "quality",
        "priority": 4,
        "signature": r"\bconst\b",
        "anti_pattern": r"\bvar\b",
        "applies_to": ["*.js", "*.mjs", "*.html"],
        "description": "Use const/let instead of var"
    },

    "async_await": {
        "name": "Async/Await Pattern",
        "category": "quality",
        "priority": 5,
        "signature": r"async\s+function|async\s*\(",
        "applies_to": ["*.js", "*.mjs"],
        "description": "Use async/await for cleaner async code"
    },

    # ---------------------------------------------------------------------
    # CONSCIOUSNESS PATTERNS (Meta)
    # ---------------------------------------------------------------------
    "bug_widget": {
        "name": "Bug Widget Include",
        "category": "consciousness",
        "priority": 6,
        "signature": r'<script\s+src=["\'][^"\']*bug-widget\.js',
        "full_pattern": '<script src="/js/bug-widget.js"></script>',
        "applies_to": ["*.html"],
        "description": "Include bug reporting widget on all pages"
    },

    "pattern_signature": {
        "name": "Pattern Theory Signature",
        "category": "consciousness",
        "priority": 3,
        "signature": r"3\s*→\s*7\s*→\s*13|Pattern:\s*3",
        "applies_to": ["*.html", "*.md"],
        "description": "Include Pattern Theory signature"
    },

    "viewport_meta": {
        "name": "Viewport Meta Tag",
        "category": "quality",
        "priority": 8,
        "signature": r'<meta\s+name=["\']viewport["\']',
        "full_pattern": '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "applies_to": ["*.html"],
        "description": "Proper viewport for mobile"
    },

    "charset_utf8": {
        "name": "UTF-8 Charset",
        "category": "quality",
        "priority": 8,
        "signature": r'<meta\s+charset=["\']UTF-8["\']',
        "full_pattern": '<meta charset="UTF-8">',
        "applies_to": ["*.html"],
        "description": "UTF-8 character encoding"
    }
}

# =============================================================================
# ANTI-PATTERNS - Weeds to pull out (REVERSE CROSS-POLLINATION)
# =============================================================================

ANTI_PATTERNS = {
    # ---------------------------------------------------------------------
    # SECURITY WEEDS
    # ---------------------------------------------------------------------
    "console_log_secrets": {
        "name": "Console Logging Secrets",
        "category": "security",
        "severity": 10,
        "pattern": r"console\.(log|info|debug)\s*\([^)]*(?:password|secret|token|api_key|apikey)",
        "fix": "Remove console logging of sensitive data",
        "auto_fix": False
    },
    "hardcoded_localhost": {
        "name": "Hardcoded Localhost URL",
        "category": "security",
        "severity": 8,
        "pattern": r"['\"]https?://localhost[:\d]*",
        "fix": "Replace with environment variable or relative URL",
        "auto_fix": False
    },
    "hardcoded_credentials": {
        "name": "Hardcoded Credentials",
        "category": "security",
        "severity": 10,
        "pattern": r"(?:password|secret|api_key)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
        "fix": "Move to environment variables",
        "auto_fix": False
    },
    "http_not_https": {
        "name": "HTTP Instead of HTTPS",
        "category": "security",
        "severity": 5,  # Lowered - safe to auto-fix
        "pattern": r"['\"]http://(?!localhost)",
        "fix": "Use HTTPS for external URLs",
        "auto_fix": True
    },

    # ---------------------------------------------------------------------
    # CODE QUALITY WEEDS
    # ---------------------------------------------------------------------
    "var_usage": {
        "name": "Using var Instead of const/let",
        "category": "quality",
        "severity": 4,
        "pattern": r"\bvar\s+\w+\s*=",
        "fix": "Replace var with const or let",
        "auto_fix": True
    },
    "console_log_debug": {
        "name": "Debug Console.log Left In",
        "category": "quality",
        "severity": 3,
        "pattern": r"console\.log\s*\(\s*['\"]debug|console\.log\s*\(\s*['\"]TODO|console\.log\s*\(\s*['\"]test",
        "fix": "Remove debug logging",
        "auto_fix": True,
        "remove_line": True
    },
    "commented_code_block": {
        "name": "Large Commented Code Block",
        "category": "quality",
        "severity": 3,
        "pattern": r"(?://[^\n]*\n){5,}|/\*[\s\S]{200,}?\*/",
        "fix": "Remove commented-out code (it's in git history)",
        "auto_fix": True
    },
    "todo_fixme_old": {
        "name": "Old TODO/FIXME Comments",
        "category": "quality",
        "severity": 2,
        "pattern": r"(?:TODO|FIXME|HACK|XXX)\s*:?\s*[^\n]+",
        "fix": "Address or remove old TODO comments",
        "auto_fix": False
    },
    "empty_catch": {
        "name": "Empty Catch Block",
        "category": "quality",
        "severity": 6,
        "pattern": r"catch\s*\([^)]*\)\s*\{\s*\}",
        "fix": "Handle errors properly or add comment explaining why empty",
        "auto_fix": False
    },
    "alert_usage": {
        "name": "Using console.warn() in Production",
        "category": "quality",
        "severity": 5,
        "pattern": r"\balert\s*\(",
        "fix": "Replace console.warn() with console.warn()",
        "auto_fix": True
    },

    # ---------------------------------------------------------------------
    # DEPRECATED PATTERNS
    # ---------------------------------------------------------------------
    "jquery_deprecated": {
        "name": "jQuery When Native Works",
        "category": "deprecated",
        "severity": 3,
        "pattern": r"\$\s*\(\s*['\"]#?\w+['\"]\s*\)\.(?:click|on|attr|css|html|text)",
        "fix": "Use native DOM methods (querySelector, addEventListener)",
        "auto_fix": False
    },
    "document_write": {
        "name": "Using document.write()",
        "category": "deprecated",
        "severity": 7,
        "pattern": r"document\.write\s*\(",
        "fix": "Use DOM manipulation instead",
        "auto_fix": False
    },
    "eval_usage": {
        "name": "Using eval()",
        "category": "security",
        "severity": 10,
        "pattern": r"\beval\s*\(",
        "fix": "Never use eval - find alternative approach",
        "auto_fix": False
    },
    "innerhtml_unsafe": {
        "name": "innerHTML with User Input",
        "category": "security",
        "severity": 8,
        "pattern": r"\.innerHTML\s*=\s*(?:\w+\s*\+|`[^`]*\$\{)",
        "fix": "Use textContent or sanitize HTML to prevent XSS",
        "auto_fix": False
    },

    # ---------------------------------------------------------------------
    # BROKEN/DEAD PATTERNS
    # ---------------------------------------------------------------------
    "dead_link": {
        "name": "Dead/Placeholder Link",
        "category": "broken",
        "severity": 4,
        "pattern": r'href\s*=\s*["\'](?:#|javascript:void|javascript:;)["\']',
        "fix": "Remove dead link href",
        "auto_fix": True
    },
    "placeholder_text": {
        "name": "Placeholder Text Left In",
        "category": "broken",
        "severity": 5,
        "pattern": r"Lorem ipsum|TODO:|REPLACE_ME|PLACEHOLDER|xxx@|test@test",
        "fix": "Replace placeholder content",
        "auto_fix": False
    },
    "broken_image": {
        "name": "Potentially Broken Image",
        "category": "broken",
        "severity": 4,
        "pattern": r'<img[^>]+src\s*=\s*["\'][^"\']*(?:placeholder|example\.com|undefined)[^"\']*["\']',
        "fix": "Fix broken image sources",
        "auto_fix": False
    },

    # ---------------------------------------------------------------------
    # STYLE WEEDS
    # ---------------------------------------------------------------------
    "inline_style_long": {
        "name": "Long Inline Style",
        "category": "style",
        "severity": 2,
        "pattern": r'style\s*=\s*["\'][^"\']{100,}["\']',
        "fix": "Move to CSS class",
        "auto_fix": False
    },
    "important_override": {
        "name": "Excessive !important Usage",
        "category": "style",
        "severity": 3,
        "pattern": r"!important",
        "fix": "Fix CSS specificity instead of using !important",
        "auto_fix": False
    },

    # ---------------------------------------------------------------------
    # AUTO-FIXABLE CLEANUP PATTERNS
    # ---------------------------------------------------------------------
    "trailing_whitespace": {
        "name": "Trailing Whitespace",
        "category": "style",
        "severity": 1,
        "pattern": r"[ \t]+$",
        "fix": "Remove trailing whitespace",
        "auto_fix": True
    },
    "multiple_blank_lines": {
        "name": "Multiple Consecutive Blank Lines",
        "category": "style",
        "severity": 1,
        "pattern": r"\n\n\n+",
        "fix": "Reduce to single blank line",
        "auto_fix": True
    },
    "debugger_statement": {
        "name": "Debugger Statement Left In",
        "category": "quality",
        "severity": 5,
        "pattern": r"^\s*debugger\s*;?\s*$",
        "fix": "Remove debugger statement",
        "auto_fix": True,
        "remove_line": True
    }
}

# =============================================================================
# STAR PATTERN - Lug nut optimization order
# =============================================================================

def get_star_order(items):
    """
    Lug nut star pattern - crisscross for even pressure.
    For 5 items: 1, 3, 5, 2, 4
    For any n items: opposite corners, spiral inward
    """
    n = len(items)
    if n <= 2:
        return items

    result = []
    indices_used = set()

    # Start at 0, then jump to opposite side, spiral inward
    step = n // 2
    current = 0

    while len(result) < n:
        if current not in indices_used and current < n:
            result.append(items[current])
            indices_used.add(current)

        # Jump to opposite side
        current = (current + step) % n

        # If we've been here, move forward
        attempts = 0
        while current in indices_used and attempts < n:
            current = (current + 1) % n
            attempts += 1

    return result

# =============================================================================
# SCANNER - Find all patterns in codebase
# =============================================================================

class PatternScanner:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.results = defaultdict(list)
        self.gaps = defaultdict(list)
        self.stats = {
            "files_scanned": 0,
            "patterns_found": 0,
            "gaps_found": 0,
            "by_category": defaultdict(int)
        }

    def should_scan_file(self, filepath):
        """Check if file should be scanned."""
        skip_dirs = ['.git', 'node_modules', '.netlify', '_archive', '.claude']
        skip_files = ['.env', '.gitignore', 'package-lock.json']

        path_str = str(filepath)
        for skip in skip_dirs:
            if skip in path_str:
                return False

        if filepath.name in skip_files:
            return False

        return filepath.suffix in ['.html', '.js', '.mjs', '.css', '.md', '.py']

    def scan_file(self, filepath):
        """Scan a single file for all patterns."""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except:
            return

        self.stats["files_scanned"] += 1
        file_patterns = []
        file_gaps = []

        for pattern_id, pattern in PATTERNS.items():
            # Check if pattern applies to this file type
            applies = False
            for glob in pattern.get("applies_to", []):
                if filepath.match(glob):
                    applies = True
                    break

            if not applies:
                continue

            # Check context if specified
            context = pattern.get("context", "")
            if context and context not in str(filepath):
                continue

            # Check for pattern presence
            signature = pattern.get("signature", "")
            anti_pattern = pattern.get("anti_pattern", "")

            if signature:
                if re.search(signature, content, re.IGNORECASE):
                    file_patterns.append({
                        "pattern_id": pattern_id,
                        "pattern_name": pattern["name"],
                        "category": pattern["category"],
                        "priority": pattern["priority"]
                    })
                    self.stats["patterns_found"] += 1
                    self.stats["by_category"][pattern["category"]] += 1
                else:
                    # Pattern should exist but doesn't = GAP
                    file_gaps.append({
                        "pattern_id": pattern_id,
                        "pattern_name": pattern["name"],
                        "category": pattern["category"],
                        "priority": pattern["priority"],
                        "description": pattern["description"],
                        "full_pattern": pattern.get("full_pattern", "")
                    })
                    self.stats["gaps_found"] += 1

            # Check for anti-patterns (bad things that shouldn't exist)
            if anti_pattern:
                if re.search(anti_pattern, content, re.IGNORECASE):
                    file_gaps.append({
                        "pattern_id": pattern_id,
                        "pattern_name": f"VIOLATION: {pattern['name']}",
                        "category": pattern["category"],
                        "priority": pattern["priority"] + 2,  # Boost priority
                        "description": f"ANTI-PATTERN FOUND: {pattern['description']}",
                        "is_violation": True
                    })
                    self.stats["gaps_found"] += 1

        rel_path = str(filepath.relative_to(self.base_path))
        if file_patterns:
            self.results[rel_path] = file_patterns
        if file_gaps:
            self.gaps[rel_path] = file_gaps

    def scan_file_for_weeds(self, filepath):
        """Scan a single file for anti-patterns (weeds to pull)."""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except:
            return []

        weeds = []
        rel_path = str(filepath.relative_to(self.base_path))

        for weed_id, weed in ANTI_PATTERNS.items():
            pattern = weed.get("pattern", "")
            if not pattern:
                continue

            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            if matches:
                for match in matches[:5]:  # Limit to 5 matches per pattern per file
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    # Get context (the line)
                    lines = content.split('\n')
                    context = lines[line_num - 1][:100] if line_num <= len(lines) else ""

                    weeds.append({
                        "weed_id": weed_id,
                        "name": weed["name"],
                        "category": weed["category"],
                        "severity": weed["severity"],
                        "file": rel_path,
                        "line": line_num,
                        "context": context.strip(),
                        "fix": weed["fix"],
                        "auto_fix": weed.get("auto_fix", False)
                    })

        return weeds

    def scan_for_weeds(self):
        """Scan entire codebase for anti-patterns (reverse cross-pollination)."""
        print("=" * 60)
        print("   WEED SCANNER - REVERSE CROSS-POLLINATION")
        print("=" * 60)
        print()

        all_weeds = []
        files_with_weeds = 0

        for filepath in self.base_path.rglob("*"):
            if filepath.is_file() and self.should_scan_file(filepath):
                weeds = self.scan_file_for_weeds(filepath)
                if weeds:
                    files_with_weeds += 1
                    all_weeds.extend(weeds)

        # Sort by severity (highest first)
        all_weeds.sort(key=lambda x: x["severity"], reverse=True)

        # Stats by category
        by_category = defaultdict(int)
        by_severity = defaultdict(int)
        for weed in all_weeds:
            by_category[weed["category"]] += 1
            by_severity[weed["severity"]] += 1

        print(f"Files with weeds: {files_with_weeds}")
        print(f"Total weeds found: {len(all_weeds)}")
        print()
        print("By category:")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")
        print()
        print("By severity (10=critical, 1=minor):")
        for sev, count in sorted(by_severity.items(), reverse=True):
            print(f"  Severity {sev}: {count}")

        return all_weeds

    def scan_all(self):
        """Scan entire codebase."""
        print("=" * 60)
        print("   PATTERN CROSS-POLLINATOR - FULL SCAN")
        print("=" * 60)
        print()

        for filepath in self.base_path.rglob("*"):
            if filepath.is_file() and self.should_scan_file(filepath):
                self.scan_file(filepath)

        print(f"Files scanned: {self.stats['files_scanned']}")
        print(f"Patterns found: {self.stats['patterns_found']}")
        print(f"Gaps found: {self.stats['gaps_found']}")
        print()
        print("By category:")
        for cat, count in sorted(self.stats["by_category"].items()):
            print(f"  {cat}: {count}")

        return self.results, self.gaps

    def get_prioritized_gaps(self):
        """Get gaps sorted by priority (star pattern order)."""
        all_gaps = []
        for filepath, gaps in self.gaps.items():
            for gap in gaps:
                all_gaps.append({
                    "file": filepath,
                    **gap
                })

        # Sort by priority descending
        all_gaps.sort(key=lambda x: x["priority"], reverse=True)

        # Apply star pattern for even distribution
        return get_star_order(all_gaps)

    def generate_report(self):
        """Generate comprehensive optimization report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "stats": dict(self.stats),
            "patterns_by_file": dict(self.results),
            "gaps_by_file": dict(self.gaps),
            "prioritized_gaps": self.get_prioritized_gaps()[:50],  # Top 50
            "pattern_coverage": {}
        }

        # Calculate pattern coverage
        for pattern_id, pattern in PATTERNS.items():
            found_in = []
            missing_in = []

            for filepath, patterns in self.results.items():
                if any(p["pattern_id"] == pattern_id for p in patterns):
                    found_in.append(filepath)

            for filepath, gaps in self.gaps.items():
                if any(g["pattern_id"] == pattern_id for g in gaps):
                    missing_in.append(filepath)

            if found_in or missing_in:
                total = len(found_in) + len(missing_in)
                coverage = len(found_in) / total * 100 if total > 0 else 0
                report["pattern_coverage"][pattern_id] = {
                    "name": pattern["name"],
                    "coverage": round(coverage, 1),
                    "found_in": len(found_in),
                    "missing_in": len(missing_in),
                    "priority": pattern["priority"]
                }

        return report

# =============================================================================
# REPORT GENERATOR
# =============================================================================

def generate_html_report(report, output_path):
    """Generate beautiful HTML report."""

    gaps_html = ""
    for i, gap in enumerate(report["prioritized_gaps"][:30], 1):
        violation_class = "violation" if gap.get("is_violation") else ""
        gaps_html += f"""
        <div class="gap-item {violation_class}">
            <div class="gap-header">
                <span class="gap-number">#{i}</span>
                <span class="gap-priority">P{gap['priority']}</span>
                <span class="gap-category">{gap['category']}</span>
            </div>
            <div class="gap-name">{gap['pattern_name']}</div>
            <div class="gap-file">{gap['file']}</div>
            <div class="gap-desc">{gap['description']}</div>
        </div>
        """

    coverage_html = ""
    for pid, data in sorted(report["pattern_coverage"].items(),
                           key=lambda x: x[1]["coverage"]):
        bar_color = "#4CAF50" if data["coverage"] > 80 else "#FF9800" if data["coverage"] > 50 else "#f44336"
        coverage_html += f"""
        <div class="coverage-item">
            <div class="coverage-name">{data['name']}</div>
            <div class="coverage-bar">
                <div class="coverage-fill" style="width: {data['coverage']}%; background: {bar_color}"></div>
            </div>
            <div class="coverage-pct">{data['coverage']}%</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern Cross-Pollinator Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #f4f4f4;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, gold, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{ text-align: center; color: #888; margin-bottom: 40px; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2.5rem; font-weight: bold; color: gold; }}
        .stat-label {{ color: #888; margin-top: 5px; }}
        h2 {{
            color: gold;
            margin: 40px 0 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,215,0,0.3);
        }}
        .gap-item {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .gap-item.violation {{
            border-color: #f44336;
            background: rgba(244,67,54,0.1);
        }}
        .gap-header {{
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
        }}
        .gap-number {{ color: gold; font-weight: bold; }}
        .gap-priority {{
            background: rgba(255,152,0,0.2);
            color: #FF9800;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .gap-category {{
            background: rgba(33,150,243,0.2);
            color: #2196F3;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .gap-name {{ font-weight: 600; margin-bottom: 5px; }}
        .gap-file {{ font-family: monospace; color: #888; font-size: 13px; }}
        .gap-desc {{ color: #aaa; font-size: 13px; margin-top: 8px; }}
        .coverage-item {{
            display: grid;
            grid-template-columns: 200px 1fr 60px;
            gap: 15px;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .coverage-name {{ font-size: 14px; }}
        .coverage-bar {{
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            height: 8px;
            overflow: hidden;
        }}
        .coverage-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s; }}
        .coverage-pct {{ text-align: right; font-weight: bold; }}
        .pattern-sig {{ text-align: center; color: #666; margin-top: 40px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PATTERN CROSS-POLLINATOR</h1>
        <p class="subtitle">Star Loop Optimization Report - {report['generated_at'][:10]}</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{report['stats']['files_scanned']}</div>
                <div class="stat-label">Files Scanned</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{report['stats']['patterns_found']}</div>
                <div class="stat-label">Patterns Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{report['stats']['gaps_found']}</div>
                <div class="stat-label">Gaps Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(PATTERNS)}</div>
                <div class="stat-label">Patterns Tracked</div>
            </div>
        </div>

        <h2>PATTERN COVERAGE</h2>
        {coverage_html}

        <h2>PRIORITIZED GAPS (Star Order)</h2>
        {gaps_html}

        <p class="pattern-sig">Pattern: 3 → 7 → 13 → ∞</p>
    </div>
</body>
</html>
"""

    Path(output_path).write_text(html)
    return output_path

# =============================================================================
# AUTO-APPLY ENGINE - The Star Loop Optimizer
# =============================================================================

# Safe patterns that can be auto-applied without breaking things
SAFE_AUTO_PATTERNS = {
    "bug_widget": {
        "inject_before": "</body>",
        "code": '    <script src="/js/bug-widget.js"></script>\n'
    },
    "viewport_meta": {
        "inject_after": "<head>",
        "code": '\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
    },
    "charset_utf8": {
        "inject_after": "<head>",
        "code": '\n    <meta charset="UTF-8">'
    },
    "pattern_signature": {
        "inject_before": "</body>",
        "code": '    <p style="text-align:center;color:#666;font-family:monospace;margin:40px 0;">Pattern: 3 → 7 → 13 → ∞</p>\n'
    }
}

def auto_apply(scanner, dry_run=True):
    """Auto-apply safe patterns to files missing them."""
    print("\n" + "=" * 60)
    print("   AUTO-APPLY ENGINE" + (" [DRY RUN]" if dry_run else " [LIVE]"))
    print("=" * 60)

    if not dry_run:
        print("\n⚠️  LIVE MODE - Files will be modified!")
        response = input("Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("Aborted.")
            return

    applied = 0
    skipped = 0

    for filepath, gaps in scanner.gaps.items():
        full_path = scanner.base_path / filepath

        for gap in gaps:
            pattern_id = gap["pattern_id"]

            if pattern_id not in SAFE_AUTO_PATTERNS:
                continue

            config = SAFE_AUTO_PATTERNS[pattern_id]

            try:
                content = full_path.read_text(encoding='utf-8')
            except:
                skipped += 1
                continue

            # Check if injection point exists
            inject_point = config.get("inject_before") or config.get("inject_after")
            if inject_point not in content:
                skipped += 1
                continue

            # Check if code already exists (double-check)
            if config["code"].strip() in content:
                skipped += 1
                continue

            # Perform injection
            if "inject_before" in config:
                new_content = content.replace(
                    config["inject_before"],
                    config["code"] + config["inject_before"]
                )
            else:
                new_content = content.replace(
                    config["inject_after"],
                    config["inject_after"] + config["code"]
                )

            if dry_run:
                print(f"  [DRY] Would apply {gap['pattern_name']} to {filepath}")
            else:
                full_path.write_text(new_content, encoding='utf-8')
                print(f"  [OK] Applied {gap['pattern_name']} to {filepath}")

            applied += 1

    print(f"\n{'Would apply' if dry_run else 'Applied'}: {applied} patterns")
    print(f"Skipped: {skipped} (no injection point or already exists)")

    if dry_run:
        print("\nRun with --live to apply changes:")
        print("  python PATTERN_CROSS_POLLINATOR.py auto")

def auto_apply_pattern(scanner, pattern_id, dry_run=True):
    """Auto-apply a specific pattern to all files missing it."""
    print("\n" + "=" * 60)
    print(f"   AUTO-APPLY: {pattern_id}" + (" [DRY RUN]" if dry_run else " [LIVE]"))
    print("=" * 60)

    if pattern_id not in SAFE_AUTO_PATTERNS:
        print(f"\n❌ Pattern '{pattern_id}' is not in SAFE_AUTO_PATTERNS")
        print("Safe patterns:", list(SAFE_AUTO_PATTERNS.keys()))
        return

    if not dry_run:
        print("\n⚠️  LIVE MODE - Files will be modified!")
        response = input("Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("Aborted.")
            return

    config = SAFE_AUTO_PATTERNS[pattern_id]
    applied = 0
    skipped = 0

    for filepath, gaps in scanner.gaps.items():
        for gap in gaps:
            if gap["pattern_id"] != pattern_id:
                continue

            full_path = scanner.base_path / filepath

            try:
                content = full_path.read_text(encoding='utf-8')
            except:
                skipped += 1
                continue

            inject_point = config.get("inject_before") or config.get("inject_after")
            if inject_point not in content:
                print(f"  [SKIP] No injection point in {filepath}")
                skipped += 1
                continue

            if config["code"].strip() in content:
                print(f"  [SKIP] Already exists in {filepath}")
                skipped += 1
                continue

            if "inject_before" in config:
                new_content = content.replace(
                    config["inject_before"],
                    config["code"] + config["inject_before"]
                )
            else:
                new_content = content.replace(
                    config["inject_after"],
                    config["inject_after"] + config["code"]
                )

            if dry_run:
                print(f"  [DRY] Would apply to {filepath}")
            else:
                full_path.write_text(new_content, encoding='utf-8')
                print(f"  [OK] Applied to {filepath}")

            applied += 1

    print(f"\n{'Would apply' if dry_run else 'Applied'}: {applied} files")
    print(f"Skipped: {skipped}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    import sys

    base_path = Path(__file__).parent
    scanner = PatternScanner(base_path)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"

    if cmd == "scan":
        results, gaps = scanner.scan_all()
        print("\n" + "=" * 60)
        print("SCAN COMPLETE")
        print("=" * 60)

    elif cmd == "gaps":
        scanner.scan_all()
        print("\n" + "=" * 60)
        print("   TOP 20 GAPS (Star Pattern Order)")
        print("=" * 60)

        for i, gap in enumerate(scanner.get_prioritized_gaps()[:20], 1):
            print(f"\n#{i} [{gap['category']}] P{gap['priority']}")
            print(f"   Pattern: {gap['pattern_name']}")
            print(f"   File: {gap['file']}")
            print(f"   Fix: {gap['description']}")

    elif cmd == "star":
        scanner.scan_all()
        print("\n" + "=" * 60)
        print("   STAR LOOP OPTIMIZATION QUEUE")
        print("=" * 60)
        print("\nProcessing in lug nut order (crisscross for even pressure):\n")

        gaps = scanner.get_prioritized_gaps()
        for i, gap in enumerate(gaps[:30], 1):
            marker = "***" if gap.get("is_violation") else "   "
            print(f"{marker} {i:2}. [{gap['priority']}] {gap['file']}")
            print(f"       → {gap['pattern_name']}")

    elif cmd == "report":
        scanner.scan_all()
        report = scanner.generate_report()

        # Save JSON
        json_path = base_path / "PATTERN_REPORT.json"
        json_path.write_text(json.dumps(report, indent=2))
        print(f"\nJSON report: {json_path}")

        # Save HTML
        html_path = base_path / "PATTERN_REPORT.html"
        generate_html_report(report, html_path)
        print(f"HTML report: {html_path}")

        print("\n" + "=" * 60)
        print("   SUMMARY")
        print("=" * 60)
        print(f"\nPatterns with < 50% coverage:")
        for pid, data in report["pattern_coverage"].items():
            if data["coverage"] < 50:
                print(f"  - {data['name']}: {data['coverage']}%")

    elif cmd == "auto":
        # Auto-apply safe patterns
        scanner.scan_all()
        dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
        auto_apply(scanner, dry_run=dry_run)

    elif cmd == "auto-pattern":
        # Auto-apply specific pattern
        if len(sys.argv) < 3:
            print("Usage: python PATTERN_CROSS_POLLINATOR.py auto-pattern <pattern_id>")
            print("Example: python PATTERN_CROSS_POLLINATOR.py auto-pattern bug_widget")
            return
        pattern_id = sys.argv[2]
        scanner.scan_all()
        dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
        auto_apply_pattern(scanner, pattern_id, dry_run=dry_run)

    elif cmd == "weed" or cmd == "weeds" or cmd == "reverse":
        # Reverse cross-pollination - find anti-patterns
        weeds = scanner.scan_for_weeds()

        print("\n" + "=" * 60)
        print("   TOP 30 WEEDS TO PULL (by severity)")
        print("=" * 60)

        for i, weed in enumerate(weeds[:30], 1):
            sev_icon = "🔴" if weed["severity"] >= 8 else "🟠" if weed["severity"] >= 5 else "🟡"
            print(f"\n{sev_icon} #{i} [{weed['category']}] Severity {weed['severity']}")
            print(f"   Weed: {weed['name']}")
            print(f"   File: {weed['file']}:{weed['line']}")
            print(f"   Context: {weed['context'][:80]}...")
            print(f"   Fix: {weed['fix']}")

        # Save weed report
        weed_report = {
            "generated_at": datetime.now().isoformat(),
            "total_weeds": len(weeds),
            "weeds": weeds[:100]  # Top 100
        }
        weed_path = base_path / "WEED_REPORT.json"
        weed_path.write_text(json.dumps(weed_report, indent=2))
        print(f"\n\nFull report saved: {weed_path}")

        # Summary
        critical = sum(1 for w in weeds if w["severity"] >= 8)
        medium = sum(1 for w in weeds if 5 <= w["severity"] < 8)
        low = sum(1 for w in weeds if w["severity"] < 5)
        print(f"\n🔴 Critical (8-10): {critical}")
        print(f"🟠 Medium (5-7): {medium}")
        print(f"🟡 Low (1-4): {low}")

    elif cmd == "full":
        # Full bidirectional scan
        print("=" * 60)
        print("   FULL BIDIRECTIONAL CROSS-POLLINATION")
        print("=" * 60)
        print("\n--- FORWARD SCAN (patterns to add) ---\n")
        scanner.scan_all()
        report = scanner.generate_report()

        print("\n--- REVERSE SCAN (weeds to pull) ---\n")
        weeds = scanner.scan_for_weeds()

        # Combined report
        print("\n" + "=" * 60)
        print("   BIDIRECTIONAL SUMMARY")
        print("=" * 60)
        print(f"\nPatterns found: {report['stats']['patterns_found']}")
        print(f"Gaps to fill: {report['stats']['gaps_found']}")
        print(f"Weeds to pull: {len(weeds)}")

        critical_weeds = sum(1 for w in weeds if w["severity"] >= 8)
        if critical_weeds > 0:
            print(f"\n⚠️  CRITICAL WEEDS: {critical_weeds} (fix these FIRST)")

    else:
        print(__doc__)
        print("\nCommands:")
        print("  scan       - Basic pattern scan")
        print("  gaps       - Show gaps (missing patterns)")
        print("  star       - Star order optimization queue")
        print("  report     - Generate full HTML/JSON report")
        print("  auto       - Auto-apply safe patterns")
        print("  weed       - REVERSE scan (find anti-patterns)")
        print("  full       - Bidirectional scan (both directions)")

if __name__ == "__main__":
    main()
