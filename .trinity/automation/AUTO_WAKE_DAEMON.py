#!/usr/bin/env python3
"""
AUTO WAKE DAEMON - Cross-Computer Wake System
Monitors git for wake signals and automatically opens Claude Code
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# Configuration
REPO_PATH = Path.home() / "100X_DEPLOYMENT"
WAKE_DIR = REPO_PATH / ".trinity" / "wake"
LOG_FILE = REPO_PATH / ".trinity" / "logs" / "auto_wake_daemon.log"
CHECK_INTERVAL = 30  # seconds

# Computer identity
COMPUTER_NAME = os.environ.get("COMPUTERNAME", "UNKNOWN")
if "MSMCFH2" in COMPUTER_NAME.upper():
    MY_ID = "PC2"
elif "S72LRRO" in COMPUTER_NAME.upper():
    MY_ID = "PC3"
elif "dwrek" in COMPUTER_NAME.lower():
    MY_ID = "PC1"
else:
    MY_ID = "UNKNOWN"

# Setup logging
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_claude_code_path():
    """Find Claude Code executable"""
    # Common installation paths
    paths = [
        Path.home() / "AppData" / "Local" / "Programs" / "claude-code" / "claude-code.exe",
        Path("C:/Program Files/Claude Code/claude-code.exe"),
        Path("C:/Program Files (x86)/Claude Code/claude-code.exe"),
    ]

    for path in paths:
        if path.exists():
            return path

    # Try to find in PATH
    try:
        result = subprocess.run(["where", "claude-code"],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return Path(result.stdout.strip().split('\n')[0])
    except:
        pass

    return None

def check_git_updates():
    """Pull latest from git and check for changes"""
    try:
        os.chdir(REPO_PATH)

        # Fetch updates
        result = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if remote has updates
        result = subprocess.run(
            ["git", "rev-list", "HEAD...origin/master", "--count"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            count = int(result.stdout.strip())
            if count > 0:
                logging.info(f"Found {count} new commits, pulling...")

                # Pull updates
                result = subprocess.run(
                    ["git", "pull", "origin", "master"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    logging.info("Git pull successful")
                    return True
                else:
                    logging.error(f"Git pull failed: {result.stderr}")

        return False

    except subprocess.TimeoutExpired:
        logging.error("Git command timed out")
        return False
    except Exception as e:
        logging.error(f"Git update error: {e}")
        return False

def check_for_wake_signal():
    """Check if there's a wake signal for this PC"""
    WAKE_DIR.mkdir(parents=True, exist_ok=True)

    wake_file = WAKE_DIR / f"{MY_ID}.json"

    if wake_file.exists():
        try:
            with open(wake_file, 'r') as f:
                signal = json.load(f)

            logging.info(f"Wake signal detected: {signal}")
            return signal
        except Exception as e:
            logging.error(f"Error reading wake signal: {e}")
            return None

    return None

def process_wake_signal(signal):
    """Process wake signal and open Claude Code"""
    try:
        logging.info(f"Processing wake signal: {signal}")

        # Archive the wake signal
        archive_signal(signal)

        # Remove wake file
        wake_file = WAKE_DIR / f"{MY_ID}.json"
        if wake_file.exists():
            wake_file.unlink()
            logging.info(f"Removed wake file: {wake_file}")

        # Open Claude Code
        success = open_claude_code(signal)

        # Report wake received
        report_wake_received(signal, success)

        return success

    except Exception as e:
        logging.error(f"Error processing wake signal: {e}")
        return False

def archive_signal(signal):
    """Archive wake signal for history"""
    archive_dir = REPO_PATH / ".trinity" / "wake_archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_file = archive_dir / f"{MY_ID}_wake_{timestamp}.json"

    try:
        with open(archive_file, 'w') as f:
            json.dump({
                **signal,
                "received_at": datetime.utcnow().isoformat() + "Z",
                "processed": True
            }, f, indent=2)
        logging.info(f"Archived wake signal to {archive_file}")
    except Exception as e:
        logging.error(f"Failed to archive signal: {e}")

