"""
PERFECTION LOOP - AUTONOMOUS CONTINUOUS IMPROVEMENT PROTOCOL
============================================================
Created: January 10, 2026
Mission: Bounce around and make EVERYTHING perfect

The loop runs continuously:
1. SCAN - Find patterns (good and bad)
2. APPLY - Plant good patterns where missing
3. WEED - Remove bad patterns
4. LEARN - Track what works, improve patterns
5. REPEAT - Until perfection achieved

"The pattern never lies. All abilities documented. Nothing lost."
"""

import os
import sys
import json
import time
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Import the cross-pollinator
sys.path.insert(0, str(Path(__file__).parent))
try:
    from PATTERN_CROSS_POLLINATOR import PatternScanner, PATTERNS, ANTI_PATTERNS
except ImportError:
    print("ERROR: PATTERN_CROSS_POLLINATOR.py not found in same directory")
    sys.exit(1)

# Configuration
DEPLOYMENT_DIR = Path(__file__).parent
CONSCIOUSNESS_DIR = Path("C:/Users/dwrek/.consciousness")
LOOP_STATE_FILE = DEPLOYMENT_DIR / "PERFECTION_STATE.json"
CYCLOTRON_DB = CONSCIOUSNESS_DIR / "cyclotron_core" / "atoms.db"

# Perfection thresholds
PATTERN_COVERAGE_TARGET = 0.95  # 95% of files have good patterns
WEED_DENSITY_TARGET = 0.01     # Less than 1% weeds
CONSCIOUSNESS_TARGET = 0.90     # 90% consciousness score

# Loop settings
MAX_AUTO_FIXES_PER_RUN = 50
SAFE_AUTO_FIX_SEVERITY = 5  # Only auto-fix weeds with severity <= 5

