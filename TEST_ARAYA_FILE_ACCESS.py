"""
ARAYA FILE ACCESS - TEST SUITE
Proves the security layer works correctly.

Tests:
1. Whitelist enforcement
2. Blacklist enforcement
3. Backup creation
4. Rollback functionality
5. Audit logging
"""

import os
import time
from ARAYA_FILE_ACCESS import araya_files, read, write, rollback, list_files, get_logs
from pathlib import Path

def print_test(name: str):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")

def print_result(success: bool, message: str):
    """Print test result."""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {message}")

def test_whitelist_allowed():
    """Test that allowed file types work."""
    print_test("Whitelist - Allowed Files")

    test_file = "test_allowed.html"
    test_content = "<html><body>Test</body></html>"

    # Write
    success, msg = write(test_file, test_content)
    print_result(success, f"Write HTML file: {msg}")

    # Read
    success, content, msg = read(test_file)
    print_result(success and content == test_content, f"Read HTML file: {msg}")

    # Cleanup
    try:
        (Path("C:/Users/dwrek/100X_DEPLOYMENT") / test_file).unlink()
        print("Cleanup: Removed test file")
    except:
        pass

def test_whitelist_blocked():
    """Test that blocked file types are rejected."""
    print_test("Whitelist - Blocked Files")

    # Try to write Python file (not allowed)
    success, msg = write("test_blocked.py", "print('hack')")
    print_result(not success, f"Block .py file: {msg}")

    # Try to write .env file (forbidden)
    success, msg = write(".env", "SECRET=hack")
    print_result(not success, f"Block .env file: {msg}")

    # Try to write to .git (forbidden)
    success, msg = write(".git/config", "hack")
    print_result(not success, f"Block .git/ access: {msg}")

def test_path_traversal():
    """Test that path traversal attacks are blocked."""
    print_test("Path Traversal Protection")

    # Try to escape BASE_DIR
    success, msg = write("../../../etc/passwd", "hack")
    print_result(not success, f"Block path traversal: {msg}")

    # Try to access secrets
    success, msg = write(".secrets/MASTER_KEYS.json", "hack")
    print_result(not success, f"Block .secrets/ access: {msg}")

def test_backup_creation():
    """Test that backups are created before edits."""
    print_test("Backup Creation")

    test_file = "test_backup.html"
    base_path = Path("C:/Users/dwrek/100X_DEPLOYMENT")
    full_path = base_path / test_file

    # Create initial file
    success, msg = write(test_file, "Version 1", backup=False)
    print_result(success, f"Create initial file: {msg}")

    time.sleep(0.1)  # Brief delay to ensure different timestamp

    # Edit with backup
    success, msg = write(test_file, "Version 2", backup=True)
    print_result(success, f"Edit with backup: {msg}")

    # Check backup exists
    backups = araya_files.list_backups(test_file)
    print_result(len(backups) > 0, f"Backup created: {len(backups)} backups found")

    if backups:
        print(f"  Latest backup: {backups[0].name}")

    # Cleanup
    try:
        full_path.unlink()
        for backup in backups:
            backup.unlink()
        print("Cleanup: Removed test file and backups")
    except:
        pass

def test_rollback():
    """Test rollback functionality."""
    print_test("Rollback Functionality")

    test_file = "test_rollback.html"
    base_path = Path("C:/Users/dwrek/100X_DEPLOYMENT")
    full_path = base_path / test_file

    # Version 1
    write(test_file, "Version 1", backup=False)
    time.sleep(0.1)

    # Version 2 (creates backup of v1)
    write(test_file, "Version 2", backup=True)
    time.sleep(0.1)

    # Version 3 (creates backup of v2)
    write(test_file, "Version 3", backup=True)

    # Read current (should be v3)
    success, content, msg = read(test_file)
    print_result(content == "Version 3", f"Current version: {content}")

    # Rollback to v2
    success, msg = rollback(test_file, backup_index=0)
    print_result(success, f"Rollback to previous: {msg}")

    # Verify rollback
    success, content, msg = read(test_file)
    print_result(content == "Version 2", f"After rollback: {content}")

    # Cleanup
    try:
        full_path.unlink()
        backups = araya_files.list_backups(test_file)
        for backup in backups:
            backup.unlink()
        print("Cleanup: Removed test file and backups")
    except:
        pass

def test_audit_log():
    """Test audit logging."""
    print_test("Audit Logging")

    # Clear recent operations and do some actions
    test_file = "test_audit.html"

    write(test_file, "Test content")
    read(test_file)
    write(".env", "hack")  # Should be blocked

    # Get logs
    logs = get_logs(limit=10)
    print_result(len(logs) > 0, f"Logs captured: {len(logs)} entries")

    # Print recent logs
    print("\nRecent audit log entries:")
    for log in logs[-5:]:
        print(f"  [{log['timestamp']}] {log['type']}/{log['operation']} - {log['target']}")

    # Cleanup
    try:
        (Path("C:/Users/dwrek/100X_DEPLOYMENT") / test_file).unlink()
    except:
        pass

def test_list_files():
    """Test file listing."""
    print_test("List Allowed Files")

    # List HTML files
    html_files = list_files("*.html")
    print_result(len(html_files) > 0, f"Found {len(html_files)} HTML files")

    # Show first 5
    print("\nFirst 5 HTML files:")
    for file in html_files[:5]:
        print(f"  - {file}")

def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("ARAYA FILE ACCESS - TEST SUITE")
    print("="*60)

    test_whitelist_allowed()
    test_whitelist_blocked()
    test_path_traversal()
    test_backup_creation()
    test_rollback()
    test_audit_log()
    test_list_files()

    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)
    print("\nCheck audit log: 100X_DEPLOYMENT/.araya_edits.log")

if __name__ == "__main__":
    run_all_tests()
