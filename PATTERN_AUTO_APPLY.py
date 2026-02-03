#!/usr/bin/env python3
"""
PATTERN AUTO-APPLY v1.0
THE STAR LOOP INJECTION ENGINE

Safely auto-applies missing patterns to codebase files.
Uses dry-run mode by default for safety.

Priority Order: security > auth > api > ux > quality > consciousness

Usage:
    python PATTERN_AUTO_APPLY.py dry-run              # Preview changes (SAFE)
    python PATTERN_AUTO_APPLY.py apply                # Apply all safe patterns
    python PATTERN_AUTO_APPLY.py apply --pattern=X   # Apply specific pattern
    python PATTERN_AUTO_APPLY.py apply --file=X      # Apply to specific file
    python PATTERN_AUTO_APPLY.py rollback             # Undo last apply
"""

import os
import re
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# =============================================================================
# AUTO-APPLY PATTERN DEFINITIONS
# Each pattern has injection_point and code_snippet
# =============================================================================

AUTO_APPLY_PATTERNS = {
    # -------------------------------------------------------------------------
    # SECURITY PATTERNS (Priority 10)
    # -------------------------------------------------------------------------
    "token_expiry_check": {
        "name": "Token Expiry Check",
        "category": "auth",
        "priority": 10,
        "safety": "safe",  # safe = auto-apply, review = manual review
        "applies_to": ["*.html"],
        "detect": r"localStorage\.getItem\s*\(\s*['\"]access_token['\"]",
        "missing": r"expires_at.*Date\.now",
        "injection_point": "after_auth_check",
        "code_snippet": """
// Token expiry check - auto-added by Pattern Cross-Pollinator
function isTokenExpired() {
    const expiresAt = localStorage.getItem('expires_at');
    if (!expiresAt) return true;
    return Date.now() > parseInt(expiresAt);
}

if (isTokenExpired()) {
    console.log('Token expired, redirecting to login');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('expires_at');
    window.location.href = 'login.html';
}
""",
        "insert_after": r"const\s+accessToken\s*=\s*localStorage\.getItem\s*\(\s*['\"]access_token['\"]\s*\)",
        "description": "Check if auth token is expired before making requests"
    },

    "logout_function": {
        "name": "Logout Function",
        "category": "auth",
        "priority": 9,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"localStorage\.getItem\s*\(\s*['\"]access_token['\"]",
        "missing": r"function\s+logout\s*\(\s*\)|logout\s*=\s*\(",
        "injection_point": "before_closing_script",
        "code_snippet": """
// Logout function - auto-added by Pattern Cross-Pollinator
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('expires_at');
    localStorage.removeItem('user');
    sessionStorage.clear();
    window.location.href = 'login.html';
}
""",
        "insert_before": r"</script>",
        "description": "Clean logout clearing all auth data"
    },

    # -------------------------------------------------------------------------
    # API PATTERNS (Priority 8)
    # -------------------------------------------------------------------------
    "fetch_with_auth": {
        "name": "Fetch with Auth Header Template",
        "category": "api",
        "priority": 8,
        "safety": "review",  # Needs review - might break existing fetch calls
        "applies_to": ["*.html", "*.js"],
        "detect": r"fetch\s*\(",
        "missing": r"fetch\([^)]+\{[^}]*headers[^}]*Authorization",
        "injection_point": "utility_functions",
        "code_snippet": """
// Authenticated fetch wrapper - auto-added by Pattern Cross-Pollinator
async function fetchWithAuth(url, options = {}) {
    const accessToken = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
        ...options.headers
    };

    const response = await fetch(url, { ...options, headers });

    // Auto-logout on 401
    if (response.status === 401) {
        logout();
        throw new Error('Session expired');
    }

    return response;
}
""",
        "insert_before": r"</script>",
        "description": "Wrapper for fetch calls with auth headers and 401 handling"
    },

    "safe_json_parse": {
        "name": "Safe JSON Parse",
        "category": "api",
        "priority": 7,
        "safety": "safe",
        "applies_to": ["*.mjs"],
        "detect": r"JSON\.parse\s*\(",
        "missing": r"JSON\.parse\s*\([^)]*\|\|\s*['\"]",
        "injection_point": "replace_pattern",
        "find_replace": [
            (r"JSON\.parse\s*\(\s*event\.body\s*\)", "JSON.parse(event.body || '{}')"),
        ],
        "description": "Safe JSON parsing with fallback"
    },

    # -------------------------------------------------------------------------
    # UX PATTERNS (Priority 7)
    # -------------------------------------------------------------------------
    "error_display": {
        "name": "Error Display Component",
        "category": "ux",
        "priority": 7,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"<script",
        "missing": r"error-message|errorMessage|showError",
        "injection_point": "after_body_open",
        "code_snippet": """
<!-- Error Display Component - auto-added by Pattern Cross-Pollinator -->
<div id="errorDisplay" style="display:none; position:fixed; top:20px; right:20px; background:#f44336; color:white; padding:15px 25px; border-radius:8px; z-index:10000; max-width:400px; box-shadow:0 4px 20px rgba(0,0,0,0.3);">
    <span id="errorMessage"></span>
    <button onclick="hideError()" style="background:none; border:none; color:white; margin-left:15px; cursor:pointer; font-size:18px;">&times;</button>
</div>
<script>
function showError(message, duration = 5000) {
    const el = document.getElementById('errorDisplay');
    document.getElementById('errorMessage').textContent = message;
    el.style.display = 'block';
    if (duration > 0) setTimeout(hideError, duration);
}
function hideError() {
    document.getElementById('errorDisplay').style.display = 'none';
}
</script>
""",
        "insert_after": r"<body[^>]*>",
        "description": "Display errors to users clearly"
    },

    "loading_state": {
        "name": "Loading State Component",
        "category": "ux",
        "priority": 6,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"fetch\s*\(",
        "missing": r"loading|Loading|isLoading|setLoading",
        "injection_point": "after_body_open",
        "code_snippet": """
<!-- Loading State Component - auto-added by Pattern Cross-Pollinator -->
<div id="loadingOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:9999; justify-content:center; align-items:center;">
    <div style="text-align:center; color:white;">
        <div style="width:50px; height:50px; border:3px solid rgba(255,255,255,0.3); border-top-color:gold; border-radius:50%; animation:spin 1s linear infinite; margin:0 auto 15px;"></div>
        <p id="loadingMessage">Loading...</p>
    </div>
</div>
<style>@keyframes spin { to { transform: rotate(360deg); } }</style>
<script>
function showLoading(message = 'Loading...') {
    document.getElementById('loadingMessage').textContent = message;
    document.getElementById('loadingOverlay').style.display = 'flex';
}
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}
</script>
""",
        "insert_after": r"<body[^>]*>",
        "description": "Show loading state while fetching data"
    },

    # -------------------------------------------------------------------------
    # QUALITY PATTERNS (Priority 6)
    # -------------------------------------------------------------------------
    "mobile_responsive": {
        "name": "Mobile Responsive Breakpoint",
        "category": "quality",
        "priority": 6,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"<style",
        "missing": r"@media\s*\(\s*max-width:\s*600px",
        "injection_point": "before_style_close",
        "code_snippet": """
        /* Mobile Responsive - auto-added by Pattern Cross-Pollinator */
        @media (max-width: 768px) {
            .container { padding: 15px; }
            h1 { font-size: 1.8rem; }
            h2 { font-size: 1.4rem; }
        }
        @media (max-width: 480px) {
            body { font-size: 14px; }
            .card { padding: 15px; }
            button { width: 100%; margin-bottom: 10px; }
        }
""",
        "insert_before": r"</style>",
        "description": "Mobile-first responsive breakpoints"
    },

    "dom_content_loaded": {
        "name": "DOMContentLoaded Wrapper",
        "category": "quality",
        "priority": 5,
        "safety": "review",  # Might break existing script order
        "applies_to": ["*.html"],
        "detect": r"<script[^>]*>(?!.*DOMContentLoaded)",
        "missing": r"DOMContentLoaded",
        "injection_point": "wrap_script",
        "description": "Wait for DOM before running scripts"
    },

    # -------------------------------------------------------------------------
    # CONSCIOUSNESS PATTERNS (Priority 3)
    # -------------------------------------------------------------------------
    "bug_widget": {
        "name": "Bug Widget Include",
        "category": "consciousness",
        "priority": 4,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"</body>",
        "missing": r'<script\s+src=["\'][^"\']*bug-widget\.js',
        "injection_point": "before_body_close",
        "code_snippet": """
<!-- Bug Widget - auto-added by Pattern Cross-Pollinator -->
<script src="/js/bug-widget.js"></script>
""",
        "insert_before": r"</body>",
        "description": "Include bug reporting widget on all pages"
    },

    "pattern_signature": {
        "name": "Pattern Theory Signature",
        "category": "consciousness",
        "priority": 3,
        "safety": "safe",
        "applies_to": ["*.html"],
        "detect": r"</body>",
        "missing": r"3\s*→\s*7\s*→\s*13|Pattern:\s*3",
        "injection_point": "before_body_close",
        "code_snippet": """
<!-- Pattern: 3 → 7 → 13 → ∞ -->
""",
        "insert_before": r"</body>",
        "description": "Include Pattern Theory signature"
    },
}

