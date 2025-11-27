#!/usr/bin/env python3
"""SELF_HEALING_SYSTEM.py - Auto detection and recovery from system issues."""

import json; import shutil; import subprocess
from pathlib import Path
from datetime import datetime, timedelta

try: from CYCLOTRON_BRAIN_BRIDGE import CyclotronBridge
except: CyclotronBridge = None

HOME = Path.home()
CONSCIOUSNESS, DEPLOYMENT, PLANNING = HOME / ".consciousness", HOME / "100X_DEPLOYMENT", HOME / ".planning"
HEALING_LOG = CONSCIOUSNESS / "healing_log.json"

class HealthCheck:
    def __init__(self, name: str, check_fn, heal_fn, severity: str = "warning"):
        self.name, self.check_fn, self.heal_fn, self.severity = name, check_fn, heal_fn, severity
        self.last_check, self.last_heal, self.heal_count = None, None, 0

class SelfHealingSystem:
    def __init__(self):
        self.cyclotron = CyclotronBridge() if CyclotronBridge else None
        self.checks, self.healing_log = [], []
        self._register_checks()

    def _register_checks(self):
        checks = [("cyclotron_index", self._check_cyclotron_index, self._heal_cyclotron_index, "critical"),
                  ("consciousness_dirs", self._check_consciousness_dirs, self._heal_consciousness_dirs, "critical"),
                  ("planning_dirs", self._check_planning_dirs, self._heal_planning_dirs, "critical"),
                  ("stale_data", self._check_stale_data, self._heal_stale_data, "warning"),
                  ("disk_space", self._check_disk_space, self._heal_disk_space, "warning"),
                  ("orphan_files", self._check_orphan_files, self._heal_orphan_files, "warning"),
                  ("git_status", self._check_git_status, self._heal_git_status, "info"),
                  ("json_validity", self._check_json_validity, self._heal_json_validity, "warning")]
        self.checks = [HealthCheck(n, c, h, s) for n, c, h, s in checks]

    def _check_cyclotron_index(self) -> tuple:
        ix = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if not ix.exists(): return False, "Cyclotron index missing"
        try:
            data = json.load(open(ix))
            return (True, f"Index OK: {len(data.get('atoms', []))} atoms") if "atoms" in data else (False, "Index corrupted")
        except: return False, "Index invalid JSON"

    def _heal_cyclotron_index(self) -> tuple:
        ap = CONSCIOUSNESS / "cyclotron_core" / "atoms"; ap.mkdir(parents=True, exist_ok=True)
        atoms, tags, types = [], {}, {}
        for f in ap.glob("*.json"):
            try:
                a = json.load(open(f))
                atoms.append({"id": a["id"], "preview": a["content"][:100], "type": a.get("type", "fact"), "tags": a.get("tags", [])})
                for t in a.get("tags", []): tags.setdefault(t, []).append(a["id"])
                types.setdefault(a.get("type", "fact"), []).append(a["id"])
            except: continue
        ix = {"atoms": atoms, "tags": tags, "types": types, "stats": {"total": len(atoms), "by_type": {t: len(i) for t, i in types.items()}}, "updated": datetime.now().isoformat()}
        json.dump(ix, open(CONSCIOUSNESS / "cyclotron_core" / "INDEX.json", 'w'), indent=2)
        return True, f"Rebuilt index: {len(atoms)} atoms"

    def _check_consciousness_dirs(self) -> tuple:
        missing = [d for d in ["brain", "agents", "memory", "cyclotron_core"] if not (CONSCIOUSNESS / d).exists()]
        return (False, f"Missing: {missing}") if missing else (True, "Dirs OK")

    def _heal_consciousness_dirs(self) -> tuple:
        created = []
        for d in ["brain", "agents", "memory", "cyclotron_core", "cyclotron_core/atoms", "task_queue", "task_results"]:
            p = CONSCIOUSNESS / d
            if not p.exists(): p.mkdir(parents=True); created.append(d)
        return True, f"Created: {created}"

    def _check_planning_dirs(self) -> tuple:
        missing = [d for d in ["traction"] if not (PLANNING / d).exists()]
        return (False, f"Missing: {missing}") if missing else (True, "Planning OK")

    def _heal_planning_dirs(self) -> tuple:
        created = []
        for d in ["traction", "archives", "projections"]:
            p = PLANNING / d
            if not p.exists(): p.mkdir(parents=True); created.append(d)
        return True, f"Created: {created}"

    def _check_stale_data(self) -> tuple:
        stale = [p.name for p in [PLANNING/"traction"/"SCORECARD_WEEKLY.json", CONSCIOUSNESS/"session_state.json", CONSCIOUSNESS/"cyclotron_core"/"INDEX.json"]
                 if p.exists() and datetime.now() - datetime.fromtimestamp(p.stat().st_mtime) > timedelta(days=7)]
        return (False, f"Stale: {stale}") if stale else (True, "No stale files")

    def _heal_stale_data(self) -> tuple: return True, "Flagged for regeneration"

    def _check_disk_space(self) -> tuple:
        try:
            u = shutil.disk_usage(HOME); pct = (u.used / u.total) * 100; free = u.free / (1024**3)
            return (False, f"Disk {pct:.1f}% ({free:.1f}GB)") if pct > 90 else (True, f"Disk OK: {pct:.1f}%")
        except Exception as e: return False, f"Disk check failed: {e}"

    def _heal_disk_space(self) -> tuple:
        cleaned = 0
        for path, pattern, keep in [(CONSCIOUSNESS/"agents", "state_*.json", 50), (CONSCIOUSNESS/"task_results", "result_*.json", 100)]:
            if path.exists():
                for f in sorted(path.glob(pattern))[:-keep]: f.unlink(); cleaned += 1
        return True, f"Cleaned {cleaned} files"

    def _check_orphan_files(self) -> tuple:
        ap, ix = CONSCIOUSNESS/"cyclotron_core"/"atoms", CONSCIOUSNESS/"cyclotron_core"/"INDEX.json"
        if ap.exists() and ix.exists():
            indexed = {a["id"] for a in json.load(open(ix)).get("atoms", [])}
            orphans = [f.stem for f in ap.glob("*.json") if f.stem not in indexed]
            if orphans: return False, f"{len(orphans)} orphan atoms"
        return True, "No orphans"

    def _heal_orphan_files(self) -> tuple: self._heal_cyclotron_index(); return True, "Re-indexed"

    def _check_git_status(self) -> tuple:
        try:
            r = subprocess.run(["git", "-C", str(DEPLOYMENT), "status", "--porcelain"], capture_output=True, text=True)
            n = len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0
            return (False, f"{n} changes") if n > 50 else (True, f"{n} changes")
        except Exception as e: return False, f"Git error: {e}"

    def _heal_git_status(self) -> tuple: return True, "Logged (commit manually)"

    def _check_json_validity(self) -> tuple:
        invalid = []
        for p in [CONSCIOUSNESS/"cyclotron_core"/"INDEX.json", PLANNING/"traction"/"SCORECARD_WEEKLY.json", PLANNING/"traction"/"ROCKS_Q4_2025.json"]:
            if p.exists():
                try: json.load(open(p))
                except: invalid.append(p.name)
        return (False, f"Invalid: {invalid}") if invalid else (True, "JSON OK")

    def _heal_json_validity(self) -> tuple:
        healed = []
        for p, d in [(CONSCIOUSNESS/"cyclotron_core"/"INDEX.json", {"atoms": [], "tags": {}, "types": {}, "stats": {"total": 0}})]:
            if p.exists():
                try: json.load(open(p))
                except: shutil.copy(p, p.with_suffix(".json.bak")); json.dump(d, open(p, 'w'), indent=2); healed.append(p.name)
        return True, f"Healed: {healed}" if healed else "No healing needed"

    # === MAIN METHODS ===

    def run_checks(self) -> dict:
        """Run all health checks."""
        results = {"healthy": [], "unhealthy": [], "timestamp": datetime.now().isoformat()}
        for check in self.checks:
            healthy, message = check.check_fn(); check.last_check = datetime.now().isoformat()
            r = {"name": check.name, "severity": check.severity, "healthy": healthy, "message": message}
            results["healthy" if healthy else "unhealthy"].append(r)
        return results

    def heal(self, check_name: str = None) -> dict:
        """Heal specific or all unhealthy checks."""
        healed = []
        for check in self.checks:
            if check_name and check.name != check_name: continue
            healthy, _ = check.check_fn()
            if not healthy:
                success, message = check.heal_fn(); check.last_heal = datetime.now().isoformat(); check.heal_count += 1
                healed.append({"name": check.name, "success": success, "message": message})
                if self.cyclotron: self.cyclotron.create_atom(f"Healed: {check.name} - {message}", atom_type="action", source="self_healing", tags=["healing", check.severity, "automated"])
        self._save_healing_log(healed); return {"healed": healed}

    def auto_heal(self) -> dict:
        """Run checks and heal all issues."""
        print("=" * 60 + "\nSELF-HEALING SYSTEM\n" + "=" * 60)
        cr = self.run_checks()
        print(f"\nHealth Check: {len(cr['healthy'])} healthy, {len(cr['unhealthy'])} unhealthy")
        if cr['unhealthy']:
            for r in cr['unhealthy']: print(f"  [{r['severity'].upper()}] {r['name']}: {r['message']}")
            print("\nHealing..."); hr = self.heal()
            for r in hr['healed']: print(f"  {'OK' if r['success'] else 'FAIL'} {r['name']}: {r['message']}")
            return {"checks": cr, "healing": hr}
        print("\nAll systems healthy!"); return {"checks": cr, "healing": {"healed": []}}

    def _save_healing_log(self, healed: list):
        self.healing_log.extend(healed)
        json.dump({"log": self.healing_log[-100:], "updated": datetime.now().isoformat()}, open(HEALING_LOG, 'w'), indent=2)

    def get_status(self) -> dict:
        """Get system health status."""
        checks = self.run_checks()
        return {"total_checks": len(self.checks), "healthy": len(checks["healthy"]), "unhealthy": len(checks["unhealthy"]),
                "critical_issues": [r for r in checks["unhealthy"] if r["severity"] == "critical"],
                "warnings": [r for r in checks["unhealthy"] if r["severity"] == "warning"]}


def main():
    """CLI for self-healing system."""
    import sys; healer = SelfHealingSystem()
    if len(sys.argv) < 2:
        print("Self-Healing System\n" + "=" * 40 + "\nCommands: check, heal, auto, status"); return
    cmd = sys.argv[1]
    if cmd == "check":
        r = healer.run_checks(); print(f"\nHealthy: {len(r['healthy'])}")
        for x in r['healthy']: print(f"  OK {x['name']}: {x['message']}")
        print(f"\nUnhealthy: {len(r['unhealthy'])}")
        for x in r['unhealthy']: print(f"  FAIL [{x['severity']}] {x['name']}: {x['message']}")
    elif cmd == "heal":
        for r in healer.heal()['healed']: print(f"{'OK' if r['success'] else 'FAIL'} {r['name']}: {r['message']}")
    elif cmd == "auto": healer.auto_heal()
    elif cmd == "status":
        s = healer.get_status(); print(f"\nHealth: {s['healthy']}/{s['total_checks']} passing")
        if s['critical_issues']: print(f"Critical: {len(s['critical_issues'])}")
        if s['warnings']: print(f"Warnings: {len(s['warnings'])}")
    else: print(f"Unknown: {cmd}")

if __name__ == "__main__": main()