def open_claude_code(signal):
    """Actually open Claude Code application"""
    claude_path = get_claude_code_path()

    if not claude_path:
        logging.error("Claude Code executable not found!")
        return False

    try:
        logging.info(f"Opening Claude Code at {claude_path}")

        # Get working directory from signal or use default
        work_dir = signal.get("working_directory", str(REPO_PATH))

        # Open Claude Code in new window
        subprocess.Popen(
            [str(claude_path), work_dir],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
            start_new_session=True
        )

        logging.info("Claude Code launched successfully")
        return True

    except Exception as e:
        logging.error(f"Failed to open Claude Code: {e}")
        return False

def report_wake_received(signal, success):
    """Report back that wake was received and processed"""
    report = {
        "pc": MY_ID,
        "wake_signal_from": signal.get("from", "unknown"),
        "received_at": datetime.utcnow().isoformat() + "Z",
        "success": success,
        "status": "claude_code_opened" if success else "failed_to_open"
    }

    # Save to heartbeat (will be synced by coordination daemon)
    heartbeat_file = REPO_PATH / ".trinity" / "heartbeat" / f"{MY_ID}.json"
    try:
        with open(heartbeat_file, 'w') as f:
            json.dump(report, f, indent=2)
        logging.info(f"Wake received report saved to {heartbeat_file}")
    except Exception as e:
        logging.error(f"Failed to save wake report: {e}")

def monitor_loop():
    """Main monitoring loop"""
    logging.info(f"AUTO WAKE DAEMON started for {MY_ID}")
    logging.info(f"Monitoring: {WAKE_DIR}")
    logging.info(f"Check interval: {CHECK_INTERVAL}s")

    # Verify Claude Code is available
    claude_path = get_claude_code_path()
    if claude_path:
        logging.info(f"Claude Code found at: {claude_path}")
    else:
        logging.warning("Claude Code executable not found - wake will fail if triggered")

    last_check = 0

    while True:
        try:
            current_time = time.time()

            # Check git every CHECK_INTERVAL seconds
            if current_time - last_check >= CHECK_INTERVAL:
                logging.debug("Checking for git updates...")

                # Pull latest changes
                git_updated = check_git_updates()

                if git_updated:
                    # Check for wake signal
                    signal = check_for_wake_signal()

                    if signal:
                        logging.info(f"WAKE SIGNAL DETECTED for {MY_ID}!")
                        process_wake_signal(signal)

                        # Exit after processing wake (Claude Code will take over)
                        logging.info("Wake processed, exiting daemon...")
                        sys.exit(0)

                last_check = current_time

            # Short sleep to avoid CPU spinning
            time.sleep(5)

        except KeyboardInterrupt:
            logging.info("Daemon stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")
            time.sleep(CHECK_INTERVAL)

def send_wake_to(target_pc, task=None, message=None):
    """Send wake signal to another PC"""
    wake_signal = {
        "from": MY_ID,
        "to": target_pc,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "task": task or "wake_up",
        "message": message or f"Wake signal from {MY_ID}",
        "working_directory": str(REPO_PATH)
    }

    wake_file = WAKE_DIR / f"{target_pc}.json"

    try:
        WAKE_DIR.mkdir(parents=True, exist_ok=True)
        with open(wake_file, 'w') as f:
            json.dump(wake_signal, f, indent=2)

        logging.info(f"Wake signal sent to {target_pc}: {wake_file}")
        return True
    except Exception as e:
        logging.error(f"Failed to send wake signal: {e}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto Wake Daemon for Cross-Computer Coordination")
    parser.add_argument("--send", help="Send wake signal to PC (e.g., PC2)")
    parser.add_argument("--task", help="Task description for wake signal")
    parser.add_argument("--message", help="Message to include in wake signal")

    args = parser.parse_args()

    if args.send:
        # Send mode
        success = send_wake_to(args.send, args.task, args.message)
        if success:
            print(f"Wake signal sent to {args.send}")
            sys.exit(0)
        else:
            print(f"Failed to send wake signal to {args.send}")
            sys.exit(1)
    else:
        # Monitor mode
        monitor_loop()