# =============================================================================
# BACKUP SYSTEM
# =============================================================================

class BackupManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.backup_dir = self.base_path / ".pattern_backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.manifest_path = self.backup_dir / "manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if self.manifest_path.exists():
            return json.loads(self.manifest_path.read_text())
        return {"backups": [], "rollback_stack": []}

    def _save_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2))

    def backup_file(self, filepath, session_id):
        """Backup a file before modification."""
        rel_path = filepath.relative_to(self.base_path)
        backup_name = f"{session_id}_{rel_path.name}_{datetime.now().strftime('%H%M%S')}"
        backup_path = self.backup_dir / backup_name

        shutil.copy2(filepath, backup_path)

        backup_record = {
            "original": str(rel_path),
            "backup": backup_name,
            "session": session_id,
            "timestamp": datetime.now().isoformat()
        }
        self.manifest["backups"].append(backup_record)
        self.manifest["rollback_stack"].append(backup_record)
        self._save_manifest()

        return backup_path

    def rollback_last_session(self):
        """Rollback all changes from last session."""
        if not self.manifest["rollback_stack"]:
            return []

        last_session = self.manifest["rollback_stack"][-1]["session"]
        rolled_back = []

        for record in reversed(self.manifest["rollback_stack"]):
            if record["session"] == last_session:
                backup_path = self.backup_dir / record["backup"]
                original_path = self.base_path / record["original"]

                if backup_path.exists():
                    shutil.copy2(backup_path, original_path)
                    rolled_back.append(record["original"])
                    self.manifest["rollback_stack"].remove(record)

        self._save_manifest()
        return rolled_back

