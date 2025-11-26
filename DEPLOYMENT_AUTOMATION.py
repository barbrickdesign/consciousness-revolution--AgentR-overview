#!/usr/bin/env python3
"""
AUTOMATED DEPLOYMENT & RECOVERY SYSTEM
- Blue-green deployments
- Health checks before/after
- Automatic rollback on failure
- Self-healing restarts
"""

import subprocess
import json
import time
import threading
import psutil
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

DEPLOYMENT_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT")
BACKUP_DIR = DEPLOYMENT_DIR / ".backups"
STATUS_FILE = DEPLOYMENT_DIR / "deployment_status.json"
LOG_DIR = DEPLOYMENT_DIR / ".deployment_logs"

BACKUP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

DB_PATH = "C:/Users/dwrek/.consciousness/cyclotron_core/atoms.db"


class DeploymentManager:
    """Manage application deployments with rollback support."""

    def __init__(self):
        self.current_version = None
        self.deployments = []
        self.load_status()

    def load_status(self):
        """Load deployment status from file."""
        if STATUS_FILE.exists():
            try:
                with open(STATUS_FILE) as f:
                    data = json.load(f)
                    self.current_version = data.get('current_version')
                    self.deployments = data.get('deployments', [])
            except Exception as e:
                print(f"[DEPLOY] Error loading status: {e}")

    def save_status(self):
        """Save deployment status to file."""
        with open(STATUS_FILE, 'w') as f:
            json.dump({
                'current_version': self.current_version,
                'deployments': self.deployments[-20:],  # Keep last 20
                'updated': datetime.now().isoformat()
            }, f, indent=2)

    def deploy(self, version: str, services: List[str]) -> Dict:
        """Deploy new version with blue-green strategy."""

        log_file = LOG_DIR / f"deploy_{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log = self._create_logger(log_file)

        log.write(f"\n{'='*70}\n")
        log.write(f"DEPLOYMENT: {version}\n")
        log.write(f"Services: {', '.join(services)}\n")
        log.write(f"Time: {datetime.now().isoformat()}\n")
        log.write(f"{'='*70}\n\n")

        try:
            # Step 1: Backup current
            log.write("[STEP 1] Backing up current version...\n")
            backup_path = self._backup_current()
            if not backup_path:
                log.write("  ERROR: Backup failed\n")
                log.write(f"\nDEPLOYMENT FAILED\n")
                return {'success': False, 'error': 'Backup failed', 'log': str(log_file)}

            log.write(f"  OK - Backup: {backup_path}\n\n")

            # Step 2: Health check (before)
            log.write("[STEP 2] Health check (current state)...\n")
            health_before = self._health_check(log)
            log.write(f"  Status: {'PASS' if health_before['healthy'] else 'FAIL'}\n\n")

            # Step 3: Deploy new version
            log.write(f"[STEP 3] Deploying version {version}...\n")
            deploy_ok = self._deploy_services(services, log)

            if not deploy_ok:
                log.write("  ERROR: Deployment failed - Rolling back...\n")
                self._rollback(backup_path, log)
                log.write(f"\nDEPLOYMENT FAILED (ROLLED BACK)\n")
                return {
                    'success': False,
                    'error': 'Deployment failed, rolled back',
                    'log': str(log_file)
                }

            log.write(f"  OK - Version {version} deployed\n\n")

            # Step 4: Health check (after)
            log.write("[STEP 4] Health check (new state)...\n")
            health_after = self._health_check(log)

            if not health_after['healthy']:
                log.write("  FAIL - Health check failed - Rolling back...\n")
                self._rollback(backup_path, log)
                log.write(f"\nDEPLOYMENT FAILED (HEALTH CHECK, ROLLED BACK)\n")
                return {
                    'success': False,
                    'error': 'Health check failed, rolled back',
                    'log': str(log_file)
                }

            log.write(f"  OK - Health checks passed\n\n")

            # Step 5: Activate
            log.write("[STEP 5] Activating new version...\n")
            self.current_version = version
            self.save_status()

            # Record deployment
            self.deployments.append({
                'version': version,
                'timestamp': datetime.now().isoformat(),
                'services': services,
                'health_before': health_before,
                'health_after': health_after,
                'status': 'success',
                'backup': str(backup_path)
            })
            self.save_status()

            log.write(f"  OK - Version {version} activated\n\n")
            log.write(f"DEPLOYMENT SUCCESSFUL: {version}\n")

            return {
                'success': True,
                'version': version,
                'health_before': health_before,
                'health_after': health_after,
                'log': str(log_file),
                'backup': str(backup_path)
            }

        except Exception as e:
            log.write(f"\nEXCEPTION: {e}\n")
            log.write(f"DEPLOYMENT FAILED\n")
            return {'success': False, 'error': str(e), 'log': str(log_file)}
        finally:
            log.close()

    def _create_logger(self, log_file: Path):
        """Create a simple logger object."""
        class Logger:
            def __init__(self, path):
                self.path = path
                self.file = open(path, 'w')

            def write(self, msg: str):
                self.file.write(msg)
                self.file.flush()
                print(msg, end='')

            def close(self):
                self.file.close()

        return Logger(log_file)

    def _backup_current(self) -> Optional[Path]:
        """Backup current database and configs."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)

            # Backup database
            if Path(DB_PATH).exists():
                shutil.copy2(DB_PATH, backup_path / "atoms.db")

            # Backup cache
            cache_dir = Path("C:/Users/dwrek/.consciousness/cache")
            if cache_dir.exists():
                shutil.copytree(
                    cache_dir,
                    backup_path / "cache",
                    dirs_exist_ok=True
                )

            return backup_path
        except Exception as e:
            print(f"[DEPLOY] Backup failed: {e}")
            return None

    def _deploy_services(self, services: List[str], log) -> bool:
        """Deploy services."""
        try:
            for service in services:
                log.write(f"  Deploying {service}...\n")

                # Find and run service startup script
                script = DEPLOYMENT_DIR / f"START_{service}.bat"
                if script.exists():
                    subprocess.run(
                        str(script),
                        shell=True,
                        timeout=60,
                        capture_output=True
                    )
                    time.sleep(2)  # Give service time to start
                else:
                    log.write(f"    WARNING: Startup script not found\n")

            return True
        except Exception as e:
            log.write(f"  ERROR: {e}\n")
            return False

    def _health_check(self, log) -> Dict:
        """Perform system health checks."""
        checks = {
            'database': self._check_database(log),
            'system': self._check_system(log),
            'timestamp': datetime.now().isoformat()
        }

        checks['healthy'] = all(
            checks.get(k, False) for k in ['database', 'system']
        )

        return checks

    def _check_database(self, log) -> bool:
        """Check database availability."""
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH, timeout=5)
            conn.execute("SELECT COUNT(*) FROM atoms")
            count = conn.fetchone()[0]
            conn.close()

            log.write(f"    Database: OK ({count} atoms)\n")
            return True
        except Exception as e:
            log.write(f"    Database: FAIL - {e}\n")
            return False

    def _check_system(self, log) -> bool:
        """Check system resource availability."""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('C:').percent

            log.write(f"    System: CPU {cpu}%, Memory {memory}%, Disk {disk}%\n")

            # Fail if resources critical
            if cpu > 95 or memory > 95 or disk > 95:
                log.write(f"    System: FAIL - Resources critical\n")
                return False

            return True
        except Exception as e:
            log.write(f"    System: FAIL - {e}\n")
            return False

    def _rollback(self, backup_path: Path, log):
        """Rollback to previous version."""
        try:
            log.write(f"  Rolling back from: {backup_path}\n")

            # Restore database
            if (backup_path / "atoms.db").exists():
                shutil.copy2(
                    backup_path / "atoms.db",
                    DB_PATH
                )
                log.write(f"  Restored database\n")

            # Restore cache
            if (backup_path / "cache").exists():
                cache_dir = Path("C:/Users/dwrek/.consciousness/cache")
                shutil.rmtree(cache_dir, ignore_errors=True)
                shutil.copytree(
                    backup_path / "cache",
                    cache_dir
                )
                log.write(f"  Restored cache\n")

            log.write(f"  Rollback complete\n")
            return True
        except Exception as e:
            log.write(f"  Rollback failed: {e}\n")
            return False


class SelfHealingMonitor:
    """Monitor services and auto-restart if unhealthy."""

    def __init__(self, services: List[str], check_interval: int = 60):
        self.services = services
        self.check_interval = check_interval
        self.restart_counts = {}
        self.is_running = False

    def start(self):
        """Start self-healing monitoring."""
        self.is_running = True
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()
        print(f"[HEAL] Self-healing monitor started ({len(self.services)} services)")

    def stop(self):
        """Stop monitoring."""
        self.is_running = False

    def _monitor_loop(self):
        """Continuous monitoring loop."""
        while self.is_running:
            try:
                for service in self.services:
                    if not self._is_healthy(service):
                        count = self.restart_counts.get(service, 0)
                        print(f"[HEAL] {service} unhealthy - restart #{count + 1}")

                        if self._restart_service(service):
                            self.restart_counts[service] = count + 1
                        else:
                            print(f"[HEAL] Failed to restart {service}")

            except Exception as e:
                print(f"[HEAL] Monitor error: {e}")

            time.sleep(self.check_interval)

    def _is_healthy(self, service: str) -> bool:
        """Check if service is healthy."""
        try:
            # Check if process is running
            for proc in psutil.process_iter(['pid', 'name']):
                if service.lower() in proc.info['name'].lower():
                    return True
            return False
        except:
            return False

    def _restart_service(self, service: str) -> bool:
        """Restart a service."""
        try:
            script = DEPLOYMENT_DIR / f"START_{service}.bat"
            if script.exists():
                subprocess.Popen(
                    str(script),
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(5)  # Wait for startup
                return True
            return False
        except Exception as e:
            print(f"[HEAL] Restart failed: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get monitoring statistics."""
        return {
            'is_running': self.is_running,
            'services': self.services,
            'restart_counts': self.restart_counts,
            'timestamp': datetime.now().isoformat()
        }


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════╗")
    print("║  DEPLOYMENT & RECOVERY SYSTEM         ║")
    print("╚════════════════════════════════════════╝\n")

    manager = DeploymentManager()

    print(f"Current version: {manager.current_version}")
    print(f"Recent deployments: {len(manager.deployments)}\n")

    # Example: Deploy new version
    print("Example deployment (simulated):\n")
    print("result = manager.deploy(")
    print("    version='1.2.0',")
    print("    services=['CYCLOTRON_DAEMON', 'CYCLOTRON_SEMANTIC_API']")
    print(")\n")

    # Start self-healing monitor (example)
    print("Starting self-healing monitor...\n")
    healer = SelfHealingMonitor(
        services=["CYCLOTRON_DAEMON"],
        check_interval=60
    )
    healer.start()

    try:
        # Keep alive for monitoring
        while True:
            stats = healer.get_stats()
            time.sleep(300)  # Update stats every 5 minutes
    except KeyboardInterrupt:
        print("\n[DEPLOY] Shutting down...")
        healer.stop()
