#!/usr/bin/env python3
"""
RECURSIVE TASK ENGINE
Tasks that spawn subtasks autonomously.
Self-expanding automation for foundational system issues.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re

from AUTONOMOUS_TASK_RUNNER import AutonomousRunner
from CYCLOTRON_BRAIN_BRIDGE import CyclotronBridge

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
RECURSIVE_PATH = CONSCIOUSNESS / "recursive_tasks"
RECURSIVE_PATH.mkdir(parents=True, exist_ok=True)


class RecursiveTask:
    """A task that can spawn subtasks."""

    def __init__(self, description: str, priority: str = "normal", parent_id: str = None):
        self.id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
        self.description = description
        self.priority = priority  # urgent, high, normal, low
        self.parent_id = parent_id
        self.subtasks = []
        self.status = "pending"  # pending, in_progress, completed, failed
        self.created = datetime.now().isoformat()
        self.completed = None
        self.result = None
        self.depth = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "parent_id": self.parent_id,
            "subtasks": self.subtasks,
            "status": self.status,
            "created": self.created,
            "completed": self.completed,
            "result": self.result,
            "depth": self.depth
        }


class RecursiveTaskEngine:
    """Engine for recursive task execution."""

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.runner = AutonomousRunner()
        self.cyclotron = CyclotronBridge()
        self.task_tree = {}
        self.execution_log = []

    def create_task(self, description: str, priority: str = "normal",
                   parent_id: str = None) -> RecursiveTask:
        """Create a new task."""
        task = RecursiveTask(description, priority, parent_id)

        if parent_id and parent_id in self.task_tree:
            parent = self.task_tree[parent_id]
            task.depth = parent.depth + 1
            parent.subtasks.append(task.id)

        self.task_tree[task.id] = task
        return task

    def decompose_task(self, task: RecursiveTask) -> List[str]:
        """
        Decompose a complex task into subtasks.
        Returns list of subtask descriptions.
        """
        if task.depth >= self.max_depth:
            return []

        description = task.description.lower()
        subtasks = []

        # Pattern-based decomposition
        if "build" in description or "create" in description:
            subtasks = [
                f"Research requirements for: {task.description}",
                f"Design architecture for: {task.description}",
                f"Implement core functionality for: {task.description}",
                f"Test and validate: {task.description}",
                f"Document and deploy: {task.description}"
            ]

        elif "fix" in description or "resolve" in description:
            subtasks = [
                f"Diagnose root cause of: {task.description}",
                f"Develop fix for: {task.description}",
                f"Test fix for: {task.description}",
                f"Verify no regression from: {task.description}"
            ]

        elif "integrate" in description:
            # Extract components
            components = re.findall(r'\b[A-Z][a-z]+\b', task.description)
            if len(components) >= 2:
                subtasks = [
                    f"Analyze {components[0]} interface",
                    f"Analyze {components[1]} interface",
                    f"Design integration layer between {components[0]} and {components[1]}",
                    f"Implement integration connectors",
                    f"Test integration end-to-end"
                ]

        elif "automate" in description:
            subtasks = [
                f"Identify manual steps in: {task.description}",
                f"Design automation workflow for: {task.description}",
                f"Build automation scripts for: {task.description}",
                f"Schedule and monitor automation"
            ]

        elif "optimize" in description or "improve" in description:
            subtasks = [
                f"Measure current performance of: {task.description}",
                f"Identify bottlenecks in: {task.description}",
                f"Implement optimizations for: {task.description}",
                f"Validate improvement in: {task.description}"
            ]

        return subtasks

    def execute_task(self, task: RecursiveTask) -> dict:
        """Execute a task recursively."""
        print(f"\n{'  ' * task.depth}[Depth {task.depth}] Executing: {task.description[:50]}...")

        task.status = "in_progress"

        # Check if task needs decomposition
        subtask_descriptions = self.decompose_task(task)

        if subtask_descriptions:
            print(f"{'  ' * task.depth}  Decomposed into {len(subtask_descriptions)} subtasks")

            # Create and execute subtasks
            subtask_results = []
            for desc in subtask_descriptions:
                subtask = self.create_task(desc, task.priority, task.id)
                result = self.execute_task(subtask)
                subtask_results.append(result)

            # Aggregate results
            task.result = {
                "type": "composite",
                "subtasks": len(subtask_results),
                "successful": sum(1 for r in subtask_results if r.get("status") == "complete"),
                "summary": f"Completed {len(subtask_results)} subtasks"
            }

        else:
            # Leaf task - execute directly
            try:
                result = self.runner.run_task(task.description, mode="quick")
                task.result = {
                    "type": "leaf",
                    "status": result["status"],
                    "outputs": len(result.get("outputs", [])),
                    "decisions": len(result.get("decisions", []))
                }
            except Exception as e:
                task.result = {
                    "type": "leaf",
                    "status": "failed",
                    "error": str(e)
                }

        task.status = "completed" if task.result.get("status") != "failed" else "failed"
        task.completed = datetime.now().isoformat()

        # Store in Cyclotron
        self.cyclotron.create_atom(
            f"Task {task.status}: {task.description[:100]} (depth {task.depth})",
            atom_type="action",
            source="recursive_engine",
            tags=["task", f"depth_{task.depth}", task.status]
        )

        return task.result

    def run(self, description: str, priority: str = "normal") -> dict:
        """Run a recursive task."""
        print("=" * 60)
        print("RECURSIVE TASK ENGINE")
        print("=" * 60)
        print(f"Task: {description}")
        print(f"Max depth: {self.max_depth}")
        print()

        # Create root task
        root = self.create_task(description, priority)

        # Execute recursively
        result = self.execute_task(root)

        # Generate report
        report = self._generate_report(root)

        # Save execution
        self._save_execution(root)

        return report

    def _generate_report(self, root: RecursiveTask) -> dict:
        """Generate execution report."""
        # Count tasks at each depth
        depth_counts = {}
        total_tasks = 0

        def count_tasks(task_id, depth=0):
            nonlocal total_tasks
            if task_id not in self.task_tree:
                return

            task = self.task_tree[task_id]
            total_tasks += 1
            depth_counts[depth] = depth_counts.get(depth, 0) + 1

            for subtask_id in task.subtasks:
                count_tasks(subtask_id, depth + 1)

        count_tasks(root.id)

        report = {
            "root_task": root.description,
            "status": root.status,
            "total_tasks": total_tasks,
            "depth_distribution": depth_counts,
            "max_depth_reached": max(depth_counts.keys()) if depth_counts else 0,
            "result": root.result
        }

        print("\n" + "=" * 60)
        print("EXECUTION REPORT")
        print("=" * 60)
        print(f"Status: {report['status']}")
        print(f"Total tasks: {report['total_tasks']}")
        print(f"Max depth: {report['max_depth_reached']}")
        print(f"Depth distribution: {report['depth_distribution']}")

        return report

    def _save_execution(self, root: RecursiveTask):
        """Save execution to disk."""
        execution = {
            "root_id": root.id,
            "tasks": {tid: t.to_dict() for tid, t in self.task_tree.items()},
            "timestamp": datetime.now().isoformat()
        }

        filename = f"execution_{root.id}.json"
        with open(RECURSIVE_PATH / filename, 'w') as f:
            json.dump(execution, f, indent=2)


class FoundationalIssueResolver:
    """Resolves foundational system issues recursively."""

    # Known foundational issues and their resolution tasks
    FOUNDATIONAL_ISSUES = {
        "knowledge_fragmentation": {
            "description": "Knowledge scattered across files",
            "resolution": "Build unified knowledge graph with Cyclotron indexing",
            "priority": "high"
        },
        "no_automated_monitoring": {
            "description": "No automated system health monitoring",
            "resolution": "Build comprehensive health monitoring with alerts",
            "priority": "high"
        },
        "api_cost_optimization": {
            "description": "API costs not optimized",
            "resolution": "Build API usage tracking and caching layer",
            "priority": "normal"
        },
        "missing_backup_system": {
            "description": "No automated backup system",
            "resolution": "Build automated backup with rotation and verification",
            "priority": "urgent"
        },
        "trinity_communication": {
            "description": "Trinity communication not standardized",
            "resolution": "Build standardized A2A protocol for Trinity",
            "priority": "high"
        },
        "onboarding_complexity": {
            "description": "User onboarding too complex",
            "resolution": "Build progressive disclosure onboarding system",
            "priority": "normal"
        },
        "knowledge_transfer_risk": {
            "description": "Too much knowledge in Commander's head",
            "resolution": "Build automated knowledge extraction and documentation",
            "priority": "high"
        },
        "no_error_recovery": {
            "description": "No automatic error recovery",
            "resolution": "Build self-healing system with automatic retry and fallback",
            "priority": "urgent"
        }
    }

    def __init__(self):
        self.engine = RecursiveTaskEngine(max_depth=3)
        self.cyclotron = CyclotronBridge()
        self.resolved = []

    def scan_issues(self) -> List[dict]:
        """Scan for unresolved foundational issues."""
        unresolved = []

        for issue_id, issue in self.FOUNDATIONAL_ISSUES.items():
            # Check if already resolved in Cyclotron
            atoms = self.cyclotron.search(issue_id)
            resolved_atoms = [a for a in atoms if "resolved" in a.tags]

            if not resolved_atoms:
                unresolved.append({
                    "id": issue_id,
                    **issue
                })

        return unresolved

    def resolve_issue(self, issue_id: str) -> dict:
        """Resolve a specific foundational issue."""
        if issue_id not in self.FOUNDATIONAL_ISSUES:
            return {"error": f"Unknown issue: {issue_id}"}

        issue = self.FOUNDATIONAL_ISSUES[issue_id]

        print(f"\nResolving: {issue['description']}")
        print(f"Task: {issue['resolution']}")

        # Run through recursive engine
        result = self.engine.run(issue['resolution'], issue['priority'])

        # Mark as resolved
        self.cyclotron.create_atom(
            f"Resolved foundational issue: {issue_id} - {issue['description']}",
            atom_type="decision",
            source="foundational_resolver",
            tags=[issue_id, "resolved", "foundational"]
        )

        self.resolved.append(issue_id)
        return result

    def resolve_all(self) -> dict:
        """Resolve all foundational issues."""
        print("=" * 60)
        print("FOUNDATIONAL ISSUE RESOLVER")
        print("=" * 60)

        unresolved = self.scan_issues()
        print(f"\nFound {len(unresolved)} unresolved issues")

        # Sort by priority
        priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
        unresolved.sort(key=lambda x: priority_order.get(x["priority"], 2))

        results = []
        for issue in unresolved:
            result = self.resolve_issue(issue["id"])
            results.append({
                "issue": issue["id"],
                "result": result
            })

        print("\n" + "=" * 60)
        print("RESOLUTION COMPLETE")
        print("=" * 60)
        print(f"Resolved: {len(results)}/{len(unresolved)} issues")

        return {
            "total": len(unresolved),
            "resolved": len(results),
            "results": results
        }

    def get_status(self) -> dict:
        """Get resolution status."""
        unresolved = self.scan_issues()
        return {
            "total_issues": len(self.FOUNDATIONAL_ISSUES),
            "unresolved": len(unresolved),
            "resolved": len(self.FOUNDATIONAL_ISSUES) - len(unresolved),
            "issues": [
                {
                    "id": issue_id,
                    "description": issue["description"],
                    "priority": issue["priority"],
                    "resolved": issue_id not in [u["id"] for u in unresolved]
                }
                for issue_id, issue in self.FOUNDATIONAL_ISSUES.items()
            ]
        }


def demo():
    """Demonstrate recursive task engine."""
    print("=" * 60)
    print("RECURSIVE TASK ENGINE DEMO")
    print("=" * 60)

    engine = RecursiveTaskEngine(max_depth=2)

    # Test recursive decomposition
    engine.run("Build automated backup system with rotation and cloud sync")


def main():
    """CLI for recursive task engine."""
    import sys

    if len(sys.argv) < 2:
        print("Recursive Task Engine")
        print("=" * 40)
        print("\nCommands:")
        print("  run <task>       - Run task recursively")
        print("  scan             - Scan foundational issues")
        print("  resolve <id>     - Resolve specific issue")
        print("  resolve-all      - Resolve all issues")
        print("  status           - Show issue status")
        print("  demo             - Run demo")
        return

    command = sys.argv[1]

    if command == "demo":
        demo()

    elif command == "run" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        engine = RecursiveTaskEngine()
        engine.run(task)

    elif command == "scan":
        resolver = FoundationalIssueResolver()
        issues = resolver.scan_issues()
        print(f"\nUnresolved foundational issues: {len(issues)}")
        for issue in issues:
            print(f"  [{issue['priority'].upper()}] {issue['id']}: {issue['description']}")

    elif command == "resolve" and len(sys.argv) >= 3:
        issue_id = sys.argv[2]
        resolver = FoundationalIssueResolver()
        resolver.resolve_issue(issue_id)

    elif command == "resolve-all":
        resolver = FoundationalIssueResolver()
        resolver.resolve_all()

    elif command == "status":
        resolver = FoundationalIssueResolver()
        status = resolver.get_status()
        print(f"\nFoundational Issues: {status['resolved']}/{status['total_issues']} resolved")
        for issue in status['issues']:
            symbol = "✅" if issue['resolved'] else "❌"
            print(f"  {symbol} [{issue['priority']}] {issue['id']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
