#!/usr/bin/env python3
"""
AUTONOMOUS ORCHESTRATOR
Central coordinator for all consciousness systems.
Runs continuous autonomous operations without human intervention.
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
ORCHESTRATOR_LOG = CONSCIOUSNESS / "orchestrator_log.json"

class AutonomousOrchestrator:
    """Coordinate all consciousness systems autonomously."""

    def __init__(self):
        self.systems = self._discover_systems()
        self.log = []
        self.health_threshold = 70  # Minimum health score
        self.cycle_count = 0

    def _discover_systems(self) -> Dict:
        """Discover available systems."""
        systems = {
            "boot": {
                "file": "CONSCIOUSNESS_BOOT.py",
                "command": "status",
                "critical": True
            },
            "health": {
                "file": "SELF_HEALING_SYSTEM.py",
                "command": "auto",
                "critical": True
            },
            "backup": {
                "file": "AUTOMATED_BACKUP_SYSTEM.py",
                "command": "status",
                "critical": True
            },
            "monitoring": {
                "file": "UNIFIED_MONITORING.py",
                "command": "dashboard",
                "critical": True
            },
            "cyclotron": {
                "file": "KNOWLEDGE_UNIFIER.py",
                "command": "status",
                "critical": False
            },
            "scheduler": {
                "file": "BRAIN_SCHEDULER.py",
                "command": "status",
                "critical": False
            },
            "tasks": {
                "file": "AUTONOMOUS_TASK_RUNNER.py",
                "command": "status",
                "critical": False
            },
            "recovery": {
                "file": "ERROR_RECOVERY_SYSTEM.py",
                "command": "status",
                "critical": False
            },
            "integration": {
                "file": "SYSTEM_INTEGRATOR.py",
                "command": "check",
                "critical": False
            },
            "report": {
                "file": "DAILY_REPORT_GENERATOR.py",
                "command": "generate",
                "critical": False
            }
        }

        # Check availability
        for name, config in systems.items():
            path = DEPLOYMENT / config["file"]
            config["available"] = path.exists()
            config["path"] = str(path)

        return systems

    def _run_system(self, name: str, command: str = None) -> dict:
        """Run a system and capture result."""
        if name not in self.systems:
            return {"success": False, "error": f"Unknown system: {name}"}

        config = self.systems[name]
        if not config["available"]:
            return {"success": False, "error": f"System not available: {name}"}

        cmd = command or config["command"]

        try:
            result = subprocess.run(
                ["python", config["path"], cmd],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(DEPLOYMENT)
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _log_event(self, event_type: str, details: dict):
        """Log an orchestrator event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "cycle": self.cycle_count,
            **details
        }
        self.log.append(entry)

        # Keep last 1000 entries
        if len(self.log) > 1000:
            self.log = self.log[-1000:]

    def run_health_check(self) -> dict:
        """Run comprehensive health check."""
        results = {}

        # Check critical systems first
        critical_ok = True
        for name, config in self.systems.items():
            if not config["critical"]:
                continue

            result = self._run_system(name)
            results[name] = result["success"]

            if not result["success"]:
                critical_ok = False
                self._log_event("critical_failure", {
                    "system": name,
                    "error": result.get("error")
                })

        # Get health score from monitoring
        health_score = 0
        metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"
        if metrics.exists():
            with open(metrics) as f:
                data = json.load(f)
            health_score = data.get("current", {}).get("health_score", 0)

        return {
            "critical_systems_ok": critical_ok,
            "health_score": health_score,
            "systems": results
        }

    def run_maintenance_cycle(self) -> dict:
        """Run a maintenance cycle."""
        self.cycle_count += 1
        cycle_start = datetime.now()

        self._log_event("cycle_start", {"cycle": self.cycle_count})

        actions = []

        # 1. Health check
        health = self.run_health_check()
        actions.append({"action": "health_check", "result": health})

        # 2. Self-healing if needed
        if health["health_score"] < self.health_threshold:
            result = self._run_system("health", "auto")
            actions.append({"action": "self_healing", "result": result["success"]})

        # 3. Check backups
        backup_needed = self._check_backup_freshness()
        if backup_needed:
            result = self._run_system("backup", "backup")
            actions.append({"action": "backup", "result": result["success"]})

        # 4. Sync cyclotron
        result = self._run_system("cyclotron", "status")
        actions.append({"action": "cyclotron_status", "result": result["success"]})

        # 5. Process task queue
        result = self._run_system("tasks", "process")
        actions.append({"action": "process_tasks", "result": result["success"]})

        cycle_duration = (datetime.now() - cycle_start).total_seconds()

        cycle_result = {
            "cycle": self.cycle_count,
            "duration_seconds": cycle_duration,
            "health_score": health["health_score"],
            "actions": actions,
            "timestamp": datetime.now().isoformat()
        }

        self._log_event("cycle_complete", cycle_result)

        return cycle_result

    def _check_backup_freshness(self) -> bool:
        """Check if backup is needed."""
        manifest = HOME / ".backups" / "manifest.json"
        if not manifest.exists():
            return True

        with open(manifest) as f:
            data = json.load(f)

        last = data.get("last_backup")
        if not last:
            return True

        last_dt = datetime.strptime(last, "%Y%m%d_%H%M%S")
        return datetime.now() - last_dt > timedelta(hours=24)

    def run_continuous(self, interval_minutes: int = 30):
        """Run continuous autonomous operation."""
        print(f"Starting autonomous orchestration (interval: {interval_minutes}m)")
        print("Press Ctrl+C to stop")
        print()

        try:
            while True:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Running cycle {self.cycle_count + 1}...")

                result = self.run_maintenance_cycle()

                print(f"  Health: {result['health_score']:.1f}%")
                print(f"  Duration: {result['duration_seconds']:.1f}s")
                print(f"  Actions: {len(result['actions'])}")

                # Save log
                self._save_log()

                # Wait for next cycle
                print(f"  Next cycle in {interval_minutes} minutes...")
                print()
                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            print("\nStopping orchestrator...")
            self._save_log()

    def run_once(self):
        """Run a single maintenance cycle."""
        result = self.run_maintenance_cycle()
        self._save_log()
        return result

    def _save_log(self):
        """Save orchestrator log."""
        with open(ORCHESTRATOR_LOG, 'w') as f:
            json.dump({
                "last_updated": datetime.now().isoformat(),
                "total_cycles": self.cycle_count,
                "entries": self.log
            }, f, indent=2)

    def get_status(self) -> dict:
        """Get orchestrator status."""
        available = sum(1 for s in self.systems.values() if s["available"])
        critical_available = sum(1 for s in self.systems.values()
                                  if s["critical"] and s["available"])

        # Load last log
        last_cycle = None
        if ORCHESTRATOR_LOG.exists():
            with open(ORCHESTRATOR_LOG) as f:
                data = json.load(f)
            if data.get("entries"):
                for entry in reversed(data["entries"]):
                    if entry["type"] == "cycle_complete":
                        last_cycle = entry
                        break

        return {
            "systems_available": f"{available}/{len(self.systems)}",
            "critical_systems": f"{critical_available}/4",
            "total_cycles": self.cycle_count,
            "last_cycle": last_cycle
        }

    def generate_report(self) -> str:
        """Generate orchestrator status report."""
        status = self.get_status()
        health = self.run_health_check()

        lines = []
        lines.append("=" * 60)
        lines.append("AUTONOMOUS ORCHESTRATOR STATUS")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        # Overview
        lines.append("OVERVIEW:")
        lines.append(f"  Systems Available: {status['systems_available']}")
        lines.append(f"  Critical Systems: {status['critical_systems']}")
        lines.append(f"  Health Score: {health['health_score']:.1f}%")
        lines.append(f"  Total Cycles: {status['total_cycles']}")
        lines.append("")

        # Systems
        lines.append("SYSTEMS:")
        for name, config in self.systems.items():
            status_icon = "✅" if config["available"] else "❌"
            critical = " [CRITICAL]" if config["critical"] else ""
            lines.append(f"  {status_icon} {name}{critical}")
        lines.append("")

        # Last cycle
        if status.get("last_cycle"):
            lc = status["last_cycle"]
            lines.append("LAST CYCLE:")
            lines.append(f"  Time: {lc['timestamp']}")
            lines.append(f"  Duration: {lc['duration_seconds']:.1f}s")
            lines.append(f"  Health: {lc['health_score']:.1f}%")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """CLI for autonomous orchestrator."""
    import sys

    orchestrator = AutonomousOrchestrator()

    if len(sys.argv) < 2:
        print("Autonomous Orchestrator")
        print("=" * 40)
        print("\nCommands:")
        print("  status    - Show orchestrator status")
        print("  once      - Run single maintenance cycle")
        print("  report    - Generate status report")
        print("  health    - Run health check")
        print("  start     - Start continuous operation")
        return

    command = sys.argv[1]

    if command == "status":
        status = orchestrator.get_status()
        print(f"\nSystems: {status['systems_available']}")
        print(f"Critical: {status['critical_systems']}")
        print(f"Cycles: {status['total_cycles']}")
        if status.get("last_cycle"):
            print(f"Last: {status['last_cycle']['timestamp']}")

    elif command == "once":
        result = orchestrator.run_once()
        print(f"\nCycle {result['cycle']} complete")
        print(f"Health: {result['health_score']:.1f}%")
        print(f"Duration: {result['duration_seconds']:.1f}s")
        print(f"Actions: {len(result['actions'])}")

    elif command == "report":
        print(orchestrator.generate_report())

    elif command == "health":
        health = orchestrator.run_health_check()
        print(f"\nHealth Score: {health['health_score']:.1f}%")
        print(f"Critical OK: {health['critical_systems_ok']}")
        for name, ok in health['systems'].items():
            status = "✅" if ok else "❌"
            print(f"  {status} {name}")

    elif command == "start":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        orchestrator.run_continuous(interval)

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