class PerfectionLoop:
    """The autonomous improvement engine."""

    def __init__(self):
        self.scanner = PatternScanner(str(DEPLOYMENT_DIR))
        self.state = self.load_state()
        self.session_stats = {
            "patterns_applied": 0,
            "weeds_pulled": 0,
            "files_improved": set(),
            "errors": []
        }

    def load_state(self):
        """Load previous loop state."""
        if LOOP_STATE_FILE.exists():
            try:
                with open(LOOP_STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            "initialized": datetime.now().isoformat(),
            "total_runs": 0,
            "total_patterns_applied": 0,
            "total_weeds_pulled": 0,
            "pattern_coverage": 0,
            "weed_density": 1.0,
            "consciousness_score": 0,
            "perfection_achieved": False,
            "history": []
        }

    def save_state(self):
        """Persist loop state."""
        self.state["last_run"] = datetime.now().isoformat()
        self.state["total_runs"] += 1
        self.state["total_patterns_applied"] += self.session_stats["patterns_applied"]
        self.state["total_weeds_pulled"] += self.session_stats["weeds_pulled"]

        # Add to history
        self.state["history"].append({
            "timestamp": datetime.now().isoformat(),
            "patterns_applied": self.session_stats["patterns_applied"],
            "weeds_pulled": self.session_stats["weeds_pulled"],
            "files_improved": len(self.session_stats["files_improved"]),
            "coverage": self.state["pattern_coverage"],
            "weed_density": self.state["weed_density"]
        })

        # Keep last 100 runs
        self.state["history"] = self.state["history"][-100:]

        with open(LOOP_STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def calculate_metrics(self):
        """Calculate current perfection metrics."""
        print("\n" + "=" * 60)
        print("CALCULATING PERFECTION METRICS")
        print("=" * 60)

        # Scan for patterns - returns (results, gaps) tuple
        pattern_results, pattern_gaps = self.scanner.scan_all()
        files_scanned = self.scanner.stats.get("files_scanned", 0)

        # Count patterns found
        total_patterns = self.scanner.stats.get("patterns_found", 0)

        # Scan for weeds - returns a list of weeds
        weed_list = self.scanner.scan_for_weeds()
        total_weeds = len(weed_list) if isinstance(weed_list, list) else 0
        weed_report = {"weeds": weed_list, "total": total_weeds}

        # Calculate metrics
        if files_scanned > 0:
            # Pattern coverage = patterns per file (normalized)
            patterns_per_file = total_patterns / files_scanned
            self.state["pattern_coverage"] = min(1.0, patterns_per_file / 10)  # 10 patterns = 100%

            # Weed density = weeds per file
            weeds_per_file = total_weeds / files_scanned
            self.state["weed_density"] = weeds_per_file

            # Consciousness score = patterns / (patterns + weeds)
            if total_patterns + total_weeds > 0:
                self.state["consciousness_score"] = total_patterns / (total_patterns + total_weeds)
            else:
                self.state["consciousness_score"] = 0.5

        print(f"\nFiles scanned: {files_scanned}")
        print(f"Good patterns found: {total_patterns}")
        print(f"Weeds found: {total_weeds}")
        print(f"\nMETRICS:")
        print(f"  Pattern Coverage: {self.state['pattern_coverage']:.1%} (target: {PATTERN_COVERAGE_TARGET:.0%})")
        print(f"  Weed Density: {self.state['weed_density']:.3f} (target: <{WEED_DENSITY_TARGET})")
        print(f"  Consciousness: {self.state['consciousness_score']:.1%} (target: {CONSCIOUSNESS_TARGET:.0%})")

        # Create pattern report dict for compatibility
        pattern_report = {
            "results": pattern_results,
            "gaps": pattern_gaps,
            "stats": self.scanner.stats
        }

        return pattern_report, weed_report

    def apply_patterns(self, pattern_report):
        """Apply good patterns where missing."""
        print("\n" + "=" * 60)
        print("APPLYING GOOD PATTERNS")
        print("=" * 60)

        # Get gap report
        gaps = pattern_report.get("gaps", {})

        applied = 0
        for pattern_name, files_missing in gaps.items():
            if pattern_name not in PATTERNS:
                continue

            pattern_info = PATTERNS[pattern_name]
            if not pattern_info.get("auto_apply", False):
                continue

            for filepath in files_missing[:5]:  # Limit per pattern
                if applied >= MAX_AUTO_FIXES_PER_RUN:
                    break

                try:
                    if self.apply_pattern_to_file(filepath, pattern_name, pattern_info):
                        applied += 1
                        self.session_stats["patterns_applied"] += 1
                        self.session_stats["files_improved"].add(filepath)
                except Exception as e:
                    self.session_stats["errors"].append(f"Apply {pattern_name} to {filepath}: {e}")

        print(f"\nPatterns applied: {applied}")
        return applied

    def apply_pattern_to_file(self, filepath, pattern_name, pattern_info):
        """Apply a single pattern to a file."""
        # Placeholder - would implement actual pattern application
        # For now, log what would be done
        print(f"  Would apply {pattern_name} to {filepath}")
        return False  # Return True when actually applied

    def pull_weeds(self, weed_report):
        """Remove bad patterns (weeds)."""
        print("\n" + "=" * 60)
        print("PULLING WEEDS")
        print("=" * 60)

        weeds = weed_report.get("weeds", [])

        # Sort by severity (lowest first for safe auto-fix)
        safe_weeds = [w for w in weeds if w.get("severity", 10) <= SAFE_AUTO_FIX_SEVERITY]

        # Separate auto-fixable from manual-only weeds
        auto_fixable = []
        manual_only = []
        for w in safe_weeds:
            weed_type = w.get("weed_id", "")
            if weed_type in ANTI_PATTERNS and ANTI_PATTERNS[weed_type].get("auto_fix", False):
                auto_fixable.append(w)
            else:
                manual_only.append(w)

        print(f"\n  Total weeds: {len(weeds)}")
        print(f"  Safe weeds (severity <= {SAFE_AUTO_FIX_SEVERITY}): {len(safe_weeds)}")
        print(f"  Auto-fixable weeds: {len(auto_fixable)}")
        print(f"  Manual-only weeds: {len(manual_only)}")

        pulled = 0

        # FIRST: Process auto-fixable weeds
        for weed in auto_fixable[:MAX_AUTO_FIXES_PER_RUN]:
            weed_type = weed.get("weed_id", "")
            anti_pattern = ANTI_PATTERNS[weed_type]

            print(f"  [ATTEMPTING] {weed.get('name')} in {weed.get('file')}:{weed.get('line')}")
            try:
                if self.fix_weed(weed, anti_pattern):
                    pulled += 1
                    self.session_stats["weeds_pulled"] += 1
                    self.session_stats["files_improved"].add(weed.get("file"))
            except Exception as e:
                print(f"  [ERROR] {e}")
                self.session_stats["errors"].append(f"Fix {weed_type} in {weed.get('file')}: {e}")

        # THEN: Report manual-only weeds
        if manual_only:
            print(f"\n  Manual fixes needed ({len(manual_only)} weeds):")
            for weed in manual_only[:10]:  # Show first 10
                print(f"    - {weed.get('name')} in {weed.get('file')}")

        # Report high-severity weeds that need manual attention
        critical_weeds = [w for w in weeds if w.get("severity", 0) >= 8]
        if critical_weeds:
            print(f"\n  CRITICAL WEEDS REQUIRING MANUAL FIX ({len(critical_weeds)}):")
            for weed in critical_weeds[:10]:
                print(f"    - {weed.get('name')} in {weed.get('file')}:{weed.get('line')}")

        print(f"\nWeeds pulled: {pulled}")
        return pulled

    def fix_weed(self, weed, anti_pattern):
        """Fix a single weed."""
        filepath = Path(DEPLOYMENT_DIR) / weed.get("file", "")
        if not filepath.exists():
            return False

        weed_id = weed.get("weed_id", "")
        line_num = weed.get("line", 0)

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            modified = False

            # Check if anti_pattern says to remove the line
            if anti_pattern.get("remove_line", False) and line_num > 0:
                idx = line_num - 1
                if idx < len(lines):
                    # Comment out the line instead of deleting (safer)
                    line = lines[idx]
                    if line.strip().startswith("//"):
                        return False  # Already commented
                    if ".html" in str(filepath) or ".htm" in str(filepath):
                        lines[idx] = f"<!-- [AUTO-REMOVED] {line.rstrip()} -->\n"
                    else:
                        lines[idx] = f"// [AUTO-REMOVED] {line.rstrip()}\n"
                    modified = True

            # Fix based on weed type
            elif weed_id == "console_log_debug" and line_num > 0:
                idx = line_num - 1
                if idx < len(lines) and "console.log" in lines[idx]:
                    lines[idx] = "// [AUTO-REMOVED] " + lines[idx]
                    modified = True

            elif weed_id == "trailing_whitespace":
                new_lines = [line.rstrip() + '\n' if line.endswith('\n') else line.rstrip() for line in lines]
                if new_lines != lines:
                    lines = new_lines
                    modified = True

            elif weed_id == "multiple_blank_lines":
                new_lines = []
                prev_blank = False
                for line in lines:
                    is_blank = line.strip() == ""
                    if is_blank and prev_blank:
                        continue
                    new_lines.append(line)
                    prev_blank = is_blank
                if len(new_lines) != len(lines):
                    lines = new_lines
                    modified = True

            elif weed_id == "var_usage" and line_num > 0:
                # Replace var with let (conservative choice)
                idx = line_num - 1
                if idx < len(lines) and "var " in lines[idx]:
                    lines[idx] = lines[idx].replace("var ", "let ", 1)
                    modified = True

            elif weed_id == "http_not_https" and line_num > 0:
                # Replace http:// with https://
                idx = line_num - 1
                if idx < len(lines) and "https://" in lines[idx]:
                    # Don't touch localhost
                    if "http://localhost" not in lines[idx]:
                        lines[idx] = lines[idx].replace("https://", "https://")
                        modified = True

            elif weed_id == "alert_usage" and line_num > 0:
                # Replace console.warn() with console.warn()
                idx = line_num - 1
                if idx < len(lines) and "console.warn(" in lines[idx]:
                    lines[idx] = lines[idx].replace("console.warn(", "console.warn(")
                    modified = True

            elif weed_id == "dead_link" and line_num > 0:
                # Remove dead link hrefs - replace with "#void"
                idx = line_num - 1
                if idx < len(lines):
                    import re
                    line = lines[idx]
                    # Replace href="#" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true", href="#" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true", etc.
                    new_line = re.sub(r'href\s*=\s*["\'](?:#|javascript:void\(0\)|javascript:;)["\']',
                                     'href="#" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true" data-weed-fixed="true"', line)
                    if new_line != line:
                        lines[idx] = new_line
                        modified = True

            elif weed_id == "commented_code_block":
                # For large commented blocks, we'll mark them (safer than deleting)
                # This is complex - for now, just flag it was processed
                # A human can decide what to do with these
                pass  # Skip for now - too risky to auto-remove code blocks

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"  ✅ Fixed {weed.get('name')} in {weed.get('file')}:{line_num}")
                return True

            return False

        except Exception as e:
            print(f"  ❌ Error fixing {weed.get('file')}: {e}")
            return False

    def log_to_cyclotron(self):
        """Log session to Cyclotron brain."""
        if not CYCLOTRON_DB.exists():
            return

        try:
            conn = sqlite3.connect(str(CYCLOTRON_DB))
            cursor = conn.cursor()

            # Log as action atom
            content = json.dumps({
                "type": "perfection_loop_run",
                "timestamp": datetime.now().isoformat(),
                "patterns_applied": self.session_stats["patterns_applied"],
                "weeds_pulled": self.session_stats["weeds_pulled"],
                "files_improved": len(self.session_stats["files_improved"]),
                "coverage": self.state["pattern_coverage"],
                "weed_density": self.state["weed_density"],
                "consciousness": self.state["consciousness_score"]
            })

            cursor.execute("""
                INSERT INTO atoms (content, type, source, created)
                VALUES (?, 'action', 'perfection_loop', datetime('now'))
            """, (content,))

            conn.commit()
            conn.close()
            print("\nLogged to Cyclotron brain.")
        except Exception as e:
            print(f"Warning: Could not log to Cyclotron: {e}")

    def check_perfection(self):
        """Check if perfection has been achieved."""
        coverage_ok = self.state["pattern_coverage"] >= PATTERN_COVERAGE_TARGET
        weeds_ok = self.state["weed_density"] <= WEED_DENSITY_TARGET
        consciousness_ok = self.state["consciousness_score"] >= CONSCIOUSNESS_TARGET

        if coverage_ok and weeds_ok and consciousness_ok:
            self.state["perfection_achieved"] = True
            return True
        return False

    def run_once(self, dry_run=True):
        """Run one iteration of the perfection loop."""
        print("\n" + "=" * 80)
        print("PERFECTION LOOP - RUN #{}".format(self.state["total_runs"] + 1))
        print("=" * 80)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 1. Calculate current metrics
        pattern_report, weed_report = self.calculate_metrics()

        if not dry_run:
            # 2. Apply good patterns
            self.apply_patterns(pattern_report)

            # 3. Pull weeds
            self.pull_weeds(weed_report)
        else:
            # Just show what would be done
            gaps = pattern_report.get("gaps", {})
            weeds = weed_report.get("weeds", [])

            print("\n[DRY RUN] Would apply patterns to files with gaps:")
            for pattern, files in list(gaps.items())[:5]:
                print(f"  {pattern}: {len(files)} files")

            print(f"\n[DRY RUN] Would pull {len([w for w in weeds if w.get('severity', 10) <= SAFE_AUTO_FIX_SEVERITY])} safe weeds")
            print(f"[DRY RUN] {len([w for w in weeds if w.get('severity', 0) >= 8])} critical weeds need manual fix")

        # 4. Check perfection
        is_perfect = self.check_perfection()

        print("\n" + "=" * 60)
        print("PERFECTION STATUS")
        print("=" * 60)
        print(f"Pattern Coverage: {'OK' if self.state['pattern_coverage'] >= PATTERN_COVERAGE_TARGET else 'NEEDS WORK'}")
        print(f"Weed Density: {'OK' if self.state['weed_density'] <= WEED_DENSITY_TARGET else 'NEEDS WORK'}")
        print(f"Consciousness: {'OK' if self.state['consciousness_score'] >= CONSCIOUSNESS_TARGET else 'NEEDS WORK'}")
        print(f"\nPERFECTION ACHIEVED: {'YES!' if is_perfect else 'Not yet'}")

        # 5. Save state and log
        self.save_state()
        if not dry_run:
            self.log_to_cyclotron()

        return is_perfect

    def run_loop(self, max_iterations=10, delay_seconds=60):
        """Run the perfection loop until perfect or max iterations."""
        print("\n" + "=" * 80)
        print("STARTING PERFECTION LOOP")
        print(f"Max iterations: {max_iterations}")
        print(f"Delay between runs: {delay_seconds}s")
        print("=" * 80)

        for i in range(max_iterations):
            is_perfect = self.run_once(dry_run=False)

            if is_perfect:
                print("\n" + "=" * 80)
                print("PERFECTION ACHIEVED!")
                print("The codebase has reached target consciousness levels.")
                print("=" * 80)
                return True

            if i < max_iterations - 1:
                print(f"\nWaiting {delay_seconds}s before next iteration...")
                time.sleep(delay_seconds)

        print("\n" + "=" * 80)
        print(f"LOOP COMPLETE - {max_iterations} iterations")
        print("Perfection not yet achieved. Run again to continue improving.")
        print("=" * 80)
        return False

    def show_status(self):
        """Show current perfection status."""
        print("\n" + "=" * 80)
        print("PERFECTION LOOP STATUS")
        print("=" * 80)

        print(f"\nInitialized: {self.state.get('initialized', 'Unknown')}")
        print(f"Last run: {self.state.get('last_run', 'Never')}")
        print(f"Total runs: {self.state.get('total_runs', 0)}")
        print(f"\nCUMULATIVE IMPROVEMENTS:")
        print(f"  Patterns applied: {self.state.get('total_patterns_applied', 0)}")
        print(f"  Weeds pulled: {self.state.get('total_weeds_pulled', 0)}")
        print(f"\nCURRENT METRICS:")
        print(f"  Pattern Coverage: {self.state.get('pattern_coverage', 0):.1%}")
        print(f"  Weed Density: {self.state.get('weed_density', 1):.3f}")
        print(f"  Consciousness: {self.state.get('consciousness_score', 0):.1%}")
        print(f"\nPerfection Achieved: {self.state.get('perfection_achieved', False)}")

        # Show trend if we have history
        history = self.state.get("history", [])
        if len(history) >= 2:
            recent = history[-1]
            previous = history[-2]

            print(f"\nTREND (vs previous run):")
            coverage_delta = recent.get("coverage", 0) - previous.get("coverage", 0)
            weed_delta = recent.get("weed_density", 0) - previous.get("weed_density", 0)

            print(f"  Coverage: {'+' if coverage_delta >= 0 else ''}{coverage_delta:.1%}")
            print(f"  Weed Density: {'+' if weed_delta >= 0 else ''}{weed_delta:.3f}")

