#!/usr/bin/env python3
"""
REAL-TIME MONITORING SYSTEM
Dashboard + alerting for Cyclotron infrastructure.

Monitors:
- Database health (size, atom count, query performance)
- API performance (response times, error rates)
- Cache effectiveness (hit rates, memory usage)
- System resources (CPU, memory, disk)
- Error patterns
"""

import json
import sqlite3
import psutil
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque

MONITORING_DIR = Path("C:/Users/dwrek/.consciousness/monitoring")
MONITORING_DIR.mkdir(exist_ok=True)

ALERT_FILE = MONITORING_DIR / "alerts.json"
METRICS_FILE = MONITORING_DIR / "metrics.json"
DASHBOARD_FILE = MONITORING_DIR / "dashboard.html"
CACHE_STATS_FILE = MONITORING_DIR / "cache_stats.json"

DB_PATH = "C:/Users/dwrek/.consciousness/cyclotron_core/atoms.db"


class SystemMetrics:
    """Collect system health metrics."""

    def __init__(self):
        self.metrics = deque(maxlen=1440)  # 24 hours at 1-min intervals
        self.alerts = deque(maxlen=100)

    def collect_metrics(self) -> dict:
        """Collect all system metrics."""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'database': self._collect_db_metrics(),
            'system': self._collect_system_metrics(),
            'cache': self._collect_cache_metrics()
        }

        self.metrics.append(metrics)
        return metrics

    def _collect_db_metrics(self) -> dict:
        """Collect database metrics."""
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5)
            cursor = conn.cursor()

            # Count atoms
            cursor.execute("SELECT COUNT(*) FROM atoms")
            atom_count = cursor.fetchone()[0]

            # Get breakdown by type
            cursor.execute("""
                SELECT type, COUNT(*) as count
                FROM atoms
                GROUP BY type
            """)
            by_type = {row[0]: row[1] for row in cursor.fetchall()}

            conn.close()

            # Database file size
            db_size_bytes = Path(DB_PATH).stat().st_size
            db_size_mb = round(db_size_bytes / (1024 * 1024), 2)

            return {
                'atom_count': atom_count,
                'db_size_mb': db_size_mb,
                'by_type': by_type,
                'status': 'healthy' if atom_count > 0 else 'degraded'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error',
                'atom_count': 0
            }

    def _collect_system_metrics(self) -> dict:
        """Collect system resource metrics."""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory
            memory = psutil.virtual_memory()

            # Disk
            disk = psutil.disk_usage('C:')

            # Determine status
            status = 'healthy'
            if cpu_percent > 80 or memory.percent > 85 or disk.percent > 85:
                status = 'warning'
            if cpu_percent > 95 or memory.percent > 95 or disk.percent > 95:
                status = 'critical'

            return {
                'cpu_percent': round(cpu_percent, 1),
                'memory_percent': round(memory.percent, 1),
                'memory_available_mb': round(memory.available / (1024*1024), 1),
                'disk_percent': round(disk.percent, 1),
                'disk_free_gb': round(disk.free / (1024*1024*1024), 1),
                'status': status
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def _collect_cache_metrics(self) -> dict:
        """Collect cache effectiveness metrics."""
        try:
            cache_stats_path = Path("C:/Users/dwrek/.consciousness/cache/cache_stats.json")

            if cache_stats_path.exists():
                with open(cache_stats_path) as f:
                    cache_stats = json.load(f)

                return {
                    'hit_rate_percent': cache_stats.get('hit_rate', 0),
                    'memory_hits': cache_stats.get('memory_hits', 0),
                    'filesystem_hits': cache_stats.get('filesystem_hits', 0),
                    'database_hits': cache_stats.get('database_hits', 0),
                    'total_requests': cache_stats.get('total_requests', 0),
                    'status': 'healthy' if cache_stats.get('hit_rate', 0) > 50 else 'degraded'
                }
            else:
                return {
                    'hit_rate_percent': 0,
                    'status': 'disabled'
                }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

    def check_alerts(self, metrics: dict) -> list:
        """Check metrics against alert thresholds."""
        alerts = []

        # Database alerts
        db = metrics.get('database', {})
        if db.get('atom_count', 0) == 0:
            alerts.append({
                'severity': 'critical',
                'category': 'database',
                'message': 'No atoms in database',
                'timestamp': datetime.now().isoformat()
            })

        # System alerts
        sys = metrics.get('system', {})

        if sys.get('cpu_percent', 0) > 90:
            alerts.append({
                'severity': 'warning',
                'category': 'system',
                'message': f"High CPU: {sys['cpu_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        if sys.get('memory_percent', 0) > 90:
            alerts.append({
                'severity': 'warning',
                'category': 'system',
                'message': f"High memory: {sys['memory_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        if sys.get('disk_percent', 0) > 85:
            alerts.append({
                'severity': 'warning',
                'category': 'system',
                'message': f"Disk low: {sys['disk_percent']}% full",
                'timestamp': datetime.now().isoformat()
            })

        # Cache alerts
        cache = metrics.get('cache', {})
        if cache.get('hit_rate_percent', 0) < 30 and cache.get('total_requests', 0) > 10:
            alerts.append({
                'severity': 'warning',
                'category': 'cache',
                'message': f"Low cache hit rate: {cache['hit_rate_percent']}%",
                'timestamp': datetime.now().isoformat()
            })

        return alerts

    def save_metrics(self):
        """Save latest metrics to file."""
        if self.metrics:
            latest = list(self.metrics)[-1]
            with open(METRICS_FILE, 'w') as f:
                json.dump(latest, f, indent=2)

    def save_alerts(self, alerts: list):
        """Save alerts to file."""
        self.alerts.extend(alerts)

        with open(ALERT_FILE, 'w') as f:
            json.dump({
                'alerts': list(self.alerts),
                'updated': datetime.now().isoformat(),
                'critical_count': sum(1 for a in self.alerts if a['severity'] == 'critical'),
                'warning_count': sum(1 for a in self.alerts if a['severity'] == 'warning')
            }, f, indent=2)

    def generate_dashboard(self) -> str:
        """Generate HTML dashboard."""
        latest = list(self.metrics)[-1] if self.metrics else {}
        recent = list(self.metrics)[-10:] if self.metrics else []

        db = latest.get('database', {})
        sys = latest.get('system', {})
        cache = latest.get('cache', {})

        # Calculate trends
        cpu_trend = "↑" if len(recent) > 1 and recent[-1].get('system', {}).get('cpu_percent', 0) > recent[-2].get('system', {}).get('cpu_percent', 0) else "↓"
        mem_trend = "↑" if len(recent) > 1 and recent[-1].get('system', {}).get('memory_percent', 0) > recent[-2].get('system', {}).get('memory_percent', 0) else "↓"

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cyclotron Monitoring Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0e27;
            color: #00ff41;
            padding: 20px;
            line-height: 1.4;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; margin-bottom: 20px; font-size: 24px; text-shadow: 0 0 10px #00ff41; }}
        .timestamp {{ text-align: center; color: #888; font-size: 12px; margin-bottom: 20px; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{
            background: #1a1f3a;
            border: 2px solid #00ff41;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
        }}
        .card-title {{ font-weight: bold; font-size: 14px; margin-bottom: 15px; border-bottom: 1px solid #00ff41; padding-bottom: 10px; }}
        .metric {{ margin: 10px 0; display: flex; justify-content: space-between; }}
        .metric-label {{ color: #888; }}
        .metric-value {{ color: #00ff41; font-weight: bold; }}

        .healthy {{ color: #00ff41; }}
        .warning {{ color: #ffaa00; }}
        .critical {{ color: #ff4444; }}
        .error {{ color: #ff4444; }}

        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #0a0e27;
            border: 1px solid #00ff41;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff41, #00aa00);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            color: black;
            font-weight: bold;
        }}

        .alerts {{ margin-top: 30px; }}
        .alert {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            border-left: 4px solid;
        }}
        .alert.critical {{ border-left-color: #ff4444; background: rgba(255, 68, 68, 0.1); }}
        .alert.warning {{ border-left-color: #ffaa00; background: rgba(255, 170, 0, 0.1); }}
        .alert.info {{ border-left-color: #00ff41; background: rgba(0, 255, 65, 0.1); }}

        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
            margin: 5px 0;
        }}
        .status-healthy {{ background: #00ff41; color: #000; }}
        .status-warning {{ background: #ffaa00; color: #000; }}
        .status-critical {{ background: #ff4444; color: #fff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ CYCLOTRON MONITORING DASHBOARD ⚡</h1>
        <div class="timestamp">Updated: {latest.get('timestamp', 'N/A')}</div>

        <div class="grid">
            <!-- DATABASE CARD -->
            <div class="card">
                <div class="card-title">📊 DATABASE</div>
                <div class="metric">
                    <span class="metric-label">Total Atoms:</span>
                    <span class="metric-value">{db.get('atom_count', 0):,}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Size:</span>
                    <span class="metric-value">{db.get('db_size_mb', 0)} MB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value {db.get('status', 'error')}">{db.get('status', 'unknown').upper()}</span>
                </div>
                {_render_atom_breakdown(db.get('by_type', {}))}
            </div>

            <!-- SYSTEM RESOURCES CARD -->
            <div class="card">
                <div class="card-title">💻 SYSTEM RESOURCES</div>
                <div class="metric">
                    <span class="metric-label">CPU:</span>
                    <span class="metric-value">{sys.get('cpu_percent', 0)}% {cpu_trend}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {sys.get('cpu_percent', 0)}%">{sys.get('cpu_percent', 0)}%</div>
                </div>

                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Memory:</span>
                    <span class="metric-value">{sys.get('memory_percent', 0)}% {mem_trend}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {sys.get('memory_percent', 0)}%">{sys.get('memory_percent', 0)}%</div>
                </div>

                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Disk:</span>
                    <span class="metric-value">{sys.get('disk_percent', 0)}% ({sys.get('disk_free_gb', 0)} GB free)</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {sys.get('disk_percent', 0)}%">{sys.get('disk_percent', 0)}%</div>
                </div>

                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value {sys.get('status', 'error')}">{sys.get('status', 'unknown').upper()}</span>
                </div>
            </div>

            <!-- CACHE PERFORMANCE CARD -->
            <div class="card">
                <div class="card-title">⚙️ CACHE PERFORMANCE</div>
                <div class="metric">
                    <span class="metric-label">Hit Rate:</span>
                    <span class="metric-value">{cache.get('hit_rate_percent', 0)}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {cache.get('hit_rate_percent', 0)}%">{cache.get('hit_rate_percent', 0)}%</div>
                </div>

                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Memory Hits:</span>
                    <span class="metric-value">{cache.get('memory_hits', 0):,}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Disk Hits:</span>
                    <span class="metric-value">{cache.get('filesystem_hits', 0):,}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">DB Hits:</span>
                    <span class="metric-value">{cache.get('database_hits', 0):,}</span>
                </div>

                <div class="metric" style="margin-top: 15px;">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value {cache.get('status', 'error')}">{cache.get('status', 'unknown').upper()}</span>
                </div>
            </div>
        </div>

        {_render_alerts_section(list(self.alerts))}
    </div>
</body>
</html>
"""
        return html


def _render_atom_breakdown(by_type: dict) -> str:
    """Render atom type breakdown."""
    html = '<div style="margin-top: 15px; font-size: 12px;">'
    for atom_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        html += f'<div>{atom_type}: <span class="metric-value">{count}</span></div>'
    html += '</div>'
    return html


def _render_alerts_section(alerts: list) -> str:
    """Render alerts section."""
    if not alerts:
        return '<div class="alerts"><div class="alert info">No alerts</div></div>'

    html = '<div class="alerts"><div class="card-title">⚠️ RECENT ALERTS</div>'

    # Group by severity
    critical = [a for a in alerts if a['severity'] == 'critical']
    warnings = [a for a in alerts if a['severity'] == 'warning']

    for alert in critical[-5:]:
        html += f'<div class="alert critical"><strong>CRITICAL:</strong> {alert["message"]}</div>'

    for alert in warnings[-5:]:
        html += f'<div class="alert warning"><strong>WARNING:</strong> {alert["message"]}</div>'

    html += '</div>'
    return html


def monitoring_loop(monitor: SystemMetrics):
    """Continuous monitoring loop."""
    print("[MONITOR] Starting monitoring loop (interval: 60 seconds)")

    while True:
        try:
            # Collect metrics
            metrics = monitor.collect_metrics()

            # Check alerts
            alerts = monitor.check_alerts(metrics)

            # Save results
            monitor.save_metrics()
            monitor.save_alerts(alerts)

            # Generate dashboard
            dashboard_html = monitor.generate_dashboard()
            with open(DASHBOARD_FILE, 'w') as f:
                f.write(dashboard_html)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Metrics collected")

            if alerts:
                critical = sum(1 for a in alerts if a['severity'] == 'critical')
                warning = sum(1 for a in alerts if a['severity'] == 'warning')
                print(f"  ⚠️  ALERTS: {critical} critical, {warning} warning")

        except Exception as e:
            print(f"[ERROR] Monitoring failed: {e}")

        # Sample every 60 seconds
        time.sleep(60)


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════╗")
    print("║  CYCLOTRON MONITORING SYSTEM          ║")
    print("╚════════════════════════════════════════╝\n")

    print(f"[MONITOR] Dashboard: {DASHBOARD_FILE}")
    print(f"[MONITOR] Metrics:   {METRICS_FILE}")
    print(f"[MONITOR] Alerts:    {ALERT_FILE}")

    monitor = SystemMetrics()

    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitoring_loop, args=(monitor,), daemon=True)
    monitor_thread.start()

    try:
        # Keep main thread alive
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n[MONITOR] Stopping...")