# =============================================================================
# AUTO-APPLY ENGINE
# =============================================================================

class PatternAutoApply:
    def __init__(self, base_path, dry_run=True):
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        self.backup = BackupManager(base_path)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.changes = []
        self.skipped = []
        self.errors = []

    def should_process_file(self, filepath):
        """Check if file should be processed."""
        skip_dirs = ['.git', 'node_modules', '.netlify', '_archive', '.claude', '.pattern_backups']
        skip_files = ['.env', '.gitignore', 'package-lock.json']

        path_str = str(filepath)
        for skip in skip_dirs:
            if skip in path_str:
                return False

        if filepath.name in skip_files:
            return False

        return filepath.suffix in ['.html', '.js', '.mjs']

    def check_pattern_needed(self, content, pattern):
        """Check if pattern is needed in this file."""
        # Must have the detection pattern (context)
        detect = pattern.get("detect", "")
        if detect and not re.search(detect, content, re.IGNORECASE):
            return False

        # Must NOT have the missing pattern (gap)
        missing = pattern.get("missing", "")
        if missing and re.search(missing, content, re.IGNORECASE):
            return False

        return True

    def apply_pattern(self, filepath, pattern_id, pattern):
        """Apply a single pattern to a file."""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.errors.append({"file": str(filepath), "error": str(e)})
            return False

        if not self.check_pattern_needed(content, pattern):
            return False

        # Determine injection method
        injection = pattern.get("injection_point", "")
        new_content = content

        if injection == "replace_pattern":
            # Find and replace patterns
            for find, replace in pattern.get("find_replace", []):
                new_content = re.sub(find, replace, new_content)

        elif "insert_after" in pattern:
            # Insert after a pattern
            insert_point = pattern["insert_after"]
            snippet = pattern["code_snippet"]
            match = re.search(insert_point, new_content)
            if match:
                pos = match.end()
                new_content = new_content[:pos] + "\n" + snippet + new_content[pos:]

        elif "insert_before" in pattern:
            # Insert before a pattern
            insert_point = pattern["insert_before"]
            snippet = pattern["code_snippet"]
            match = re.search(insert_point, new_content)
            if match:
                pos = match.start()
                new_content = new_content[:pos] + snippet + "\n" + new_content[pos:]

        else:
            # Unknown injection method
            self.skipped.append({
                "file": str(filepath),
                "pattern": pattern_id,
                "reason": f"Unknown injection point: {injection}"
            })
            return False

        # Check if content changed
        if new_content == content:
            return False

        # Record the change
        change = {
            "file": str(filepath.relative_to(self.base_path)),
            "pattern_id": pattern_id,
            "pattern_name": pattern["name"],
            "category": pattern["category"],
            "safety": pattern.get("safety", "review"),
            "lines_added": snippet.count('\n') if 'snippet' in dir() else 0
        }

        if self.dry_run:
            change["status"] = "would_apply"
            self.changes.append(change)
            return True
        else:
            # Backup and apply
            self.backup.backup_file(filepath, self.session_id)
            filepath.write_text(new_content, encoding='utf-8')
            change["status"] = "applied"
            self.changes.append(change)
            return True

    def scan_and_apply(self, pattern_filter=None, file_filter=None, safe_only=True):
        """Scan codebase and apply patterns."""
        print("=" * 60)
        print(f"   PATTERN AUTO-APPLY - {'DRY RUN' if self.dry_run else 'APPLYING'}")
        print("=" * 60)
        print()

        # Sort patterns by priority
        sorted_patterns = sorted(
            AUTO_APPLY_PATTERNS.items(),
            key=lambda x: x[1]["priority"],
            reverse=True
        )

        for filepath in self.base_path.rglob("*"):
            if not filepath.is_file():
                continue
            if not self.should_process_file(filepath):
                continue
            if file_filter and file_filter not in str(filepath):
                continue

            for pattern_id, pattern in sorted_patterns:
                # Filter by pattern name if specified
                if pattern_filter and pattern_filter != pattern_id:
                    continue

                # Skip unsafe patterns in safe mode
                if safe_only and pattern.get("safety") != "safe":
                    continue

                # Check file type match
                applies = False
                for glob in pattern.get("applies_to", []):
                    if filepath.match(glob):
                        applies = True
                        break

                if not applies:
                    continue

                self.apply_pattern(filepath, pattern_id, pattern)

        return self.generate_report()

    def generate_report(self):
        """Generate application report."""
        report = {
            "session_id": self.session_id,
            "dry_run": self.dry_run,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_changes": len(self.changes),
                "by_category": defaultdict(int),
                "by_pattern": defaultdict(int),
                "by_safety": defaultdict(int)
            },
            "changes": self.changes,
            "skipped": self.skipped,
            "errors": self.errors
        }

        for change in self.changes:
            report["summary"]["by_category"][change["category"]] += 1
            report["summary"]["by_pattern"][change["pattern_id"]] += 1
            report["summary"]["by_safety"][change["safety"]] += 1

        # Convert defaultdicts
        report["summary"]["by_category"] = dict(report["summary"]["by_category"])
        report["summary"]["by_pattern"] = dict(report["summary"]["by_pattern"])
        report["summary"]["by_safety"] = dict(report["summary"]["by_safety"])

        return report

