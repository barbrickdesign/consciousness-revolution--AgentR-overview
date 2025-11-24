#!/usr/bin/env python3
"""
AUTOMATED BACKUP SYSTEM
Backup with rotation and verification.
Resolves foundational issue: missing_backup_system
"""

import json
import shutil
import hashlib
import gzip
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
PLANNING = HOME / ".planning"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
BACKUP_ROOT = HOME / ".backups"
BACKUP_ROOT.mkdir(parents=True, exist_ok=True)


class BackupSystem:
    """Automated backup with rotation and verification."""

    def __init__(self, retention_days: int = 30, max_backups: int = 10):
        self.retention_days = retention_days
        self.max_backups = max_backups
        self.backup_manifest = BACKUP_ROOT / "manifest.json"
        self._load_manifest()

    def _load_manifest(self):
        """Load backup manifest."""
        if self.backup_manifest.exists():
            try:
                with open(self.backup_manifest) as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    self.manifest = {
                        "backups": data.get("backups", []),
                        "last_backup": data.get("last_backup"),
                        "total_size": data.get("total_size", 0)
                    }
            except (json.JSONDecodeError, KeyError):
                self.manifest = {
                    "backups": [],
                    "last_backup": None,
                    "total_size": 0
                }
        else:
            self.manifest = {
                "backups": [],
                "last_backup": None,
                "total_size": 0
            }

    def _save_manifest(self):
        """Save backup manifest."""
        with open(self.backup_manifest, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def backup_directory(self, source_dir: Path, backup_name: str) -> dict:
        """Backup a directory with compression."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = BACKUP_ROOT / f"{backup_name}_{timestamp}"
        backup_dir.mkdir(parents=True)

        files_backed_up = 0
        total_size = 0
        checksums = {}

        # Walk directory and backup files
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                # Skip certain files
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', '.pyc', 'node_modules']):
                    continue

                # Create relative path
                rel_path = file_path.relative_to(source_dir)
                dest_path = backup_dir / rel_path

                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy and compress JSON files
                if file_path.suffix == '.json':
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(str(dest_path) + '.gz', 'wb') as f_out:
                            f_out.writelines(f_in)
                    checksums[str(rel_path)] = self._calculate_checksum(file_path)
                else:
                    shutil.copy2(file_path, dest_path)
                    checksums[str(rel_path)] = self._calculate_checksum(file_path)

                files_backed_up += 1
                total_size += file_path.stat().st_size

        # Save checksums
        with open(backup_dir / "checksums.json", 'w') as f:
            json.dump(checksums, f, indent=2)

        # Create backup record
        backup_record = {
            "name": backup_name,
            "timestamp": timestamp,
            "path": str(backup_dir),
            "source": str(source_dir),
            "files": files_backed_up,
            "size": total_size,
            "checksums": len(checksums)
        }

        self.manifest["backups"].append(backup_record)
        self.manifest["last_backup"] = timestamp
        self.manifest["total_size"] += total_size
        self._save_manifest()

        return backup_record

    def backup_all(self) -> dict:
        """Backup all critical directories."""
        print("=" * 60)
        print("AUTOMATED BACKUP SYSTEM")
        print("=" * 60)

        results = []

        # Backup consciousness
        print("\n1. Backing up .consciousness...")
        result = self.backup_directory(CONSCIOUSNESS, "consciousness")
        results.append(result)
        print(f"   {result['files']} files, {result['size'] / 1024:.1f} KB")

        # Backup planning
        print("\n2. Backing up .planning...")
        result = self.backup_directory(PLANNING, "planning")
        results.append(result)
        print(f"   {result['files']} files, {result['size'] / 1024:.1f} KB")

        # Backup key deployment files
        print("\n3. Backing up key deployment files...")
        key_files_dir = BACKUP_ROOT / "deployment_key_files"
        key_files_dir.mkdir(exist_ok=True)

        key_patterns = ["*.py", "*.json", "*.md"]
        key_count = 0
        for pattern in key_patterns:
            for f in DEPLOYMENT.glob(pattern):
                if f.is_file() and f.stat().st_size < 1_000_000:  # < 1MB
                    shutil.copy2(f, key_files_dir / f.name)
                    key_count += 1

        print(f"   {key_count} key files copied")

        # Rotate old backups
        self._rotate_backups()

        print("\n" + "=" * 60)
        print("BACKUP COMPLETE")
        print("=" * 60)
        print(f"Total backups: {len(self.manifest['backups'])}")
        print(f"Last backup: {self.manifest['last_backup']}")

        return {
            "backups": results,
            "total": len(results),
            "timestamp": datetime.now().isoformat()
        }

    def _rotate_backups(self):
        """Remove old backups based on retention policy."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        cutoff_str = cutoff.strftime("%Y%m%d_%H%M%S")

        removed = []
        kept = []

        for backup in self.manifest["backups"]:
            if backup["timestamp"] < cutoff_str:
                # Remove old backup
                backup_path = Path(backup["path"])
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                removed.append(backup["name"])
            else:
                kept.append(backup)

        # Also enforce max backups
        if len(kept) > self.max_backups:
            # Remove oldest
            kept.sort(key=lambda x: x["timestamp"])
            to_remove = kept[:-self.max_backups]
            kept = kept[-self.max_backups:]

            for backup in to_remove:
                backup_path = Path(backup["path"])
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                removed.append(backup["name"])

        self.manifest["backups"] = kept

        if removed:
            print(f"\nRotated {len(removed)} old backups")

        self._save_manifest()

    def verify_backup(self, backup_name: str = None) -> dict:
        """Verify backup integrity using checksums."""
        if not self.manifest["backups"]:
            return {"error": "No backups found"}

        # Get latest or specific backup
        if backup_name:
            backup = next((b for b in self.manifest["backups"] if b["name"] == backup_name), None)
        else:
            backup = self.manifest["backups"][-1]

        if not backup:
            return {"error": f"Backup {backup_name} not found"}

        backup_path = Path(backup["path"])
        checksums_file = backup_path / "checksums.json"

        if not checksums_file.exists():
            return {"error": "Checksums file missing"}

        with open(checksums_file) as f:
            original_checksums = json.load(f)

        # Verify source files still match
        source_dir = Path(backup["source"])
        verified = 0
        changed = []
        missing = []

        for rel_path, original_hash in original_checksums.items():
            source_file = source_dir / rel_path

            if not source_file.exists():
                missing.append(rel_path)
            else:
                current_hash = self._calculate_checksum(source_file)
                if current_hash == original_hash:
                    verified += 1
                else:
                    changed.append(rel_path)

        result = {
            "backup": backup["name"],
            "timestamp": backup["timestamp"],
            "verified": verified,
            "changed": len(changed),
            "missing": len(missing),
            "integrity": "OK" if not changed and not missing else "CHANGED"
        }

        if changed:
            result["changed_files"] = changed[:10]
        if missing:
            result["missing_files"] = missing[:10]

        return result

    def restore(self, backup_name: str = None, target_dir: Path = None) -> dict:
        """Restore from backup."""
        if not self.manifest["backups"]:
            return {"error": "No backups found"}

        # Get backup
        if backup_name:
            backup = next((b for b in self.manifest["backups"] if backup_name in b["name"]), None)
        else:
            backup = self.manifest["backups"][-1]

        if not backup:
            return {"error": f"Backup not found"}

        backup_path = Path(backup["path"])
        restore_target = target_dir or Path(backup["source"])

        print(f"Restoring {backup['name']} to {restore_target}...")

        restored = 0
        for file_path in backup_path.rglob("*"):
            if file_path.is_file() and file_path.name != "checksums.json":
                rel_path = file_path.relative_to(backup_path)

                # Handle gzipped files
                if file_path.suffix == '.gz':
                    dest_path = restore_target / str(rel_path)[:-3]
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with gzip.open(file_path, 'rb') as f_in:
                        with open(dest_path, 'wb') as f_out:
                            f_out.write(f_in.read())
                else:
                    dest_path = restore_target / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)

                restored += 1

        return {
            "backup": backup["name"],
            "restored_to": str(restore_target),
            "files": restored
        }

    def get_status(self) -> dict:
        """Get backup system status."""
        return {
            "total_backups": len(self.manifest["backups"]),
            "last_backup": self.manifest["last_backup"],
            "total_size_mb": self.manifest["total_size"] / (1024 * 1024),
            "retention_days": self.retention_days,
            "backups": [
                {
                    "name": b["name"],
                    "timestamp": b["timestamp"],
                    "files": b["files"]
                }
                for b in self.manifest["backups"][-5:]
            ]
        }


