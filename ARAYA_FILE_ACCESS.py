"""
ARAYA FILE ACCESS LAYER
Secure file operations with whitelisting, backups, and audit logging.

Built by C1×C2 - Structure + Security + Speed
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

class ArayaFileAccess:
    """Secure file access layer for ARAYA with whitelisting and audit logging."""

    # Base directory - everything relative to this
    BASE_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT")

    # Whitelist - allowed file patterns
    ALLOWED_PATTERNS = [
        "*.html",
        "*.md",
        "*.css",
        "*.js",
        "*.json",  # Allow JSON for data files
        "*.txt"    # Allow text files for ARAYA notes/content
    ]

    # Blacklist - NEVER allow edits to these
    FORBIDDEN_PATHS = [
        ".env*",
        "netlify/functions/*",
        ".git/*",
        "*.py",  # No Python edits via ARAYA for security
        ".secrets/*",
        ".araya_edits.log"  # Can't edit own audit log
    ]

    # Audit log location
    AUDIT_LOG = BASE_DIR / ".araya_edits.log"

    def __init__(self):
        """Initialize file access layer."""
        # Ensure audit log exists
        if not self.AUDIT_LOG.exists():
            self.AUDIT_LOG.touch()
            self._log_action("SYSTEM", "INIT", "Audit log created", {"success": True})

    def _is_path_allowed(self, file_path: str) -> Tuple[bool, str]:
        """
        Check if a file path is allowed for editing.

        Returns:
            (allowed: bool, reason: str)
        """
        try:
            # Convert to Path and resolve
            full_path = (self.BASE_DIR / file_path).resolve()

            # Must be within BASE_DIR
            if not str(full_path).startswith(str(self.BASE_DIR)):
                return False, "Path outside allowed directory"

            # Check blacklist first (higher priority)
            rel_path = full_path.relative_to(self.BASE_DIR)
            for forbidden in self.FORBIDDEN_PATHS:
                if rel_path.match(forbidden):
                    return False, f"Path matches forbidden pattern: {forbidden}"

            # Check whitelist
            allowed = False
            for pattern in self.ALLOWED_PATTERNS:
                if rel_path.match(pattern):
                    allowed = True
                    break

            if not allowed:
                return False, "File type not in whitelist"

            return True, "OK"

        except Exception as e:
            return False, f"Path validation error: {str(e)}"

    def _create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create backup of file before editing.

        Returns:
            Path to backup file, or None if backup failed
        """
        try:
            if not file_path.exists():
                return None  # No backup needed for new files

            # Backup naming: file.ext.backup.TIMESTAMP
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup.{timestamp}")

            shutil.copy2(file_path, backup_path)
            return backup_path

        except Exception as e:
            self._log_action("BACKUP", "ERROR", str(file_path), {
                "error": str(e),
                "success": False
            })
            return None

    def _log_action(self, action_type: str, operation: str, target: str, metadata: Dict):
        """Log action to audit log."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": action_type,
                "operation": operation,
                "target": target,
                "metadata": metadata
            }

            with open(self.AUDIT_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")

        except Exception as e:
            print(f"CRITICAL: Audit log write failed: {e}")

    def read_file(self, file_path: str) -> Tuple[bool, Optional[str], str]:
        """
        Read file contents.

        Returns:
            (success: bool, content: Optional[str], message: str)
        """
        allowed, reason = self._is_path_allowed(file_path)
        if not allowed:
            self._log_action("READ", "BLOCKED", file_path, {
                "reason": reason,
                "success": False
            })
            return False, None, f"Access denied: {reason}"

        try:
            full_path = self.BASE_DIR / file_path

            if not full_path.exists():
                return False, None, "File does not exist"

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            self._log_action("READ", "SUCCESS", file_path, {
                "size": len(content),
                "success": True
            })

            return True, content, "OK"

        except Exception as e:
            error_msg = str(e)
            self._log_action("READ", "ERROR", file_path, {
                "error": error_msg,
                "success": False
            })
            return False, None, error_msg

    def write_file(self, file_path: str, content: str, backup: bool = True) -> Tuple[bool, str]:
        """
        Write content to file with optional backup.

        Returns:
            (success: bool, message: str)
        """
        allowed, reason = self._is_path_allowed(file_path)
        if not allowed:
            self._log_action("WRITE", "BLOCKED", file_path, {
                "reason": reason,
                "success": False
            })
            return False, f"Access denied: {reason}"

        try:
            full_path = self.BASE_DIR / file_path

            # Create backup if file exists and backup requested
            backup_path = None
            if backup and full_path.exists():
                backup_path = self._create_backup(full_path)
                if backup_path is None:
                    return False, "Backup creation failed - write aborted for safety"

            # Ensure parent directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            self._log_action("WRITE", "SUCCESS", file_path, {
                "size": len(content),
                "backup": str(backup_path) if backup_path else None,
                "success": True
            })

            return True, "OK"

        except Exception as e:
            error_msg = str(e)
            self._log_action("WRITE", "ERROR", file_path, {
                "error": error_msg,
                "success": False
            })
            return False, error_msg

    def list_backups(self, file_path: str) -> List[Path]:
        """List all backups for a given file."""
        try:
            full_path = self.BASE_DIR / file_path
            backup_pattern = f"{full_path.name}.backup.*"
            backups = list(full_path.parent.glob(backup_pattern))
            backups.sort(reverse=True)  # Newest first
            return backups
        except Exception:
            return []

    def rollback(self, file_path: str, backup_index: int = 0) -> Tuple[bool, str]:
        """
        Restore file from backup.

        Args:
            file_path: Target file to restore
            backup_index: Which backup to use (0 = newest, 1 = second newest, etc.)

        Returns:
            (success: bool, message: str)
        """
        allowed, reason = self._is_path_allowed(file_path)
        if not allowed:
            return False, f"Access denied: {reason}"

        try:
            backups = self.list_backups(file_path)

            if not backups:
                return False, "No backups found"

            if backup_index >= len(backups):
                return False, f"Backup index {backup_index} out of range (only {len(backups)} backups)"

            backup_to_restore = backups[backup_index]
            full_path = self.BASE_DIR / file_path

            # Create backup of current state before rollback
            current_backup = self._create_backup(full_path)

            # Restore from backup
            shutil.copy2(backup_to_restore, full_path)

            self._log_action("ROLLBACK", "SUCCESS", file_path, {
                "restored_from": str(backup_to_restore),
                "current_backed_up_to": str(current_backup),
                "success": True
            })

            return True, f"Restored from {backup_to_restore.name}"

        except Exception as e:
            error_msg = str(e)
            self._log_action("ROLLBACK", "ERROR", file_path, {
                "error": error_msg,
                "success": False
            })
            return False, error_msg

    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Get recent audit log entries."""
        try:
            with open(self.AUDIT_LOG, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Get last N lines
            recent = lines[-limit:] if len(lines) > limit else lines

            # Parse JSON
            entries = []
            for line in recent:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    pass

            return entries

        except Exception:
            return []

    def list_allowed_files(self, pattern: str = "*") -> List[str]:
        """
        List all files that ARAYA is allowed to edit.

        Args:
            pattern: Glob pattern to filter (e.g., "*.html")

        Returns:
            List of relative file paths
        """
        allowed_files = []

        try:
            # Search for files matching allowed patterns
            for allowed_pattern in self.ALLOWED_PATTERNS:
                if pattern != "*" and not Path(pattern).match(allowed_pattern):
                    continue

                files = self.BASE_DIR.glob(allowed_pattern)
                for file in files:
                    rel_path = file.relative_to(self.BASE_DIR)

                    # Check not in blacklist
                    allowed, _ = self._is_path_allowed(str(rel_path))
                    if allowed:
                        allowed_files.append(str(rel_path))

            return sorted(allowed_files)

        except Exception:
            return []

# Global instance for easy importing
araya_files = ArayaFileAccess()

# Convenience functions
def read(file_path: str) -> Tuple[bool, Optional[str], str]:
    """Read file - convenience wrapper."""
    return araya_files.read_file(file_path)

def write(file_path: str, content: str, backup: bool = True) -> Tuple[bool, str]:
    """Write file - convenience wrapper."""
    return araya_files.write_file(file_path, content, backup)

def rollback(file_path: str, backup_index: int = 0) -> Tuple[bool, str]:
    """Rollback file - convenience wrapper."""
    return araya_files.rollback(file_path, backup_index)

def list_files(pattern: str = "*.html") -> List[str]:
    """List allowed files - convenience wrapper."""
    return araya_files.list_allowed_files(pattern)

def get_logs(limit: int = 100) -> List[Dict]:
    """Get audit logs - convenience wrapper."""
    return araya_files.get_audit_log(limit)

if __name__ == "__main__":
    print("ARAYA File Access Layer - Loaded")
    print(f"Base directory: {ArayaFileAccess.BASE_DIR}")
    print(f"Audit log: {ArayaFileAccess.AUDIT_LOG}")
    print(f"\nAllowed patterns: {ArayaFileAccess.ALLOWED_PATTERNS}")
    print(f"Forbidden paths: {ArayaFileAccess.FORBIDDEN_PATHS}")
