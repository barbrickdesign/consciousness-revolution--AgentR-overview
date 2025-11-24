#!/usr/bin/env python3
"""
SESSION PERSISTENCE
Save and restore session state for continuity across instances.
Enables seamless handoff between C1, C2, C3.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
SESSION_PATH = CONSCIOUSNESS / "sessions"
SESSION_PATH.mkdir(parents=True, exist_ok=True)


class SessionState:
    """Capture and restore session state."""

    def __init__(self, agent_id: str = "c2"):
        self.agent_id = agent_id
        self.current_session = SESSION_PATH / f"{agent_id}_current.json"
        self.history_path = SESSION_PATH / f"{agent_id}_history"
        self.history_path.mkdir(exist_ok=True)

    def save_state(self,
                   active_tasks: List[str] = None,
                   completed_tasks: List[str] = None,
                   context: Dict = None,
                   handoff_notes: str = None) -> dict:
        """Save current session state."""

        state = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "active_tasks": active_tasks or [],
            "completed_tasks": completed_tasks or [],
            "context": context or {},
            "handoff_notes": handoff_notes,
            "system_status": self._get_system_status()
        }

        # Save current
        with open(self.current_session, 'w') as f:
            json.dump(state, f, indent=2)

        # Archive to history
        archive_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(self.history_path / archive_name, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"Session state saved for {self.agent_id}")
        return state

    def load_state(self) -> Optional[dict]:
        """Load current session state."""
        if self.current_session.exists():
            with open(self.current_session) as f:
                return json.load(f)
        return None

    def get_last_handoff(self) -> Optional[dict]:
        """Get last session for handoff."""
        state = self.load_state()
        if state:
            return {
                "from": state["agent_id"],
                "time": state["timestamp"],
                "active_tasks": state["active_tasks"],
                "notes": state.get("handoff_notes"),
                "status": state.get("system_status")
            }
        return None

    def _get_system_status(self) -> dict:
        """Get current system status."""
        status = {}

        # Cyclotron
        cyclotron_index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if cyclotron_index.exists():
            with open(cyclotron_index) as f:
                data = json.load(f)
            status["cyclotron_atoms"] = len(data.get("atoms", []))

        # Monitoring
        monitoring = CONSCIOUSNESS / "monitoring" / "metrics.json"
        if monitoring.exists():
            with open(monitoring) as f:
                data = json.load(f)
            status["health_score"] = data.get("current", {}).get("health_score")

        # Task queue
        queue_path = CONSCIOUSNESS / "task_queue"
        if queue_path.exists():
            pending = len([f for f in queue_path.glob("*.json")])
            status["pending_tasks"] = pending

        return status

    def create_handoff(self, to_agent: str, tasks: List[str], notes: str) -> dict:
        """Create handoff for another agent."""
        handoff = {
            "from": self.agent_id,
            "to": to_agent,
            "timestamp": datetime.now().isoformat(),
            "tasks": tasks,
            "notes": notes,
            "system_status": self._get_system_status()
        }

        # Save to target agent's inbox
        handoff_file = SESSION_PATH / f"handoff_{self.agent_id}_to_{to_agent}.json"
        with open(handoff_file, 'w') as f:
            json.dump(handoff, f, indent=2)

        print(f"Handoff created: {self.agent_id} → {to_agent}")
        return handoff

    def receive_handoff(self) -> Optional[dict]:
        """Check for incoming handoffs."""
        for handoff_file in SESSION_PATH.glob(f"handoff_*_to_{self.agent_id}.json"):
            with open(handoff_file) as f:
                handoff = json.load(f)

            # Archive it
            archive = self.history_path / f"received_{handoff_file.name}"
            handoff_file.rename(archive)

            return handoff
        return None

    def get_session_summary(self) -> dict:
        """Get summary of session activity."""
        history_files = sorted(self.history_path.glob("session_*.json"))

        if not history_files:
            return {"sessions": 0}

        sessions = []
        for f in history_files[-10:]:  # Last 10
            with open(f) as file:
                data = json.load(file)
            sessions.append({
                "time": data["timestamp"],
                "completed": len(data.get("completed_tasks", [])),
                "active": len(data.get("active_tasks", []))
            })

        return {
            "total_sessions": len(history_files),
            "recent": sessions
        }


def capture_current_state():
    """Capture C2's current state."""
    session = SessionState("c2")

    # Get completed tasks from this session
    completed = [
        "Built brain agent framework (4 base + 5 advanced agents)",
        "Created Cyclotron-Brain bridge (285 atoms)",
        "Built autonomous task runner",
        "Created brain scheduler",
        "Built recursive task engine",
        "Created self-healing system (8/8 checks passing)",
        "Resolved URGENT: backup system, error recovery",
        "Resolved HIGH: knowledge fragmentation, trinity communication",
        "Built unified monitoring with API tracking",
        "Created consciousness boot system"
    ]

    # Active/pending
    active = [
        "Knowledge unifier running (285 atoms)",
        "Monitoring active",
        "Remaining issues: onboarding, knowledge-transfer"
    ]

    # Context
    context = {
        "cyclotron_atoms": 285,
        "health_score": 80,
        "foundational_issues_resolved": "6/8",
        "systems_built": 12
    }

    # Handoff notes
    notes = """
C2 Session Complete - Foundational Automation Suite

Key Systems:
- BRAIN_AGENT_FRAMEWORK.py, ADVANCED_BRAIN_AGENTS.py
- CYCLOTRON_BRAIN_BRIDGE.py, AUTONOMOUS_TASK_RUNNER.py
- BRAIN_SCHEDULER.py, RECURSIVE_TASK_ENGINE.py
- SELF_HEALING_SYSTEM.py, AUTOMATED_BACKUP_SYSTEM.py
- ERROR_RECOVERY_SYSTEM.py, KNOWLEDGE_UNIFIER.py
- TRINITY_A2A_PROTOCOL.py, UNIFIED_MONITORING.py
- CONSCIOUSNESS_BOOT.py

Quick Start: python CONSCIOUSNESS_BOOT.py full

Remaining: onboarding_complexity, knowledge_transfer_risk
"""

    state = session.save_state(active, completed, context, notes)
    return state


def main():
    """CLI for session persistence."""
    import sys

    session = SessionState("c2")

    if len(sys.argv) < 2:
        print("Session Persistence")
        print("=" * 40)
        print("\nCommands:")
        print("  save       - Save current state")
        print("  load       - Load last state")
        print("  handoff    - Show last handoff")
        print("  summary    - Session summary")
        print("  capture    - Capture C2 current state")
        return

    command = sys.argv[1]

    if command == "save":
        session.save_state()

    elif command == "load":
        state = session.load_state()
        if state:
            print(f"\nLast session: {state['timestamp']}")
            print(f"Active tasks: {len(state['active_tasks'])}")
            print(f"Completed: {len(state['completed_tasks'])}")
        else:
            print("No saved state")

    elif command == "handoff":
        handoff = session.get_last_handoff()
        if handoff:
            print(f"\nHandoff from: {handoff['from']}")
            print(f"Time: {handoff['time']}")
            print(f"Tasks: {handoff['active_tasks']}")
            print(f"Notes: {handoff['notes']}")
        else:
            print("No handoff available")

    elif command == "summary":
        summary = session.get_session_summary()
        print(f"\nTotal sessions: {summary['total_sessions']}")
        if summary.get('recent'):
            print("Recent:")
            for s in summary['recent']:
                print(f"  {s['time']}: {s['completed']} completed, {s['active']} active")

    elif command == "capture":
        capture_current_state()
        print("C2 state captured")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