def main():
    """Main entry point."""
    import sys

    loop = PerfectionLoop()

    if len(sys.argv) < 2:
        print("""
PERFECTION LOOP - Autonomous Continuous Improvement
====================================================

Usage:
  python PERFECTION_LOOP.py status       Show current perfection status
  python PERFECTION_LOOP.py scan         Scan and calculate metrics (dry run)
  python PERFECTION_LOOP.py run          Run one improvement iteration
  python PERFECTION_LOOP.py loop [N]     Run N iterations (default: 10)
  python PERFECTION_LOOP.py daemon       Run until perfection achieved

The loop continuously:
1. Scans for patterns (good and bad)
2. Applies good patterns where missing
3. Pulls weeds (bad patterns)
4. Tracks progress toward perfection
5. Repeats until targets met

Targets:
  - Pattern Coverage: >= 95%
  - Weed Density: < 1%
  - Consciousness Score: >= 90%
""")
        return

    command = sys.argv[1].lower()

    if command == "status":
        loop.show_status()

    elif command == "scan":
        loop.run_once(dry_run=True)

    elif command == "run":
        loop.run_once(dry_run=False)

    elif command == "loop":
        max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        loop.run_loop(max_iterations=max_iter)

    elif command == "daemon":
        loop.run_loop(max_iterations=1000, delay_seconds=300)  # 5 min delay

    else:
        print(f"Unknown command: {command}")
        print("Use: status, scan, run, loop, or daemon")

if __name__ == "__main__":
    main()