def main():
    """CLI for backup system."""
    import sys

    backup = BackupSystem()

    if len(sys.argv) < 2:
        print("Automated Backup System")
        print("=" * 40)
        print("\nCommands:")
        print("  backup     - Backup all critical directories")
        print("  verify     - Verify latest backup integrity")
        print("  restore    - Restore from latest backup")
        print("  status     - Show backup status")
        print("  list       - List all backups")
        return

    command = sys.argv[1]

    if command == "backup":
        backup.backup_all()

    elif command == "verify":
        result = backup.verify_backup()
        print(f"\nVerification: {result['integrity']}")
        print(f"  Verified: {result['verified']}")
        print(f"  Changed: {result['changed']}")
        print(f"  Missing: {result['missing']}")

    elif command == "restore":
        result = backup.restore()
        print(f"Restored {result['files']} files to {result['restored_to']}")

    elif command == "status":
        status = backup.get_status()
        print(f"\nBackup Status:")
        print(f"  Total backups: {status['total_backups']}")
        print(f"  Last backup: {status['last_backup']}")
        print(f"  Total size: {status['total_size_mb']:.2f} MB")

    elif command == "list":
        status = backup.get_status()
        print("\nRecent backups:")
        for b in status['backups']:
            print(f"  {b['timestamp']}: {b['name']} ({b['files']} files)")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
