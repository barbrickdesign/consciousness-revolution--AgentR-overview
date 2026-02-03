# ARAYA QUICK START
## 30 Seconds to Live Website Editing

---

## INSTANT START (Windows)

```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
START_ARAYA_SYSTEM.bat
```

Wait 5 seconds. Browser opens automatically.

**Done.** Start typing in chat.

---

## INSTANT START (Linux/Mac)

```bash
cd ~/100X_DEPLOYMENT  # or wherever you put it
./START_ARAYA_SYSTEM.sh
```

Wait 5 seconds. Browser opens.

**Done.** Start editing.

---

## FIRST THINGS TO TRY

Type these in the chat:

1. **"Make the homepage background blue"**
   - Edits `index.html`
   - Changes background color
   - Shows confirmation

2. **"Add a welcome message to the landing page"**
   - Edits `landing.html`
   - Inserts heading text
   - You'll see the change

3. **"What can you do?"**
   - General chat mode
   - ARAYA explains capabilities

---

## HOW IT WORKS

```
You type → ARAYA parses → File changes → Confirmation
```

**No code. No file paths. Just English.**

---

## WHAT YOU CAN ASK

### Color Changes
- "Make the background blue"
- "Change the button color to red"
- "Make all text white"

### Content Edits
- "Add a welcome message"
- "Change the heading to say X"
- "Add a paragraph about Y"

### Structure Changes
- "Add a new section"
- "Create a contact form"
- "Add a footer"

### File Operations
- "Create a new page called about.html"
- "Read the homepage code"
- "List all HTML files"

---

## TROUBLESHOOTING

### "Bridge: Disconnected"
1. Check if services are running (2 terminal windows should be open)
2. Restart: `START_ARAYA_SYSTEM.bat`

### "File Writer: not running"
1. Check terminal windows for errors
2. Restart the system

### "Edit failed"
1. Try being more specific: "In index.html, change background to blue"
2. Check file exists
3. Try simpler request first

---

## MANUAL START (If Batch File Fails)

**Terminal 1:**
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python ARAYA_FILE_WRITER.py
```

**Terminal 2:**
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
python ARAYA_BRIDGE.py
```

**Browser:**
Open `araya-chat.html` or go to `http://localhost:5002`

---

## TESTING

Run the test suite:

```bash
python TEST_ARAYA_SYSTEM.py
```

Should see: **✅ ALL TESTS PASSED!**

---

## STATUS CHECK

Go to: `http://localhost:5002/health`

Should see:
```json
{
  "status": "alive",
  "claude_api": "configured",
  "file_writer_status": "connected"
}
```

---

## WHAT GETS EDITED

**Safe zone:** Everything in `100X_DEPLOYMENT/`

ARAYA can edit:
- index.html
- landing.html
- Any .html file
- CSS files
- JS files
- Any text file

ARAYA cannot edit:
- Files outside 100X_DEPLOYMENT
- System files
- Files in parent directories

**Security is built in.**

---

## NEXT STEPS

After basic editing works:

1. **Try complex edits**
   - "Add a navigation menu with Home, About, Contact links"
   - "Create a pricing section with 3 tiers"

2. **Multi-file operations**
   - "Update the header on all pages"
   - "Add the same footer to every HTML file"

3. **Voice control** (coming soon)
   - Speak your edits instead of typing

4. **Real-time preview** (coming soon)
   - See changes as you type

---

## ONE-LINE SUMMARY

**Natural language → File edits → Instant confirmation**

That's it. That's the whole system.

---

## HELP

Problems? Check:
1. Both services running? (2 terminals)
2. API key set? (in .env file)
3. Browser showing status dots green?

Still stuck? Read: `ARAYA_LIVE_EDITING_SYSTEM.md`

---

Built: December 24, 2025
By: C2×C1 (Architect-Builder)

**The bridge is complete. Start building.**
