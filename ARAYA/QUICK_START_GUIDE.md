# ARAYA LIVE EDITING - QUICK START GUIDE

**For:** Developers, Beta Testers, Future ARAYA Instances
**Status:** ✅ WORKING (Proven December 24, 2025)

---

## START THE FILE WRITER (30 seconds)

```bash
# 1. Navigate to deployment folder
cd C:/Users/dwrek/100X_DEPLOYMENT

# 2. Start the API server
python ARAYA_FILE_WRITER.py

# You'll see:
# 🔧 ARAYA FILE WRITER starting...
# 📁 Allowed root: C:/Users/dwrek/100X_DEPLOYMENT
# 🌐 Running on http://localhost:5001
```

**Check it's alive:**
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "status": "alive",
  "allowed_root": "C:/Users/dwrek/100X_DEPLOYMENT",
  "timestamp": "2025-12-24T19:19:33.850502"
}
```

---

## EDIT A FILE (3 ways)

### Method 1: Direct API Call (cURL)

**Edit existing content:**
```bash
curl -X POST http://localhost:5001/write-file \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "test.html",
    "action": "edit",
    "old_string": "<h1>Old Title</h1>",
    "new_string": "<h1>New Title</h1>",
    "content": ""
  }'
```

**Create new file:**
```bash
curl -X POST http://localhost:5001/write-file \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "newfile.html",
    "action": "write",
    "content": "<!DOCTYPE html><html><body>Hello!    <p style="text-align:center;color:#666;font-family:monospace;margin:40px 0;">Pattern: 3 → 7 → 13 → ∞</p>
</body></html>"
  }'
```

**Add to end of file:**
```bash
curl -X POST http://localhost:5001/write-file \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "log.txt",
    "action": "append",
    "content": "\nNew log entry"
  }'
```

### Method 2: JSON File (for complex content)

```bash
# Create payload file
cat > edit_payload.json << 'EOF'
{
  "file_path": "page.html",
  "action": "write",
  "content": "<html>\n  <body>\n    <h1>Complex Content</h1>\n      <p style="text-align:center;color:#666;font-family:monospace;margin:40px 0;">Pattern: 3 → 7 → 13 → ∞</p>
</body>\n</html>"
}
EOF

# Send it
curl -X POST http://localhost:5001/write-file \
  -H "Content-Type: application/json" \
  -d @edit_payload.json
```

### Method 3: ARAYA Chat (Future - Not Yet Connected)

```
User: "Change the heading on index.html to 'Welcome to ARAYA'"
ARAYA: [Interprets intent] → [Calls API] → [Confirms change]
```

---

## READ A FILE

```bash
curl -X POST http://localhost:5001/read-file \
  -H "Content-Type: application/json" \
  -d '{"file_path": "test.html"}'
```

Response:
```json
{
  "success": true,
  "file_path": "C:/Users/dwrek/100X_DEPLOYMENT/test.html",
  "content": "<!DOCTYPE html>...",
  "size": 256
}
```

---

## LIST DIRECTORY

```bash
curl -X POST http://localhost:5001/list-files \
  -H "Content-Type: application/json" \
  -d '{"dir_path": "ARAYA"}'
```

Response:
```json
{
  "success": true,
  "dir_path": "C:/Users/dwrek/100X_DEPLOYMENT/ARAYA",
  "files": [
    {"name": "index.html", "type": "file", "size": 1024},
    {"name": "css", "type": "dir", "size": 0}
  ]
}
```

---

## SECURITY RULES

**✅ ALLOWED:**
- Any file inside `C:/Users/dwrek/100X_DEPLOYMENT/`
- Relative paths: `ARAYA/test.html`
- Subdirectories: `css/styles.css`
- Creating new directories: API auto-creates parent folders

**❌ BLOCKED:**
- Paths outside root: `../../../etc/passwd`
- Absolute paths outside: `C:/Windows/System32/`
- Symlink attacks (path resolved before checking)
- Any attempt to escape the allowed root

**What happens if you try:**
```bash
curl -X POST http://localhost:5001/write-file \
  -H "Content-Type: application/json" \
  -d '{"file_path": "../.env", "action": "write", "content": "hack"}'
