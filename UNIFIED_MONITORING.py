#!/usr/bin/env python3
"""
UNIFIED MONITORING SYSTEM
Comprehensive monitoring with API cost tracking.
Resolves: no_automated_monitoring, api_cost_optimization
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
MONITORING = CONSCIOUSNESS / "monitoring"
MONITORING.mkdir(parents=True, exist_ok=True)


class APIUsageTracker:
    """Track API usage and costs."""

    # Pricing per 1K tokens (approximate)
    PRICING = {
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
    }

    def __init__(self):
        self.usage_file = MONITORING / "api_usage.json"
        self._load_usage()

    def _load_usage(self):
        if self.usage_file.exists():
            with open(self.usage_file) as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                "daily": {},
                "models": {},
                "total_cost": 0,
                "total_tokens": 0
            }

    def _save_usage(self):
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)

    def log_usage(self, model: str, input_tokens: int, output_tokens: int):
        """Log API usage."""
        today = datetime.now().strftime("%Y-%m-%d")

        # Calculate cost
        pricing = self.PRICING.get(model, {"input": 0.01, "output": 0.03})
        cost = (input_tokens / 1000 * pricing["input"] +
                output_tokens / 1000 * pricing["output"])

        # Update daily
        if today not in self.usage["daily"]:
            self.usage["daily"][today] = {"tokens": 0, "cost": 0, "calls": 0}

        self.usage["daily"][today]["tokens"] += input_tokens + output_tokens
        self.usage["daily"][today]["cost"] += cost
        self.usage["daily"][today]["calls"] += 1

        # Update by model
        if model not in self.usage["models"]:
            self.usage["models"][model] = {"tokens": 0, "cost": 0, "calls": 0}

        self.usage["models"][model]["tokens"] += input_tokens + output_tokens
        self.usage["models"][model]["cost"] += cost
        self.usage["models"][model]["calls"] += 1

        # Update totals
        self.usage["total_cost"] += cost
        self.usage["total_tokens"] += input_tokens + output_tokens

        self._save_usage()

        return {"cost": cost, "tokens": input_tokens + output_tokens}

    def get_daily_report(self, days: int = 7) -> dict:
        """Get usage report for last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.strftime("%Y-%m-%d")

        report = {
            "period_days": days,
            "total_cost": 0,
            "total_tokens": 0,
            "total_calls": 0,
            "daily": []
        }

        for date, data in sorted(self.usage["daily"].items()):
            if date >= cutoff_str:
                report["daily"].append({
                    "date": date,
                    **data
                })
                report["total_cost"] += data["cost"]
                report["total_tokens"] += data["tokens"]
                report["total_calls"] += data["calls"]

        return report

    def get_cost_projections(self) -> dict:
        """Project costs based on current usage."""
        report = self.get_daily_report(7)

        if not report["daily"]:
            return {"error": "No usage data"}

        avg_daily_cost = report["total_cost"] / len(report["daily"])

        return {
            "avg_daily": avg_daily_cost,
            "projected_weekly": avg_daily_cost * 7,
            "projected_monthly": avg_daily_cost * 30,
            "by_model": {
                model: {
                    "cost": data["cost"],
                    "calls": data["calls"],
                    "cost_per_call": data["cost"] / data["calls"] if data["calls"] else 0
                }
                for model, data in self.usage["models"].items()
            }
        }


