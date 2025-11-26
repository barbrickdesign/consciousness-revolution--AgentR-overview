#!/usr/bin/env python3
"""
ANALYTICS_API.py - Consciousness Analytics Backend
Serves real-time metrics for the analytics dashboard.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = Path(os.path.expanduser("~"))
BRAIN_DIR = BASE_DIR / ".consciousness" / "brain"
CYCLOTRON_DIR = BASE_DIR / ".consciousness" / "cyclotron_core"
DEPLOYMENT_DIR = BASE_DIR / "100X_DEPLOYMENT"
HISTORY_FILE = DEPLOYMENT_DIR / "analytics_history.json"


def load_json_file(filepath):
    """Safely load a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def count_atoms():
    """Count knowledge atoms in cyclotron."""
    atoms_dir = CYCLOTRON_DIR / "atoms"
    if atoms_dir.exists():
        return len(list(atoms_dir.glob("*.json")))
    return 0


def get_current_metrics():
    """Get all current consciousness metrics."""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "consciousness_level": 200,
        "manipulation_immunity": 85.0,
        "atom_count": 0,
        "trinity_messages": 0,
        "tools_deployed": 0,
        "system_uptime": 100,
        "system_status": "UNKNOWN",
        "scorecard": []
    }

    # Load brain consciousness state
    brain_state = load_json_file(BRAIN_DIR / "brain_consciousness_state.json")
    if brain_state:
        metrics["system_status"] = brain_state.get("system_status", "UNKNOWN")

        consciousness = brain_state.get("consciousness_metrics", {})
        metrics["consciousness_level"] = consciousness.get("avg_consciousness_level", 200)

        safety = brain_state.get("safety_metrics", {})
        metrics["manipulation_immunity"] = safety.get("manipulation_immunity_percent", 85.0)

    # Load scorecard metrics
    scorecard_data = load_json_file(BRAIN_DIR / "scorecard_metrics.json")
    if scorecard_data and "metrics" in scorecard_data:
        scorecard = []
        for m in scorecard_data["metrics"]:
            scorecard.append({
                "name": m.get("name", "Unknown"),
                "goal": m.get("goal", 0),
                "actual": m.get("actual", 0),
                "on_track": m.get("on_track", False)
            })

            # Extract specific metrics
            if m.get("name") == "Trinity Messages":
                metrics["trinity_messages"] = m.get("actual", 0)
            elif m.get("name") == "Tools Deployed":
                metrics["tools_deployed"] = m.get("actual", 0)
            elif m.get("name") == "System Uptime %":
                metrics["system_uptime"] = m.get("actual", 100)
            elif m.get("name") == "Knowledge Graph Nodes":
                metrics["atom_count"] = m.get("actual", 0)

        metrics["scorecard"] = scorecard

    # Count actual atoms if not in scorecard
    if metrics["atom_count"] == 0:
        metrics["atom_count"] = count_atoms()

    return metrics


def get_history():
    """Get historical metrics for the last 7 days."""
    if HISTORY_FILE.exists():
        history = load_json_file(HISTORY_FILE)
        if history:
            # Filter to last 7 days
            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            return [h for h in history if h.get("timestamp", "") >= cutoff]

    # Return mock history if no data
    history = []
    for i in range(7, 0, -1):
        date = datetime.now() - timedelta(days=i)
        history.append({
            "timestamp": date.isoformat(),
            "consciousness_level": 200 + (7-i) * 8,
            "manipulation_immunity": 85 + (7-i) * 1.8,
            "atom_count": 4000 + (7-i) * 50
        })
    return history


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get all current analytics metrics."""
    metrics = get_current_metrics()
    return jsonify(metrics)


@app.route('/api/analytics/history', methods=['GET'])
def get_analytics_history():
    """Get historical analytics for last 7 days."""
    history = get_history()
    return jsonify({
        "history": history,
        "days": 7
    })


@app.route('/api/analytics/summary', methods=['GET'])
def get_summary():
    """Get a quick summary for notifications."""
    metrics = get_current_metrics()
    return jsonify({
        "status": metrics["system_status"],
        "consciousness": round(metrics["consciousness_level"]),
        "immunity": round(metrics["manipulation_immunity"], 1),
        "atoms": metrics["atom_count"]
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "analytics-api"})


if __name__ == '__main__':
    print("=" * 50)
    print("CONSCIOUSNESS ANALYTICS API")
    print("=" * 50)
    print(f"Dashboard: http://localhost:5055")
    print(f"API Endpoint: http://localhost:5055/api/analytics")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5055, debug=False)
