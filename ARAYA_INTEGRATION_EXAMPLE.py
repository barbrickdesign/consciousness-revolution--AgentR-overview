"""
ARAYA INTEGRATION EXAMPLE
Shows how ARAYA_UPGRADED_V2.py will use the secure file access layer.

This is a proof-of-concept for the actual integration.
"""

from ARAYA_FILE_ACCESS import read, write, rollback, list_files, get_logs

class ArayaWithFileAccess:
    """ARAYA with secure file editing capabilities."""

    def __init__(self):
        self.conversation_history = []

    def detect_intent(self, user_message: str) -> dict:
        """
        Detect what the user wants to do.
        (In real ARAYA, this uses Claude API for NLP)
        """
        msg_lower = user_message.lower()

        # Edit intent
        if any(word in msg_lower for word in ["edit", "change", "update", "modify"]):
            if "index.html" in msg_lower:
                return {
                    "intent": "edit_file",
                    "file": "index.html",
                    "action": "modify content"
                }

        # List files intent
        if "list" in msg_lower and "file" in msg_lower:
            return {
                "intent": "list_files",
                "pattern": "*.html" if "html" in msg_lower else "*"
            }

        # Rollback intent
        if "undo" in msg_lower or "rollback" in msg_lower or "revert" in msg_lower:
            return {
                "intent": "rollback",
                "file": self._extract_filename(msg_lower)
            }

        # View audit log
        if "log" in msg_lower or "history" in msg_lower:
            return {
                "intent": "show_log",
                "limit": 20
            }

        return {"intent": "unknown"}

    def _extract_filename(self, message: str) -> str:
        """Extract filename from message (simple version)."""
        words = message.split()
        for word in words:
            if ".html" in word or ".md" in word:
                return word.strip(".,!?")
        return "index.html"  # Default

    def handle_edit_file(self, file_path: str, user_message: str) -> str:
        """Handle file editing request."""
        # Read current content
        success, current_content, msg = read(file_path)

        if not success:
            return f"❌ Cannot access {file_path}: {msg}"

        # In real ARAYA, this would:
        # 1. Send current_content + user_message to Claude API
        # 2. Get AI-generated new content back
        # For demo, just add a comment
        new_content = f"<!-- EDITED BY ARAYA -->\n{current_content}"

        # Write with automatic backup
        success, msg = write(file_path, new_content)

        if success:
            return f"✅ File edited: {file_path}\n💾 Backup created automatically\n📝 Audit log updated"
        else:
            return f"❌ Edit failed: {msg}"

    def handle_list_files(self, pattern: str = "*") -> str:
        """List editable files."""
        files = list_files(pattern)

        if not files:
            return f"No files found matching: {pattern}"

        response = f"📁 Found {len(files)} editable files:\n\n"
        for i, file in enumerate(files[:20], 1):  # Show first 20
            response += f"{i}. {file}\n"

        if len(files) > 20:
            response += f"\n...and {len(files) - 20} more"

        return response

    def handle_rollback(self, file_path: str) -> str:
        """Rollback file to previous version."""
        success, msg = rollback(file_path)

        if success:
            return f"⏪ Rollback successful: {file_path}\n{msg}\n💾 Current state backed up before rollback"
        else:
            return f"❌ Rollback failed: {msg}"

    def handle_show_log(self, limit: int = 20) -> str:
        """Show recent audit log."""
        logs = get_logs(limit)

        if not logs:
            return "No audit log entries found"

        response = f"📋 Last {len(logs)} operations:\n\n"

        for log in logs[-10:]:  # Show last 10
            timestamp = log['timestamp'].split('T')[1][:8]  # Just time
            status = "✅" if log['metadata'].get('success') else "❌"
            response += f"{status} {timestamp} - {log['operation']}: {log['target']}\n"

        return response

    def process_message(self, user_message: str) -> str:
        """Main message processing - this is what ARAYA calls."""
        intent = self.detect_intent(user_message)

        if intent["intent"] == "edit_file":
            return self.handle_edit_file(intent["file"], user_message)

        elif intent["intent"] == "list_files":
            return self.handle_list_files(intent["pattern"])

        elif intent["intent"] == "rollback":
            return self.handle_rollback(intent["file"])

        elif intent["intent"] == "show_log":
            return self.handle_show_log(intent.get("limit", 20))

        else:
            return "I can help you:\n- Edit files: 'Edit index.html'\n- List files: 'List HTML files'\n- Rollback: 'Undo changes to index.html'\n- View log: 'Show edit history'"

# Demo usage
if __name__ == "__main__":
    print("="*60)
    print("ARAYA FILE ACCESS - INTEGRATION DEMO")
    print("="*60)

    araya = ArayaWithFileAccess()

    # Test 1: List files
    print("\n📝 User: List all HTML files")
    print(araya.process_message("List all HTML files"))

    # Test 2: Edit file (BLOCKED - for safety in demo)
    print("\n" + "="*60)
    print("\n📝 User: Edit index.html")
    response = araya.process_message("Edit index.html")
    print(response)

    # Test 3: Show log
    print("\n" + "="*60)
    print("\n📝 User: Show edit history")
    print(araya.process_message("Show edit history"))

    # Test 4: Rollback
    print("\n" + "="*60)
    print("\n📝 User: Undo changes to index.html")
    print(araya.process_message("Undo changes to index.html"))

    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nNext step: Integrate this into ARAYA_UPGRADED_V2.py")