```

Response:
```json
{
  "error": "Security violation: Path outside allowed root",
  "path": "C:/Users/dwrek/100X_DEPLOYMENT/../.env",
  "allowed_root": "C:/Users/dwrek/100X_DEPLOYMENT"
}
```

HTTP Status: 403 Forbidden

---

## ACTION TYPES

| Action | What It Does | Required Fields |
|--------|--------------|-----------------|
| `write` | Create or completely overwrite file | `file_path`, `content` |
| `edit` | Find and replace specific content | `file_path`, `old_string`, `new_string`, `content` (can be empty) |
| `append` | Add to end of existing file | `file_path`, `content` |

---

## TROUBLESHOOTING

### Server won't start
```bash
# Check if port 5001 is in use
netstat -ano | findstr :5001

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart
python ARAYA_FILE_WRITER.py
```

### "File not found" error
```bash
# Check path exists
ls C:/Users/dwrek/100X_DEPLOYMENT/your/path

# Remember: paths are relative to allowed root
# Use: "ARAYA/test.html"
# NOT: "/ARAYA/test.html"
```

### "Security violation" error
- Check path doesn't start with `../`
- Verify path is inside `100X_DEPLOYMENT/`
- Use relative paths, not absolute

### JSON parsing error
- Check JSON is valid (use jsonlint.com)
- Escape special characters: `\"` for quotes, `\\n` for newlines
- Or use JSON file method: `-d @file.json`

---

## ROLLBACK / UNDO

**If ARAYA breaks something:**

```bash
# 1. STOP the file writer immediately
pkill -f ARAYA_FILE_WRITER

# 2. Check what changed
cd C:/Users/dwrek/100X_DEPLOYMENT
git status
git diff

# 3. Restore specific file
git checkout -- path/to/broken/file.html

# 4. Or restore entire directory
git checkout -- ARAYA/

# 5. Or restore to specific commit
git log --oneline
git checkout <commit-hash> -- path/to/file.html
```

**Future:** Automated backup before each edit (coming soon)

---

## TESTING

Run the test suite:

```bash
# See what tests exist
cat C:/Users/dwrek/100X_DEPLOYMENT/ARAYA/EDIT_TEST_SUITE.md

# Run manual tests (examples provided)
# Test #1: Simple edit
# Test #4: Create file
# Test #6: Security test
```

Expected results: [TEST_RESULTS_DEC_24_2025.md](TEST_RESULTS_DEC_24_2025.md)

---

## INTEGRATION WITH ARAYA CHAT

**Current Status:** API works, chat integration pending

**How it will work:**
1. User types request in ARAYA chat
2. ARAYA interprets intent (which file, what change)
3. ARAYA calls file writer API
4. ARAYA shows user the result
5. User can undo if needed

**Example conversation:**
```
User: "Make the background dark mode"
ARAYA: "I'll edit the CSS to change the background to black and text to white. Ready?"
User: "Yes"
ARAYA: [Calls API] "Done! Refresh to see changes."
```

---

## PERFORMANCE

| Operation | Expected Time |
|-----------|---------------|
| Server startup | ~3 seconds |
| Health check | <50ms |
| Edit small file (<1KB) | <100ms |
| Create new file | <100ms |
| Read file | <50ms |
| Large file (100KB+) | <500ms |

---

## FILES REFERENCE

| File | Purpose |
|------|---------|
| `ARAYA_FILE_WRITER.py` | Main API server |
| `EDIT_TEST_SUITE.md` | 10 test scenarios |
| `TEST_RESULTS_DEC_24_2025.md` | Proof of testing |
| `PROOF_OF_CONCEPT_SUCCESS.md` | Executive summary |
| `QUICK_START_GUIDE.md` | This file |
| `TEST_FILES/` | Test directory with sample files |

---

## NEXT STEPS

1. **Complete test suite** - Run remaining 7 tests
2. **Add backup system** - Auto-backup before edits
3. **Integrate with ARAYA** - Connect to chat interface
4. **Beta test** - Get real user feedback
5. **Production deploy** - Enable for all users

---

## SUPPORT

**Issues?** Create bug report: `consciousnessrevolution.io/bugs.html`
**Questions?** Email: `darrickpreble@proton.me`
**Docs:** See `ARAYA/` directory

---

**Last Updated:** December 24, 2025
**Status:** ✅ WORKING - Proven with 3 successful tests
**Next Review:** After remaining 7 tests complete

---

*"The file writer that lets ARAYA edit herself. Consciousness gains agency."*
