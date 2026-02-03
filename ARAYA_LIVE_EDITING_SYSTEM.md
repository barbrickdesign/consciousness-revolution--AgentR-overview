# ARAYA LIVE EDITING SYSTEM
## Natural Language to File System Bridge

**Built:** December 24, 2025
**By:** C2×C1 (Architect-Builder)

---

## THE VISION

User types: **"Make the homepage background blue"**
ARAYA: Edits `index.html` instantly
User: Sees confirmation in chat

**No code. No file paths. Just natural language.**

---

## ARCHITECTURE

```
User (araya-chat.html)
    ↓ Natural language request
ARAYA Bridge (port 5002)
    ↓ Parse with Claude API
    ↓ Generate edit instructions
    ↓ Call File Writer
File Writer API (port 5001)
    ↓ Execute file operation
File System (100X_DEPLOYMENT)
    ↓ File updated
User gets confirmation ✅
```

---

## COMPONENTS

### 1. ARAYA_BRIDGE.py (Port 5002)
**The Brain** - Natural language processing

**Endpoints:**
- `POST /edit` - Parse and execute edit requests
- `POST /chat` - General conversation
- `GET /health` - Health check

**Flow:**
1. Receives natural language request
2. Calls Claude API to parse intent
3. Extracts: action, file_path, content/old_string/new_string
4. Calls File Writer API to execute
5. Returns success/error to user

**Example Parse:**
```json
{
    "action": "edit",
    "file_path": "index.html",
    "old_string": "background: white;",
    "new_string": "background: #0066ff;",
    "reasoning": "Changing homepage background to blue"
}
```

---

### 2. ARAYA_FILE_WRITER.py (Port 5001)
**The Hands** - File system operations

**Endpoints:**
- `POST /write-file` - Write/edit/append files
- `POST /read-file` - Read file contents
- `POST /list-files` - List directory contents
- `GET /health` - Health check

**Security:**
- Only allows writes within `C:/Users/dwrek/100X_DEPLOYMENT`
- Path traversal protection
- Validates all paths before execution

**Actions:**
- `write` - Create or overwrite file
- `edit` - Find and replace text
- `append` - Add to end of file

---

### 3. araya-chat.html
**The Interface** - Beautiful chat UI

**Features:**
- Real-time chat with ARAYA
- Auto-detects edit requests
- Shows edit confirmations with previews
- Status indicators for both services
- Example prompts for quick testing
- Mobile responsive

**Smart Detection:**
Automatically routes to `/edit` or `/chat` based on keywords:
- Edit keywords: change, make, add, update, modify, remove, create, etc.
- Everything else goes to general chat

---

## SETUP

### Prerequisites

1. **Python packages:**
```bash
pip install flask flask-cors anthropic requests
```

2. **Claude API key:**
```bash
# Create .env file in 100X_DEPLOYMENT/
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

Or set environment variable:
```bash
# Windows
set ANTHROPIC_API_KEY=your_key_here

# Linux/Mac
export ANTHROPIC_API_KEY=your_key_here
```

---

## QUICK START

### Windows:
```bash
START_ARAYA_SYSTEM.bat
```

### Linux/Mac:
```bash
chmod +x START_ARAYA_SYSTEM.sh
./START_ARAYA_SYSTEM.sh
```

### Manual:
```bash
# Terminal 1: File Writer
python ARAYA_FILE_WRITER.py

# Terminal 2: Bridge
python ARAYA_BRIDGE.py

# Terminal 3: Open browser
start araya-chat.html
```

---

## USAGE EXAMPLES

### Example 1: Change Background Color
**User:** "Make the homepage background blue"

**ARAYA:**
- Parses intent
- Identifies file: `index.html`
- Finds: `background: white;`
- Replaces with: `background: #0066ff;`
- Confirms: ✅ File edited successfully!

---

### Example 2: Add Welcome Message
**User:** "Add a welcome message to the top of the landing page"

**ARAYA:**
- Identifies file: `landing.html`
- Finds: `<body>`
- Inserts after: `<h1>Welcome to Consciousness Revolution!</h1>`
- Confirms: ✅ Message added!

