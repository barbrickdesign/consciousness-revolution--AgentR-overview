# ARAYA FILE ACCESS LAYER
## Secure file operations with whitelisting, backups, and audit logging

**Built by:** C1×C2 (Structure + Security + Speed)
**Created:** December 24, 2025

---

## QUICK START

```python
from ARAYA_FILE_ACCESS import read, write, rollback, list_files, get_logs

# Read file
success, content, msg = read("index.html")

# Write file (auto-backup)
success, msg = write("index.html", "<html>New content</html>")

# Rollback to previous version
success, msg = rollback("index.html")

# List all editable HTML files
files = list_files("*.html")

# Get recent audit log
logs = get_logs(limit=50)
```

---

## SECURITY FEATURES

### 1. WHITELIST (Allowed)
Only these file types can be edited:
- `*.html` - Web pages
- `*.md` - Documentation
- `*.css` - Stylesheets
- `*.js` - JavaScript
- `*.json` - Data files

### 2. BLACKLIST (Forbidden)
These paths are NEVER editable:
- `.env*` - Environment secrets
- `netlify/functions/*` - Serverless functions
- `.git/*` - Git repository
- `*.py` - Python code (security)
- `.secrets/*` - Credentials
- `.araya_edits.log` - Audit log itself

### 3. PATH PROTECTION
- All paths must be within `C:/Users/dwrek/100X_DEPLOYMENT/`
- Path traversal attacks blocked (`../../../etc/passwd`)
- Absolute path validation

---

## BACKUP SYSTEM

### Automatic Backups
Every file edit creates a timestamped backup:
```
index.html.backup.20251224_191827
```

### Backup Naming
```
{filename}.{ext}.backup.{YYYYMMDD_HHMMSS}
```

### List Backups
```python
from ARAYA_FILE_ACCESS import araya_files

backups = araya_files.list_backups("index.html")
# Returns list sorted by newest first
```

### Rollback
```python
# Rollback to most recent backup
success, msg = rollback("index.html", backup_index=0)

# Rollback to second most recent
success, msg = rollback("index.html", backup_index=1)
```

---

## AUDIT LOG

### Location
```
100X_DEPLOYMENT/.araya_edits.log
```

### Format
JSON lines - one entry per operation:
```json
{
  "timestamp": "2025-12-24T19:18:27.891466",
  "type": "READ",
  "operation": "SUCCESS",
  "target": "index.html",
  "metadata": {
    "size": 5432,
    "success": true
  }
}
```

### Operation Types
- `SYSTEM` - System events (init)
- `READ` - File reads
- `WRITE` - File writes
- `ROLLBACK` - Restore operations
- `BACKUP` - Backup creation

### View Log
```python
# Get last 100 entries
logs = get_logs(limit=100)

for log in logs:
    print(f"{log['timestamp']} - {log['operation']}: {log['target']}")
```

Or via command line:
```bash
tail -50 100X_DEPLOYMENT/.araya_edits.log
```

---

## API REFERENCE

### read_file(file_path)
Read file contents.

**Args:**
- `file_path` (str): Relative path from 100X_DEPLOYMENT/

**Returns:**
- `(success: bool, content: Optional[str], message: str)`

**Example:**
```python
success, content, msg = read("index.html")
if success:
    print(content)
else:
    print(f"Error: {msg}")
```

---

### write_file(file_path, content, backup=True)
Write content to file.

**Args:**
- `file_path` (str): Relative path from 100X_DEPLOYMENT/
- `content` (str): File content
- `backup` (bool): Create backup before write (default: True)

**Returns:**
- `(success: bool, message: str)`

**Example:**
```python
success, msg = write("index.html", "<html>New</html>")
if not success:
    print(f"Write failed: {msg}")
```

---

### rollback(file_path, backup_index=0)
Restore file from backup.

**Args:**
- `file_path` (str): File to restore
- `backup_index` (int): Which backup (0=newest, 1=second, etc.)

**Returns:**
- `(success: bool, message: str)`

**Example:**
```python
# Undo last edit
success, msg = rollback("index.html")

# Restore from 3 edits ago
success, msg = rollback("index.html", backup_index=2)
```

---

### list_files(pattern="*")
List all files ARAYA can edit.

**Args:**
- `pattern` (str): Glob pattern (default: "*" = all allowed)

**Returns:**
- `List[str]`: Relative file paths

**Example:**
```python
# All HTML files
html_files = list_files("*.html")

# All MD files
docs = list_files("*.md")

# All allowed files
all_files = list_files()
```

---

### get_logs(limit=100)
Get recent audit log entries.

**Args:**
- `limit` (int): Max entries to return

**Returns:**
- `List[Dict]`: Log entries (newest last)

**Example:**
```python
logs = get_logs(limit=20)
for log in logs:
    print(f"{log['type']}/{log['operation']}: {log['target']}")
```

---

## INTEGRATION WITH ARAYA

### In ARAYA_UPGRADED_V2.py