# =============================================================================
# CLI INTERFACE
# =============================================================================

def print_report(report):
    """Pretty print the report."""
    print()
    print("=" * 60)
    print("   RESULTS")
    print("=" * 60)
    print()
    print(f"Session: {report['session_id']}")
    print(f"Mode: {'DRY RUN (no changes made)' if report['dry_run'] else 'APPLIED'}")
    print(f"Total changes: {report['summary']['total_changes']}")
    print()

    if report["summary"]["by_category"]:
        print("By Category:")
        for cat, count in sorted(report["summary"]["by_category"].items()):
            print(f"  {cat}: {count}")
        print()

    if report["summary"]["by_pattern"]:
        print("By Pattern:")
        for pat, count in sorted(report["summary"]["by_pattern"].items()):
            print(f"  {pat}: {count}")
        print()

    if report["changes"]:
        print("Changes:")
        for i, change in enumerate(report["changes"][:20], 1):
            status = "[WOULD APPLY]" if change["status"] == "would_apply" else "[APPLIED]"
            print(f"  {i}. {status} {change['pattern_name']}")
            print(f"      → {change['file']}")

        if len(report["changes"]) > 20:
            print(f"  ... and {len(report['changes']) - 20} more")

    if report["errors"]:
        print("\nErrors:")
        for err in report["errors"]:
            print(f"  {err['file']}: {err['error']}")

    print()
    if report["dry_run"]:
        print("To apply these changes, run:")
        print("  python PATTERN_AUTO_APPLY.py apply")
    else:
        print("To rollback these changes, run:")
        print("  python PATTERN_AUTO_APPLY.py rollback")