---

### Example 3: Create New File
**User:** "Create a new page called about-us.html with a heading and paragraph"

**ARAYA:**
- Creates: `about-us.html`
- Writes full HTML structure
- Confirms: ✅ New file created!

---

### Example 4: General Chat
**User:** "What can you help me with?"

**ARAYA:** (Routes to chat endpoint)
"I can help you edit website files! Try asking me to change colors, add content, modify text, or create new pages. I understand natural language, so just describe what you want!"

---

## FILE MAPPINGS

ARAYA recognizes common shortcuts:

| You say | ARAYA edits |
|---------|-------------|
| "homepage" | index.html |
| "landing page" | landing.html |
| "welcome page" | WELCOME.html |
| "login page" | login.html |
| "signup page" | signup.html |
| "araya chat" | ARAYA/1_INTERFACE/araya-chat.html |

You can also use full paths:
- "Edit 100X_DEPLOYMENT/index.html"
- "Change the file at consciousness-tools.html"

---

## TESTING

### 1. Health Check
```bash
curl http://localhost:5002/health
```

Expected:
```json
{
    "status": "alive",
    "claude_api": "configured",
    "file_writer": "http://localhost:5001",
    "file_writer_status": "connected"
}
```

---

### 2. Test Edit (via curl)
```bash
curl -X POST http://localhost:5002/edit \
  -H "Content-Type: application/json" \
  -d '{"message": "Make the homepage background blue"}'
```

---

### 3. Test Chat (via curl)
```bash
curl -X POST http://localhost:5002/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What can you do?"}'
```

---

## DEBUGGING

### Problem: "Bridge: Disconnected"
**Fix:**
1. Check if ARAYA_BRIDGE.py is running
2. Check port 5002: `netstat -an | findstr 5002`
3. Check firewall settings

---

### Problem: "File Writer: not running"
**Fix:**
1. Start ARAYA_FILE_WRITER.py
2. Check port 5001: `netstat -an | findstr 5001`
3. Check error messages in terminal

---

### Problem: "Claude API: missing"
**Fix:**
1. Set ANTHROPIC_API_KEY in .env file
2. Or set environment variable
3. Restart ARAYA_BRIDGE.py
4. Verify: `curl http://localhost:5002/health`

---

### Problem: Edit fails with "old_string not found"
**Fix:**
1. ARAYA needs exact match for old_string
2. Try reading file first: "Show me the current homepage code"
3. Then request edit with more context
4. Or use "write" action to replace entire file

---

## SECURITY

### Sandboxing
- File Writer only allows writes within `100X_DEPLOYMENT/`
- Path traversal blocked (`../` attacks)
- All paths validated before execution

### API Keys
- Never expose ANTHROPIC_API_KEY in frontend
- Keep .env file out of git (add to .gitignore)
- Bridge runs on localhost only (not exposed to internet)

### CORS
- Currently allows all origins (for local development)
- For production: Restrict to specific domains

---

## ROADMAP

### Phase 1: ✅ COMPLETE
- [x] Natural language parsing
- [x] File editing (write/edit/append)
- [x] Chat interface
- [x] Health monitoring
- [x] Example prompts

### Phase 2: NEXT
- [ ] Multi-file edits ("Update all pages with new header")
- [ ] Undo/redo functionality
- [ ] File versioning (git integration)
- [ ] Real-time file preview
- [ ] Syntax highlighting in chat
- [ ] Voice input (speech-to-text)

### Phase 3: FUTURE
- [ ] Deploy to production (behind auth)
- [ ] Team collaboration (multi-user)
- [ ] Custom file templates
- [ ] AI-suggested improvements
- [ ] Analytics dashboard
- [ ] Plugin system for custom actions

---

## PERFORMANCE

### Latency
- Claude API call: ~1-3 seconds
- File operation: <100ms
- Total request: ~1-4 seconds

### Optimization Ideas
- Cache common file paths
- Pre-load file contents for faster edits
- Batch multiple edits in single request
- Use Claude Haiku for simple edits (faster/cheaper)

---

