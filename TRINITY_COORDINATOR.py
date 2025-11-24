#!/usr/bin/env python3
"""
TRINITY COORDINATOR
Manage and coordinate work across C1, C2, C3 instances.
Enables efficient task distribution and knowledge sharing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
TRINITY_PATH = HOME / ".trinity"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
COORDINATION_PATH = CONSCIOUSNESS / "trinity_coordination"
COORDINATION_PATH.mkdir(parents=True, exist_ok=True)

class TrinityCoordinator:
    """Coordinate work across Trinity instances."""

    def __init__(self):
        self.instances = {
            "c1": {"role": "Mechanic", "focus": "Build & Execute"},
            "c2": {"role": "Architect", "focus": "Design & Structure"},
            "c3": {"role": "Oracle", "focus": "Vision & Strategy"}
        }
        self.task_queue = COORDINATION_PATH / "shared_tasks.json"
        self.status_file = COORDINATION_PATH / "coordination_status.json"

    def assign_task(self, task: str, target: str = "auto",
                    priority: str = "normal", context: dict = None) -> dict:
        """Assign task to appropriate instance."""
        if target == "auto":
            target = self._determine_best_instance(task)

        task_entry = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "task": task,
            "assigned_to": target,
            "priority": priority,
            "status": "pending",
            "context": context or {},
            "created": datetime.now().isoformat()
        }

        # Load existing tasks
        tasks = self._load_tasks()
        tasks.append(task_entry)
        self._save_tasks(tasks)

        # Also send via A2A protocol if available
        self._send_a2a_notification(target, task_entry)

        return task_entry

    def _determine_best_instance(self, task: str) -> str:
        """Determine best instance for task based on keywords."""
        task_lower = task.lower()

        # C1 (Mechanic) - implementation, building, execution
        c1_keywords = ["build", "create", "implement", "fix", "deploy",
                       "install", "setup", "code", "write", "execute"]

        # C2 (Architect) - design, structure, architecture
        c2_keywords = ["design", "architect", "plan", "structure", "organize",
                       "schema", "framework", "system", "integrate", "optimize"]

        # C3 (Oracle) - strategy, vision, analysis
        c3_keywords = ["analyze", "research", "strategy", "vision", "pattern",
                       "predict", "assess", "evaluate", "recommend", "insight"]

        scores = {"c1": 0, "c2": 0, "c3": 0}

        for word in c1_keywords:
            if word in task_lower:
                scores["c1"] += 1

        for word in c2_keywords:
            if word in task_lower:
                scores["c2"] += 1

        for word in c3_keywords:
            if word in task_lower:
                scores["c3"] += 1

        # Return highest scoring, default to c2 for balanced work
        if max(scores.values()) == 0:
            return "c2"

        return max(scores.items(), key=lambda x: x[1])[0]

    def _load_tasks(self) -> List[dict]:
        """Load shared tasks."""
        if self.task_queue.exists():
            with open(self.task_queue) as f:
                return json.load(f)
        return []

    def _save_tasks(self, tasks: List[dict]):
        """Save shared tasks."""
        with open(self.task_queue, 'w') as f:
            json.dump(tasks, f, indent=2)

    def _send_a2a_notification(self, target: str, task: dict):
        """Send A2A notification about task."""
        a2a_path = TRINITY_PATH / "a2a_messages" / f"{target}_inbox"
        a2a_path.mkdir(parents=True, exist_ok=True)

        msg_file = a2a_path / f"task_{task['id']}.json"
        message = {
            "type": "TASK_ASSIGNMENT",
            "from": "coordinator",
            "to": target,
            "timestamp": datetime.now().isoformat(),
            "payload": task
        }

        with open(msg_file, 'w') as f:
            json.dump(message, f, indent=2)

    def get_pending_tasks(self, instance: str = None) -> List[dict]:
        """Get pending tasks, optionally filtered by instance."""
        tasks = self._load_tasks()
        pending = [t for t in tasks if t["status"] == "pending"]

        if instance:
            pending = [t for t in pending if t["assigned_to"] == instance]

        return sorted(pending, key=lambda x: {
            "urgent": 0, "high": 1, "normal": 2, "low": 3
        }.get(x["priority"], 2))

    def complete_task(self, task_id: str, result: str = None) -> bool:
        """Mark task as complete."""
        tasks = self._load_tasks()

        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                task["result"] = result
                self._save_tasks(tasks)
                return True

        return False

    def get_instance_status(self) -> Dict:
        """Get status of all instances."""
        status = {}

        for instance in self.instances:
            instance_status = {
                "role": self.instances[instance]["role"],
                "focus": self.instances[instance]["focus"],
                "pending_tasks": 0,
                "completed_tasks": 0,
                "last_activity": None
            }

            # Check session state
            session = CONSCIOUSNESS / "sessions" / f"{instance}_current.json"
            if session.exists():
                with open(session) as f:
                    data = json.load(f)
                instance_status["last_activity"] = data.get("timestamp")
                instance_status["active_tasks"] = data.get("active_tasks", [])

            # Count tasks
            tasks = self._load_tasks()
            for task in tasks:
                if task["assigned_to"] == instance:
                    if task["status"] == "pending":
                        instance_status["pending_tasks"] += 1
                    elif task["status"] == "completed":
                        instance_status["completed_tasks"] += 1

            status[instance] = instance_status

        return status

    def distribute_workload(self, tasks: List[str], strategy: str = "balanced") -> List[dict]:
        """Distribute multiple tasks across instances."""
        assignments = []

        if strategy == "balanced":
            # Round-robin distribution
            instances = list(self.instances.keys())
            for i, task in enumerate(tasks):
                target = instances[i % len(instances)]
                assignment = self.assign_task(task, target)
                assignments.append(assignment)

        elif strategy == "smart":
            # Auto-assign based on task content
            for task in tasks:
                assignment = self.assign_task(task, "auto")
                assignments.append(assignment)

        elif strategy == "priority":
            # All to highest priority instance (c2 default)
            for task in tasks:
                assignment = self.assign_task(task, "c2", "high")
                assignments.append(assignment)

        return assignments

    def sync_status(self):
        """Sync and update coordination status."""
        status = {
            "last_sync": datetime.now().isoformat(),
            "instances": self.get_instance_status(),
            "total_pending": len(self.get_pending_tasks()),
            "task_distribution": self._get_distribution()
        }

        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)

        return status

    def _get_distribution(self) -> Dict:
        """Get task distribution across instances."""
        tasks = self._load_tasks()
        distribution = {"c1": 0, "c2": 0, "c3": 0}

        for task in tasks:
            if task["status"] == "pending":
                instance = task["assigned_to"]
                if instance in distribution:
                    distribution[instance] += 1

        return distribution

    def generate_report(self) -> str:
        """Generate coordination report."""
        status = self.sync_status()

        lines = []
        lines.append("=" * 60)
        lines.append("TRINITY COORDINATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        # Instance status
        lines.append("INSTANCES:")
        for instance, data in status["instances"].items():
            lines.append(f"\n  {instance.upper()} - {data['role']}")
            lines.append(f"    Focus: {data['focus']}")
            lines.append(f"    Pending: {data['pending_tasks']}")
            lines.append(f"    Completed: {data['completed_tasks']}")
            if data.get("last_activity"):
                lines.append(f"    Last Active: {data['last_activity']}")

        lines.append("")

        # Distribution
        lines.append("TASK DISTRIBUTION:")
        dist = status["task_distribution"]
        total = sum(dist.values()) or 1
        for instance, count in dist.items():
            pct = (count / total) * 100
            bar = "█" * int(pct / 10)
            lines.append(f"  {instance.upper()}: {count} ({pct:.0f}%) {bar}")

        lines.append("")
        lines.append(f"Total Pending: {status['total_pending']}")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """CLI for Trinity coordinator."""
    import sys

    coordinator = TrinityCoordinator()

    if len(sys.argv) < 2:
        print("Trinity Coordinator")
        print("=" * 40)
        print("\nCommands:")
        print("  assign <task>     - Assign task (auto-routes)")
        print("  status            - Instance status")
        print("  pending [inst]    - Show pending tasks")
        print("  complete <id>     - Complete task")
        print("  report            - Full report")
        print("  sync              - Sync status")
        return

    command = sys.argv[1]

    if command == "assign":
        if len(sys.argv) < 3:
            print("Usage: assign <task>")
            return

        task = " ".join(sys.argv[2:])
        result = coordinator.assign_task(task)
        print(f"\nTask assigned to {result['assigned_to'].upper()}")
        print(f"ID: {result['id']}")

    elif command == "status":
        status = coordinator.get_instance_status()
        for instance, data in status.items():
            print(f"\n{instance.upper()} ({data['role']}):")
            print(f"  Pending: {data['pending_tasks']}")
            print(f"  Completed: {data['completed_tasks']}")

    elif command == "pending":
        instance = sys.argv[2] if len(sys.argv) > 2 else None
        tasks = coordinator.get_pending_tasks(instance)

        if not tasks:
            print("\nNo pending tasks")
            return

        print(f"\nPending tasks ({len(tasks)}):")
        for task in tasks:
            print(f"  [{task['assigned_to'].upper()}] {task['task'][:50]}")

    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: complete <task_id>")
            return

        task_id = sys.argv[2]
        if coordinator.complete_task(task_id):
            print(f"Task {task_id} completed")
        else:
            print(f"Task {task_id} not found")

    elif command == "report":
        print(coordinator.generate_report())

    elif command == "sync":
        status = coordinator.sync_status()
        print(f"\nSync complete")
        print(f"Total pending: {status['total_pending']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
