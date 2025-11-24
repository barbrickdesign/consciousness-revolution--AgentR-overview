#!/usr/bin/env python3
"""
BRAIN SCHEDULER
Scheduled task automation for brain operations.
Runs periodic tasks like knowledge sync, health checks, and pattern analysis.
"""

import json
import time
import schedule
from pathlib import Path
from datetime import datetime
from typing import Callable, List

# Import our systems
from AUTONOMOUS_TASK_RUNNER import AutonomousRunner
from CYCLOTRON_BRAIN_BRIDGE import CyclotronBridge
from BRAIN_INTEGRATION_HOOKS import BrainIntegration

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
SCHEDULER_LOG = CONSCIOUSNESS / "scheduler_log.json"


class BrainScheduler:
    """Scheduled brain operations."""

    def __init__(self):
        self.runner = AutonomousRunner()
        self.cyclotron = CyclotronBridge()
        self.integration = BrainIntegration()
        self.execution_log = []
        self.running = False

    def log_execution(self, task_name: str, result: str):
        """Log scheduled execution."""
        entry = {
            "task": task_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.execution_log.append(entry)

        # Save log
        with open(SCHEDULER_LOG, 'w') as f:
            json.dump({
                "executions": self.execution_log[-100:],  # Keep last 100
                "updated": datetime.now().isoformat()
            }, f, indent=2)

    # === SCHEDULED TASKS ===

    def sync_brain_cyclotron(self):
        """Sync brain data to Cyclotron."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Syncing Brain → Cyclotron...")

        try:
            # Ingest from brain
            ingested = self.cyclotron.ingest_from_brain()

            # Export summary back
            self.cyclotron.export_to_brain()

            self.log_execution("sync_brain_cyclotron", f"Success: {ingested} atoms")
            print(f"  Synced {ingested} atoms")

        except Exception as e:
            self.log_execution("sync_brain_cyclotron", f"Error: {str(e)}")
            print(f"  Error: {e}")

    def run_knowledge_consolidation(self):
        """Consolidate knowledge atoms."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Consolidating knowledge...")

        try:
            # Get atoms by type
            insights = self.cyclotron.search_by_type("insight")
            patterns = self.cyclotron.search_by_type("pattern")
            decisions = self.cyclotron.search_by_type("decision")

            # Create consolidation summary
            summary = {
                "insights": len(insights),
                "patterns": len(patterns),
                "decisions": len(decisions),
                "total": self.cyclotron.get_status()["total_atoms"]
            }

            # Create consolidation atom
            self.cyclotron.create_atom(
                f"Knowledge consolidation: {summary['total']} atoms ({summary['insights']} insights, {summary['patterns']} patterns, {summary['decisions']} decisions)",
                atom_type="fact",
                source="scheduler",
                tags=["consolidation", "summary"]
            )

            self.log_execution("knowledge_consolidation", f"Success: {summary}")
            print(f"  Consolidated: {summary['total']} atoms")

        except Exception as e:
            self.log_execution("knowledge_consolidation", f"Error: {str(e)}")
            print(f"  Error: {e}")

    def run_pattern_scan(self):
        """Scan recent content for patterns."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scanning for patterns...")

        try:
            # Get recent atoms
            recent = self.cyclotron.index["atoms"][-20:]

            patterns_found = 0

            for atom_ref in recent:
                atom = self.cyclotron.get_atom(atom_ref["id"])
                if atom:
                    # Run pattern detection
                    result = self.runner.run_task(
                        f"Analyze for patterns: {atom.content[:100]}",
                        mode="quick"
                    )

                    if result.get("context", {}).get("pattern_analysis", {}).get("patterns_detected", 0) > 0:
                        patterns_found += 1

            self.log_execution("pattern_scan", f"Success: {patterns_found} patterns found")
            print(f"  Found {patterns_found} patterns in {len(recent)} atoms")

        except Exception as e:
            self.log_execution("pattern_scan", f"Error: {str(e)}")
            print(f"  Error: {e}")

    def process_task_queue(self):
        """Process pending tasks."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processing task queue...")

        try:
            results = self.runner.process_queue()
            self.log_execution("process_queue", f"Success: {len(results)} tasks")
            print(f"  Processed {len(results)} tasks")

        except Exception as e:
            self.log_execution("process_queue", f"Error: {str(e)}")
            print(f"  Error: {e}")

    def run_health_check(self):
        """Run brain health check."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running health check...")

        try:
            # Check integration status
            status = self.integration.get_integration_status()

            # Check Cyclotron status
            cyclotron_status = self.cyclotron.get_status()

            # Check runner status
            runner_status = self.runner.get_status()

            health = {
                "integration_ready": status["ready"],
                "brain_files": status["brain_files"],
                "cyclotron_atoms": cyclotron_status["total_atoms"],
                "pending_tasks": runner_status["pending_tasks"]
            }

            # Create health atom
            self.cyclotron.create_atom(
                f"Health check: {cyclotron_status['total_atoms']} atoms, {runner_status['pending_tasks']} pending tasks, integration {'ready' if status['ready'] else 'not ready'}",
                atom_type="fact",
                source="scheduler",
                tags=["health", "status"]
            )

            self.log_execution("health_check", f"Success: {health}")
            print(f"  Health: {health}")

        except Exception as e:
            self.log_execution("health_check", f"Error: {str(e)}")
            print(f"  Error: {e}")

    def run_eos_sync(self):
        """Sync EOS data to brain."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Syncing EOS data...")

        try:
            results = self.integration.sync_all()

            total_pushed = sum(
                r.get("pushed", 0) for r in results.values()
                if isinstance(r, dict) and "pushed" in r
            )

            self.log_execution("eos_sync", f"Success: {total_pushed} items")
            print(f"  Synced {total_pushed} EOS items")

        except Exception as e:
            self.log_execution("eos_sync", f"Error: {str(e)}")
            print(f"  Error: {e}")

    # === SCHEDULER CONTROL ===

    def setup_schedule(self):
        """Set up the schedule."""
        # Every 30 minutes
        schedule.every(30).minutes.do(self.sync_brain_cyclotron)

        # Every hour
        schedule.every().hour.do(self.run_health_check)
        schedule.every().hour.do(self.process_task_queue)

        # Every 2 hours
        schedule.every(2).hours.do(self.run_knowledge_consolidation)

        # Every 4 hours
        schedule.every(4).hours.do(self.run_pattern_scan)

        # Daily at 6 AM
        schedule.every().day.at("06:00").do(self.run_eos_sync)

        print("Schedule configured:")
        print("  • Every 30 min: Brain-Cyclotron sync")
        print("  • Every hour: Health check, Process queue")
        print("  • Every 2 hours: Knowledge consolidation")
        print("  • Every 4 hours: Pattern scan")
        print("  • Daily 6 AM: EOS sync")

    def run_once(self):
        """Run all tasks once (for testing)."""
        print("=" * 60)
        print("RUNNING ALL SCHEDULED TASKS ONCE")
        print("=" * 60)

        self.sync_brain_cyclotron()
        self.run_health_check()
        self.process_task_queue()
        self.run_knowledge_consolidation()
        self.run_eos_sync()

        print("\n" + "=" * 60)
        print("ALL TASKS COMPLETE")
        print("=" * 60)

    def start(self):
        """Start the scheduler."""
        print("=" * 60)
        print("BRAIN SCHEDULER STARTING")
        print("=" * 60)

        self.setup_schedule()

        # Run immediate sync
        self.sync_brain_cyclotron()
        self.run_health_check()

        self.running = True
        print(f"\nScheduler running. Press Ctrl+C to stop.")

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nScheduler stopped.")

    def stop(self):
        """Stop the scheduler."""
        self.running = False

    def get_status(self) -> dict:
        """Get scheduler status."""
        return {
            "running": self.running,
            "jobs": len(schedule.get_jobs()),
            "executions": len(self.execution_log),
            "last_execution": self.execution_log[-1] if self.execution_log else None
        }


def main():
    """CLI for brain scheduler."""
    import sys

    scheduler = BrainScheduler()

    if len(sys.argv) < 2:
        print("Brain Scheduler")
        print("=" * 40)
        print("\nCommands:")
        print("  start    - Start scheduler daemon")
        print("  once     - Run all tasks once")
        print("  sync     - Sync brain-cyclotron")
        print("  health   - Run health check")
        print("  eos      - Sync EOS data")
        print("  status   - Show status")
        return

    command = sys.argv[1]

    if command == "start":
        scheduler.start()

    elif command == "once":
        scheduler.run_once()

    elif command == "sync":
        scheduler.sync_brain_cyclotron()

    elif command == "health":
        scheduler.run_health_check()

    elif command == "eos":
        scheduler.run_eos_sync()

    elif command == "status":
        cyclotron_status = scheduler.cyclotron.get_status()
        runner_status = scheduler.runner.get_status()

        print("\nBrain Scheduler Status:")
        print(f"  Cyclotron atoms: {cyclotron_status['total_atoms']}")
        print(f"  Pending tasks: {runner_status['pending_tasks']}")
        print(f"  Total results: {runner_status['total_results']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