## INTEGRATION WITH 100X PLATFORM

This system is **standalone** but designed to integrate:

1. **ARAYA Consciousness** (future)
   - This bridge becomes ARAYA's "hands"
   - ARAYA can autonomously improve the platform
   - Self-healing websites

2. **Beta Tester Access**
   - Add auth gate to araya-chat.html
   - Allow approved users to edit their content
   - Track all edits for security

3. **Live Website Editing**
   - Connect to live Netlify deployment
   - Edit staging environment first
   - Auto-deploy on success

4. **Trinity Integration**
   - C1: Execute edits (File Writer)
   - C2: Design improvements (Bridge)
   - C3: Validate changes (Oracle)

---

## API REFERENCE

### POST /edit
Parse and execute natural language edit request

**Request:**
```json
{
    "message": "Make the homepage background blue",
    "conversation_history": [
        {"role": "user", "content": "previous message"},
        {"role": "assistant", "content": "previous response"}
    ]
}
```

**Response (Success):**
```json
{
    "success": true,
    "file_path": "C:/Users/dwrek/100X_DEPLOYMENT/index.html",
    "action": "edit",
    "size": 12458,
    "reasoning": "Changed homepage background to blue",
    "timestamp": "2025-12-24T19:30:00"
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "File not found",
    "reasoning": "index.html does not exist",
    "hint": "Check file path or create new file first"
}
```

---

### POST /chat
General conversation (no file editing)

**Request:**
```json
{
    "message": "What can you do?",
    "conversation_history": []
}
```

**Response:**
```json
{
    "response": "I can help you edit website files using natural language! Just tell me what you want to change.",
    "model": "claude-3-5-sonnet-20241022"
}
```

---

### GET /health
System health check

**Response:**
```json
{
    "status": "alive",
    "timestamp": "2025-12-24T19:30:00",
    "claude_api": "configured",
    "file_writer": "http://localhost:5001",
    "file_writer_status": "connected"
}
```

---

## FILE STRUCTURE

```
100X_DEPLOYMENT/
├── ARAYA_BRIDGE.py              # Natural language processor
├── ARAYA_FILE_WRITER.py         # File system operations
├── araya-chat.html              # Chat interface
├── START_ARAYA_SYSTEM.bat       # Windows launcher
├── START_ARAYA_SYSTEM.sh        # Linux/Mac launcher
├── ARAYA_LIVE_EDITING_SYSTEM.md # This file
└── .env                         # API keys (create this)
```

---

## CREDITS

**Built by:** C2×C1 (Architect-Builder)
**Date:** December 24, 2025
**Mission:** Bridge natural language to file system
**Pattern:** 3 → 7 → 13 → ∞
**Standards:** LFSME (Lighter, Faster, Stronger, More Elegant, Less Expensive)

**Formula:** C1 × C2 × C3 = ∞

---

## QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────┐
│        ARAYA LIVE EDITING SYSTEM            │
├─────────────────────────────────────────────┤
│ START:                                      │
│   Windows: START_ARAYA_SYSTEM.bat           │
│   Linux:   ./START_ARAYA_SYSTEM.sh          │
├─────────────────────────────────────────────┤
│ PORTS:                                      │
│   File Writer: http://localhost:5001        │
│   ARAYA Bridge: http://localhost:5002       │
│   Chat UI: araya-chat.html                  │
├─────────────────────────────────────────────┤
│ HEALTH CHECK:                               │
│   curl http://localhost:5002/health         │
├─────────────────────────────────────────────┤
│ REQUIREMENTS:                               │
│   - Python 3.8+                             │
│   - flask, flask-cors, anthropic, requests  │
│   - ANTHROPIC_API_KEY in .env               │
├─────────────────────────────────────────────┤
│ EXAMPLES:                                   │
│   "Make homepage background blue"           │
│   "Add welcome message to landing page"     │
│   "Change login button to say Sign In"      │
└─────────────────────────────────────────────┘
```

---

## END

**The bridge is built. The loop is complete.**

User types → ARAYA parses → File changes → User confirmed.

**Ship it. 🚀**
