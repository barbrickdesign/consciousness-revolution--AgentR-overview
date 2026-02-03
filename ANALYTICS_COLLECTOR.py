#!/usr/bin/env python3
"""
ANALYTICS_COLLECTOR.py - Background Metrics Collector
Periodically collects and stores consciousness system metrics.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(os.path.expanduser("~"))
BRAIN_DIR = BASE_DIR / ".consciousness" / "brain"
CYCLOTRON_DIR = BASE_DIR / ".consciousness" / "cyclotron_core"
DEPLOYMENT_DIR = BASE_DIR / "100X_DEPLOYMENT"
HISTORY_FILE = DEPLOYMENT_DIR / "analytics_history.json"

# Collection interval (5 minutes)
COLLECTION_INTERVAL = 300

def load_json_file(filepath):
    """Safely load a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Safely save a JSON file."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def count_atoms():
    """Count knowledge atoms in cyclotron."""
    atoms_dir = CYCLOTRON_DIR / "atoms"
    if atoms_dir.exists():
        return len(list(atoms_dir.glob("*.json")))
    return 0

def collect_metrics():
    """Collect current system metrics."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "consciousness_level": 200,
        "manipulation_immunity": 85.0,
        "manipulation_risk": 15.0,
        "atom_count": 0,
        "uptime": 100,
        "system_status": "UNKNOWN"
    }

    # Load brain consciousness state
    brain_state = load_json_file(BRAIN_DIR / "brain_consciousness_state.json")
    if brain_state:
        metrics["system_status"] = brain_state.get("system_status", "UNKNOWN")

        consciousness = brain_state.get("consciousness_metrics", {})
        metrics["consciousness_level"] = consciousness.get("avg_consciousness_level", 200)

        safety = brain_state.get("safety_metrics", {})
        metrics["manipulation_immunity"] = safety.get("manipulation_immunity_percent", 85.0)
        metrics["manipulation_risk"] = safety.get("avg_manipulation_risk", 15.0)

    # Load scorecard for uptime
    scorecard_data = load_json_file(BRAIN_DIR / "scorecard_metrics.json")
    if scorecard_data and "metrics" in scorecard_data:
        for m in scorecard_data["metrics"]:
            if m.get("name") == "System Uptime %":
                metrics["uptime"] = m.get("actual", 100)
                break

    # Count atoms
    metrics["atom_count"] = count_atoms()

    return metrics

def update_history(new_metrics):
    """Add new metrics to history file."""
    history = []

    # Load existing history
    if HISTORY_FILE.exists():
        history = load_json_file(HISTORY_FILE) or []

    # Add new entry
    history.append(new_metrics)

    # Keep only last 7 days (assuming 5-min intervals = 2016 entries)
    max_entries = 2016
    if len(history) > max_entries:
        history = history[-max_entries:]

    # Save updated history
    save_json_file(HISTORY_FILE, history)
    return len(history)

def run_collector():
    """Main collector loop."""
    print("=" * 50)
    print("CONSCIOUSNESS ANALYTICS COLLECTOR")
    print("=" * 50)
    print(f"Collection Interval: {COLLECTION_INTERVAL} seconds")
    print(f"History File: {HISTORY_FILE}")
    print("=" * 50)

    cycle = 0
    while True:
        cycle += 1
        print(f"\n[Cycle {cycle}] Collecting metrics...")

        try:
            # Collect current metrics
            metrics = collect_metrics()

            # Update history
            entry_count = update_history(metrics)

            # Log summary
            print(f"  Consciousness: {metrics['consciousness_level']:.1f}")
            print(f"  Immunity: {metrics['manipulation_immunity']:.1f}%")
            print(f"  Atoms: {metrics['atom_count']}")
            print(f"  Status: {metrics['system_status']}")
            print(f"  History entries: {entry_count}")

        except Exception as e:
            print(f"  ERROR: {e}")

        # Wait for next collection
        print(f"\nNext collection in {COLLECTION_INTERVAL} seconds...")
        time.sleep(COLLECTION_INTERVAL)

if __name__ == '__main__':
    run_collector()