class SystemMonitor:
    """Monitor all system components."""

    def __init__(self):
        self.metrics_file = MONITORING / "metrics.json"
        self.alerts_file = MONITORING / "alerts.json"
        self.api_tracker = APIUsageTracker()
        self._load_metrics()
        self._load_alerts()

    def _load_metrics(self):
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {"history": [], "current": {}}

    def _save_metrics(self):
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)

    def _load_alerts(self):
        if self.alerts_file.exists():
            with open(self.alerts_file) as f:
                self.alerts = json.load(f)
        else:
            self.alerts = {"active": [], "history": []}

    def _save_alerts(self):
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)

    def collect_metrics(self) -> dict:
        """Collect all system metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cyclotron": self._check_cyclotron(),
            "brain": self._check_brain(),
            "disk": self._check_disk(),
            "files": self._check_files(),
            "api": self._check_api()
        }

        # Calculate health score
        scores = []
        for component, data in metrics.items():
            if isinstance(data, dict) and "healthy" in data:
                scores.append(1 if data["healthy"] else 0)

        metrics["health_score"] = sum(scores) / len(scores) * 100 if scores else 0

        # Store
        self.metrics["current"] = metrics
        self.metrics["history"].append({
            "timestamp": metrics["timestamp"],
            "health_score": metrics["health_score"]
        })
        self.metrics["history"] = self.metrics["history"][-100:]  # Keep last 100

        self._save_metrics()

        # Check for alerts
        self._check_alerts(metrics)

        return metrics

    def _check_cyclotron(self) -> dict:
        """Check Cyclotron status."""
        index_path = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"

        if not index_path.exists():
            return {"healthy": False, "error": "Index missing"}

        try:
            with open(index_path) as f:
                data = json.load(f)

            atom_count = len(data.get("atoms", []))
            return {
                "healthy": atom_count > 0,
                "atoms": atom_count,
                "types": len(data.get("types", {})),
                "tags": len(data.get("tags", {}))
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _check_brain(self) -> dict:
        """Check brain directories."""
        brain_path = CONSCIOUSNESS / "brain"
        agents_path = CONSCIOUSNESS / "agents"

        brain_files = len(list(brain_path.glob("*.json"))) if brain_path.exists() else 0
        agent_states = len(list(agents_path.glob("*.json"))) if agents_path.exists() else 0

        return {
            "healthy": brain_files > 0,
            "brain_files": brain_files,
            "agent_states": agent_states
        }

    def _check_disk(self) -> dict:
        """Check disk usage."""
        import shutil
        usage = shutil.disk_usage(HOME)
        percent_free = (usage.free / usage.total) * 100

        return {
            "healthy": percent_free > 10,
            "percent_free": round(percent_free, 1),
            "free_gb": round(usage.free / (1024**3), 2)
        }

    def _check_files(self) -> dict:
        """Check critical files."""
        critical = [
            CONSCIOUSNESS / "cyclotron_core" / "INDEX.json",
            MONITORING / "api_usage.json"
        ]

        missing = [str(f) for f in critical if not f.exists()]

        return {
            "healthy": len(missing) == 0,
            "checked": len(critical),
            "missing": missing
        }

    def _check_api(self) -> dict:
        """Check API usage."""
        report = self.api_tracker.get_daily_report(1)

        return {
            "healthy": True,
            "today_cost": report["total_cost"],
            "today_calls": report["total_calls"]
        }

    def _check_alerts(self, metrics: dict):
        """Check for alert conditions."""
        new_alerts = []

        # Low disk space
        if metrics.get("disk", {}).get("percent_free", 100) < 10:
            new_alerts.append({
                "type": "disk_low",
                "severity": "warning",
                "message": f"Disk space low: {metrics['disk']['percent_free']}% free"
            })

        # Low health score
        if metrics.get("health_score", 100) < 70:
            new_alerts.append({
                "type": "health_low",
                "severity": "warning",
                "message": f"System health low: {metrics['health_score']}%"
            })

        # High API cost
        api_cost = metrics.get("api", {}).get("today_cost", 0)
        if api_cost > 10:  # $10/day threshold
            new_alerts.append({
                "type": "api_cost_high",
                "severity": "warning",
                "message": f"High API cost today: ${api_cost:.2f}"
            })

        # Add new alerts
        for alert in new_alerts:
            alert["timestamp"] = datetime.now().isoformat()
            self.alerts["active"].append(alert)

        self._save_alerts()

    def get_dashboard(self) -> dict:
        """Get monitoring dashboard data."""
        metrics = self.collect_metrics()
        api_projections = self.api_tracker.get_cost_projections()

        return {
            "health_score": metrics["health_score"],
            "components": {
                "cyclotron": metrics.get("cyclotron", {}),
                "brain": metrics.get("brain", {}),
                "disk": metrics.get("disk", {}),
                "api": metrics.get("api", {})
            },
            "api_projections": api_projections,
            "active_alerts": len(self.alerts["active"]),
            "timestamp": metrics["timestamp"]
        }


def demo():
    """Demonstrate monitoring system."""
    print("=" * 60)
    print("UNIFIED MONITORING SYSTEM")
    print("=" * 60)

    monitor = SystemMonitor()

    # Collect metrics
    print("\n1. Collecting metrics...")
    metrics = monitor.collect_metrics()

    print(f"\nHealth Score: {metrics['health_score']:.1f}%")

    # Show components
    print("\n2. Component Status:")
    for component in ["cyclotron", "brain", "disk", "api"]:
        data = metrics.get(component, {})
        status = "✅" if data.get("healthy") else "❌"
        print(f"   {status} {component}: {data}")

    # API tracking demo
    print("\n3. API Usage Tracking...")
    api = monitor.api_tracker

    # Simulate some usage
    api.log_usage("claude-3-sonnet", 1000, 500)
    api.log_usage("claude-3-sonnet", 2000, 1000)

    report = api.get_daily_report(7)
    print(f"   Total cost: ${report['total_cost']:.4f}")
    print(f"   Total calls: {report['total_calls']}")

    # Projections
    projections = api.get_cost_projections()
    if "error" not in projections:
        print(f"   Projected monthly: ${projections['projected_monthly']:.2f}")

    # Dashboard
    print("\n4. Dashboard Summary:")
    dashboard = monitor.get_dashboard()
    print(f"   Health: {dashboard['health_score']:.1f}%")
    print(f"   Active alerts: {dashboard['active_alerts']}")


def main():
    """CLI for monitoring."""
    import sys

    monitor = SystemMonitor()

    if len(sys.argv) < 2:
        print("Unified Monitoring System")
        print("=" * 40)
        print("\nCommands:")
        print("  status     - Show current status")
        print("  collect    - Collect metrics")
        print("  api        - Show API usage")
        print("  dashboard  - Full dashboard")
        print("  demo       - Run demo")
        return

    command = sys.argv[1]

    if command == "demo":
        demo()

    elif command == "status":
        metrics = monitor.collect_metrics()
        print(f"\nHealth Score: {metrics['health_score']:.1f}%")
        for comp, data in metrics.items():
            if isinstance(data, dict) and "healthy" in data:
                status = "✅" if data["healthy"] else "❌"
                print(f"{status} {comp}")

    elif command == "collect":
        metrics = monitor.collect_metrics()
        print(json.dumps(metrics, indent=2))

    elif command == "api":
        report = monitor.api_tracker.get_daily_report(7)
        print(f"\nAPI Usage (7 days):")
        print(f"  Total cost: ${report['total_cost']:.4f}")
        print(f"  Total calls: {report['total_calls']}")
        print(f"  Total tokens: {report['total_tokens']}")

    elif command == "dashboard":
        dashboard = monitor.get_dashboard()
        print(f"\nMonitoring Dashboard")
        print(f"{'=' * 40}")
        print(f"Health: {dashboard['health_score']:.1f}%")
        print(f"Alerts: {dashboard['active_alerts']}")
        print(f"\nComponents:")
        for comp, data in dashboard['components'].items():
            status = "✅" if data.get("healthy") else "❌"
            print(f"  {status} {comp}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
