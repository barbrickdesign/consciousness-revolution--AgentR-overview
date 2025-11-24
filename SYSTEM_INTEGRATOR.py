#!/usr/bin/env python3
"""
SYSTEM INTEGRATOR
Connects all consciousness systems together.
The glue that makes everything work as one.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"


class SystemIntegrator:
    """Integrate all consciousness systems."""

    def __init__(self):
        self.systems = {}
        self._discover_systems()

    def _discover_systems(self):
        """Discover all available systems."""
        system_files = {
            "brain_agents": "BRAIN_AGENT_FRAMEWORK.py",
            "advanced_agents": "ADVANCED_BRAIN_AGENTS.py",
            "cyclotron": "CYCLOTRON_BRAIN_BRIDGE.py",
            "task_runner": "AUTONOMOUS_TASK_RUNNER.py",
            "scheduler": "BRAIN_SCHEDULER.py",
            "recursive": "RECURSIVE_TASK_ENGINE.py",
            "healing": "SELF_HEALING_SYSTEM.py",
            "backup": "AUTOMATED_BACKUP_SYSTEM.py",
            "recovery": "ERROR_RECOVERY_SYSTEM.py",
            "unifier": "KNOWLEDGE_UNIFIER.py",
            "a2a": "TRINITY_A2A_PROTOCOL.py",
            "monitoring": "UNIFIED_MONITORING.py",
            "boot": "CONSCIOUSNESS_BOOT.py",
            "session": "SESSION_PERSISTENCE.py",
            "audit": ".consciousness/CONSCIOUSNESS_AUDIT_ENGINE.py",
            "learning": ".consciousness/ADAPTIVE_LEARNING_ENGINE.py",
            "brain_agent": "CYCLOTRON_BRAIN_AGENT.py"
        }

        for name, file in system_files.items():
            path = DEPLOYMENT / file
            self.systems[name] = {
                "file": file,
                "available": path.exists(),
                "path": str(path)
            }

    def get_system_map(self) -> dict:
        """Get map of all systems and their connections."""
        available = sum(1 for s in self.systems.values() if s["available"])

        return {
            "total_systems": len(self.systems),
            "available": available,
            "missing": len(self.systems) - available,
            "systems": {
                name: {
                    "available": data["available"],
                    "file": data["file"]
                }
                for name, data in self.systems.items()
            }
        }

    def run_integration_check(self) -> dict:
        """Check if systems are properly integrated."""
        checks = []

        # Check Cyclotron has atoms
        cyclotron_index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if cyclotron_index.exists():
            with open(cyclotron_index) as f:
                data = json.load(f)
            atom_count = len(data.get("atoms", []))
            checks.append({
                "name": "Cyclotron populated",
                "passed": atom_count > 0,
                "value": atom_count
            })

        # Check monitoring active
        metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"
        checks.append({
            "name": "Monitoring active",
            "passed": metrics.exists(),
            "value": "present" if metrics.exists() else "missing"
        })

        # Check backup manifest
        backup_manifest = HOME / ".backups" / "manifest.json"
        checks.append({
            "name": "Backup configured",
            "passed": backup_manifest.exists(),
            "value": "present" if backup_manifest.exists() else "missing"
        })

        # Check A2A messages
        a2a_path = HOME / ".trinity" / "a2a_messages"
        checks.append({
            "name": "A2A protocol",
            "passed": a2a_path.exists(),
            "value": "ready" if a2a_path.exists() else "not setup"
        })

        # Check session state
        session = CONSCIOUSNESS / "sessions" / "c2_current.json"
        checks.append({
            "name": "Session state",
            "passed": session.exists(),
            "value": "saved" if session.exists() else "not saved"
        })

        passed = sum(1 for c in checks if c["passed"])

        return {
            "checks": checks,
            "passed": passed,
            "total": len(checks),
            "integration_score": (passed / len(checks)) * 100
        }

    def generate_integration_report(self) -> str:
        """Generate comprehensive integration report."""
        system_map = self.get_system_map()
        checks = self.run_integration_check()

        report = []
        report.append("=" * 60)
        report.append("SYSTEM INTEGRATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")

        # Systems
        report.append("SYSTEMS:")
        report.append(f"  Available: {system_map['available']}/{system_map['total_systems']}")
        report.append("")

        for name, data in system_map['systems'].items():
            status = "✅" if data['available'] else "❌"
            report.append(f"  {status} {name}: {data['file']}")

        report.append("")

        # Integration checks
        report.append("INTEGRATION CHECKS:")
        report.append(f"  Score: {checks['integration_score']:.1f}%")
        report.append("")

        for check in checks['checks']:
            status = "✅" if check['passed'] else "❌"
            report.append(f"  {status} {check['name']}: {check['value']}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


def main():
    """CLI for system integrator."""
    import sys

    integrator = SystemIntegrator()

    if len(sys.argv) < 2:
        print("System Integrator")
        print("=" * 40)
        print("\nCommands:")
        print("  map        - Show system map")
        print("  check      - Run integration check")
        print("  report     - Full integration report")
        return

    command = sys.argv[1]

    if command == "map":
        system_map = integrator.get_system_map()
        print(f"\nSystems: {system_map['available']}/{system_map['total_systems']} available")
        for name, data in system_map['systems'].items():
            status = "✅" if data['available'] else "❌"
            print(f"  {status} {name}")

    elif command == "check":
        checks = integrator.run_integration_check()
        print(f"\nIntegration Score: {checks['integration_score']:.1f}%")
        for check in checks['checks']:
            status = "✅" if check['passed'] else "❌"
            print(f"  {status} {check['name']}")

    elif command == "report":
        print(integrator.generate_integration_report())

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