def main():
    import sys

    base_path = Path(__file__).parent
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dry-run"

    # Parse options
    pattern_filter = None
    file_filter = None
    safe_only = True

    for arg in sys.argv[2:]:
        if arg.startswith("--pattern="):
            pattern_filter = arg.split("=")[1]
        elif arg.startswith("--file="):
            file_filter = arg.split("=")[1]
        elif arg == "--unsafe":
            safe_only = False

    if cmd == "dry-run":
        engine = PatternAutoApply(base_path, dry_run=True)
        report = engine.scan_and_apply(pattern_filter, file_filter, safe_only)
        print_report(report)

        # Save report
        report_path = base_path / "PATTERN_AUTO_APPLY_PREVIEW.json"
        report_path.write_text(json.dumps(report, indent=2))
        print(f"Preview saved to: {report_path}")

    elif cmd == "apply":
        engine = PatternAutoApply(base_path, dry_run=False)
        report = engine.scan_and_apply(pattern_filter, file_filter, safe_only)
        print_report(report)

        # Save report
        report_path = base_path / f"PATTERN_AUTO_APPLY_{engine.session_id}.json"
        report_path.write_text(json.dumps(report, indent=2))
        print(f"Report saved to: {report_path}")

    elif cmd == "rollback":
        backup = BackupManager(base_path)
        rolled_back = backup.rollback_last_session()

        if rolled_back:
            print("Rolled back files:")
            for f in rolled_back:
                print(f"  {f}")
        else:
            print("Nothing to rollback.")

    elif cmd == "patterns":
        print("Available patterns for auto-apply:")
        print()
        for pid, pattern in sorted(AUTO_APPLY_PATTERNS.items(),
                                   key=lambda x: x[1]["priority"], reverse=True):
            safety = "[SAFE]" if pattern.get("safety") == "safe" else "[REVIEW]"
            print(f"  P{pattern['priority']} {safety} {pid}")
            print(f"      {pattern['name']} - {pattern['description']}")
            print()

    else:
        print(__doc__)

if __name__ == "__main__":
    main()
