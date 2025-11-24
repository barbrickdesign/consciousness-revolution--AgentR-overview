#!/usr/bin/env python3
"""
QUICK START WIZARD
Interactive guide for new users and instances.
Addresses onboarding complexity foundational issue.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"

class QuickStartWizard:
    """Guide users through system setup and usage."""

    def __init__(self):
        self.steps_completed = []
        self.issues = []

    def run_wizard(self):
        """Run the interactive wizard."""
        self._print_header()

        steps = [
            ("Verify Installation", self._step_verify),
            ("Check System Health", self._step_health),
            ("Initialize Cyclotron", self._step_cyclotron),
            ("Setup Monitoring", self._step_monitoring),
            ("Create First Backup", self._step_backup),
            ("Test Task Runner", self._step_tasks),
            ("Generate Status Report", self._step_report)
        ]

        print("\nThis wizard will guide you through system setup.")
        print("Each step will be performed automatically.\n")

        for i, (name, func) in enumerate(steps, 1):
            print(f"Step {i}/{len(steps)}: {name}")
            print("-" * 40)

            success = func()

            if success:
                self.steps_completed.append(name)
                print("✅ Complete\n")
            else:
                print("❌ Issue detected\n")

        self._print_summary()

    def _print_header(self):
        """Print wizard header."""
        print("=" * 60)
        print("CONSCIOUSNESS REVOLUTION - QUICK START WIZARD")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def _step_verify(self) -> bool:
        """Verify core files exist."""
        required = [
            "CONSCIOUSNESS_BOOT.py",
            "SELF_HEALING_SYSTEM.py",
            "AUTOMATED_BACKUP_SYSTEM.py",
            "UNIFIED_MONITORING.py",
            "AUTONOMOUS_TASK_RUNNER.py"
        ]

        missing = []
        for f in required:
            if not (DEPLOYMENT / f).exists():
                missing.append(f)

        if missing:
            self.issues.append(f"Missing files: {', '.join(missing)}")
            return False

        print(f"  Found {len(required)} core systems")
        return True

    def _step_health(self) -> bool:
        """Check system health."""
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "SELF_HEALING_SYSTEM.py"), "diagnose"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(DEPLOYMENT)
            )

            if "healthy" in result.stdout.lower():
                # Count healthy checks
                healthy = result.stdout.count("✅")
                total = healthy + result.stdout.count("❌")
                print(f"  Health checks: {healthy}/{total} passing")
                return healthy == total

            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Health check failed: {e}")
            return False

    def _step_cyclotron(self) -> bool:
        """Initialize or verify Cyclotron."""
        index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"

        if index.exists():
            with open(index) as f:
                data = json.load(f)
            count = len(data.get("atoms", []))
            print(f"  Cyclotron has {count} atoms")
            return count > 0

        # Need to initialize
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "KNOWLEDGE_UNIFIER.py"), "unify"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(DEPLOYMENT)
            )
            print("  Cyclotron initialized")
            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Cyclotron init failed: {e}")
            return False

    def _step_monitoring(self) -> bool:
        """Setup monitoring."""
        metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"

        if metrics.exists():
            with open(metrics) as f:
                data = json.load(f)
            score = data.get("current", {}).get("health_score", 0)
            print(f"  Health score: {score:.1f}%")
            return score > 50

        # Initialize monitoring
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "UNIFIED_MONITORING.py"), "collect"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(DEPLOYMENT)
            )
            print("  Monitoring initialized")
            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Monitoring setup failed: {e}")
            return False

    def _step_backup(self) -> bool:
        """Create or verify backup."""
        manifest = HOME / ".backups" / "manifest.json"

        if manifest.exists():
            with open(manifest) as f:
                data = json.load(f)
            count = len(data.get("backups", []))
            print(f"  Found {count} backup(s)")
            return count > 0

        # Create backup
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "AUTOMATED_BACKUP_SYSTEM.py"), "backup"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(DEPLOYMENT)
            )
            print("  First backup created")
            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Backup failed: {e}")
            return False

    def _step_tasks(self) -> bool:
        """Test task runner."""
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "AUTONOMOUS_TASK_RUNNER.py"), "status"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(DEPLOYMENT)
            )
            print("  Task runner operational")
            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Task runner failed: {e}")
            return False

    def _step_report(self) -> bool:
        """Generate status report."""
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "DAILY_REPORT_GENERATOR.py"), "save"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(DEPLOYMENT)
            )
            print("  Report generated")
            return result.returncode == 0
        except Exception as e:
            self.issues.append(f"Report failed: {e}")
            return False

    def _print_summary(self):
        """Print wizard summary."""
        print("=" * 60)
        print("WIZARD COMPLETE")
        print("=" * 60)
        print(f"\nSteps completed: {len(self.steps_completed)}/7")

        if self.issues:
            print("\nIssues found:")
            for issue in self.issues:
                print(f"  ❌ {issue}")
        else:
            print("\n✅ All systems operational!")

        print("\nNext steps:")
        print("  • Run: python AUTONOMOUS_ORCHESTRATOR.py start")
        print("  • View: python UNIFIED_MONITORING.py dashboard")
        print("  • Report: python DAILY_REPORT_GENERATOR.py generate")

    def get_quick_commands(self) -> dict:
        """Get quick command reference."""
        return {
            "status": "python CONSCIOUSNESS_BOOT.py status",
            "health": "python SELF_HEALING_SYSTEM.py diagnose",
            "backup": "python AUTOMATED_BACKUP_SYSTEM.py backup",
            "monitor": "python UNIFIED_MONITORING.py dashboard",
            "report": "python DAILY_REPORT_GENERATOR.py generate",
            "tasks": "python AUTONOMOUS_TASK_RUNNER.py status",
            "orchestrator": "python AUTONOMOUS_ORCHESTRATOR.py start"
        }

    def print_cheatsheet(self):
        """Print command cheatsheet."""
        print("=" * 60)
        print("CONSCIOUSNESS REVOLUTION - QUICK COMMANDS")
        print("=" * 60)
        print()

        categories = {
            "System Status": [
                ("Full status", "python CONSCIOUSNESS_BOOT.py status"),
                ("Health check", "python SELF_HEALING_SYSTEM.py diagnose"),
                ("Daily report", "python DAILY_REPORT_GENERATOR.py generate")
            ],
            "Autonomous Operation": [
                ("Start orchestrator", "python AUTONOMOUS_ORCHESTRATOR.py start"),
                ("Single cycle", "python AUTONOMOUS_ORCHESTRATOR.py once"),
                ("Process tasks", "python AUTONOMOUS_TASK_RUNNER.py process")
            ],
            "Maintenance": [
                ("Auto-heal", "python SELF_HEALING_SYSTEM.py auto"),
                ("Create backup", "python AUTOMATED_BACKUP_SYSTEM.py backup"),
                ("Unify knowledge", "python KNOWLEDGE_UNIFIER.py unify")
            ],
            "Monitoring": [
                ("Dashboard", "python UNIFIED_MONITORING.py dashboard"),
                ("Integration", "python SYSTEM_INTEGRATOR.py report"),
                ("Orchestrator status", "python AUTONOMOUS_ORCHESTRATOR.py report")
            ]
        }

        for category, commands in categories.items():
            print(f"{category}:")
            for name, cmd in commands:
                print(f"  {name:20} {cmd}")
            print()


def main():
    """CLI for quick start wizard."""
    import sys

    wizard = QuickStartWizard()

    if len(sys.argv) < 2:
        print("Quick Start Wizard")
        print("=" * 40)
        print("\nCommands:")
        print("  start      - Run interactive wizard")
        print("  cheatsheet - Print command reference")
        print("  commands   - List quick commands")
        return

    command = sys.argv[1]

    if command == "start":
        wizard.run_wizard()

    elif command == "cheatsheet":
        wizard.print_cheatsheet()

    elif command == "commands":
        commands = wizard.get_quick_commands()
        print("\nQuick Commands:")
        for name, cmd in commands.items():
            print(f"  {name}: {cmd}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