```python
from ARAYA_FILE_ACCESS import read, write, list_files

# When ARAYA detects edit intent
if intent == "edit_file":
    file_path = extract_file_path(user_message)

    # Read current content
    success, current_content, msg = read(file_path)

    if success:
        # Generate new content with AI
        new_content = generate_edit(current_content, user_intent)

        # Write with automatic backup
        success, msg = write(file_path, new_content)

        if success:
            return f"File edited: {file_path}"
        else:
            return f"Edit failed: {msg}"
    else:
        return f"Cannot read file: {msg}"
```

### File Discovery

```python
# Show user what files they can edit
editable_files = list_files("*.html")
return f"You can edit these {len(editable_files)} HTML files: {editable_files[:10]}"
```

### Safety Checks

```python
# The module automatically:
# 1. Validates file path (whitelist/blacklist)
# 2. Creates backup before edit
# 3. Logs operation to audit log
# 4. Returns clear success/failure status
```

---

## TESTING

### Run Test Suite
```bash
cd 100X_DEPLOYMENT
python TEST_ARAYA_FILE_ACCESS.py
```

### Tests Included
1. Whitelist enforcement (HTML allowed)
2. Blacklist enforcement (.py, .env blocked)
3. Path traversal protection
4. Backup creation
5. Rollback functionality
6. Audit logging
7. File listing

### Expected Output
```
✓ PASS: Write HTML file
✓ PASS: Block .py file
✓ PASS: Block path traversal
✓ PASS: Backup created
✓ PASS: Rollback to previous
✓ PASS: Logs captured
```

---

## SECURITY GUARANTEES

1. **NO ARBITRARY CODE EXECUTION**
   - Cannot edit .py files
   - Cannot edit netlify functions

2. **NO CREDENTIAL EXPOSURE**
   - Cannot read/write .env files
   - Cannot access .secrets/ folder

3. **NO REPOSITORY DAMAGE**
   - Cannot modify .git/ folder

4. **FULL AUDIT TRAIL**
   - Every operation logged
   - Timestamps + metadata

5. **REVERSIBLE EDITS**
   - All changes create backups
   - Multiple rollback points

6. **SANDBOXED ACCESS**
   - Limited to 100X_DEPLOYMENT/
   - Path traversal blocked

---

## ARCHITECTURE

```
User Intent
    ↓
ARAYA_UPGRADED_V2.py
    ↓
ARAYA_FILE_ACCESS.py ──→ Whitelist Check ──→ BLOCKED
    ↓                          ↓
   OK                     Blacklist Check ──→ BLOCKED
    ↓                          ↓
Create Backup              Path Validation ──→ BLOCKED
    ↓                          ↓
Write File                    OK
    ↓                          ↓
Audit Log              Execute Operation
    ↓                          ↓
Success              Log to .araya_edits.log
```

---

## TROUBLESHOOTING

### "Access denied: Path matches forbidden pattern"
- You're trying to edit a blacklisted file type
- Check `FORBIDDEN_PATHS` in `ARAYA_FILE_ACCESS.py`

### "Access denied: File type not in whitelist"
- File extension not in allowed patterns
- Currently allowed: .html, .md, .css, .js, .json

### "Backup creation failed - write aborted"
- Cannot create backup of existing file
- Check disk space and permissions

### "No backups found"
- File has never been edited (no backup history)
- Or backups were manually deleted

### "Path outside allowed directory"
- Path traversal attack detected
- All paths must be within 100X_DEPLOYMENT/

---

## MAINTENANCE

### Clean Old Backups
```python
from pathlib import Path
from datetime import datetime, timedelta

base = Path("C:/Users/dwrek/100X_DEPLOYMENT")

# Delete backups older than 30 days
cutoff = datetime.now() - timedelta(days=30)

for backup in base.glob("*.backup.*"):
    if backup.stat().st_mtime < cutoff.timestamp():
        backup.unlink()
        print(f"Deleted old backup: {backup.name}")
```

### Compress Audit Log
```bash
# Rotate log when it gets large
cd 100X_DEPLOYMENT
mv .araya_edits.log .araya_edits.log.old
gzip .araya_edits.log.old
```

---

## NEXT STEPS

1. **Integrate with ARAYA_UPGRADED_V2.py**
   - Replace direct file operations with this module
   - Add file edit intent detection

2. **Add to Live Editor UI**
   - `ARAYA_LIVE_EDITOR.html` calls new API
   - Show backup/rollback buttons

3. **Test with Real Files**
   - Edit actual website pages
   - Verify backups work
   - Test rollback in production

---

## FILES

| File | Purpose |
|------|---------|
| `ARAYA_FILE_ACCESS.py` | Main security module |
| `TEST_ARAYA_FILE_ACCESS.py` | Test suite |
| `ARAYA_FILE_ACCESS_README.md` | This file |
| `.araya_edits.log` | Audit trail (auto-created) |

---

**MISSION COMPLETE: Secure file access layer deployed.**

Structure + Security + Speed = ARAYA can now safely edit website.
