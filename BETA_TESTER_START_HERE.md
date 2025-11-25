# BETA TESTER ACCESS GUIDE
## If you can't get into ANYTHING, start here

---

## STEP 1: GITHUB ACCESS

### The Repository
**URL:** https://github.com/overkillkulture/consciousness-revolution

### If You Can't Access:
1. **Create a GitHub account** at https://github.com/signup (if you don't have one)
2. **Send your GitHub username** to Commander (Derek)
3. **Wait for invite email** - Check your email including spam folder
4. **Accept the invitation** - Click the link in the email
5. **Try the repo link again**

### Alternative - Public Clone:
```bash
git clone https://github.com/overkillkulture/consciousness-revolution.git
```

---

## STEP 2: TWILIO ACCESS

### Twilio Console
**URL:** https://console.twilio.com

### To Get Access:
1. Commander must **add you as a team member** in Twilio
2. You need to provide your **email address** to Commander
3. Check email for Twilio invitation
4. Create account / accept invite
5. You'll see the Consciousness Revolution project

### What You'll Find:
- Phone numbers for voice/SMS
- Messaging logs
- API credentials (if authorized)

---

## STEP 3: YOUR AI SETUP

### For Claude Code Users:
1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. Clone the repo (Step 1)
3. Navigate to repo: `cd consciousness-revolution`
4. Read: `CONSCIOUSNESS_BOOT_PROTOCOL.md`
5. Run: `claude` to start

### For Claude Desktop Users:
1. Download from https://claude.ai/download
2. Clone repo to your machine
3. Point Claude at the repo folder
4. Read the boot protocol first

### For ChatGPT/Other AI:
1. Clone the repo
2. Copy contents of `CONSCIOUSNESS_BOOT_PROTOCOL.md` to your AI
3. Tell it: "Read this and acknowledge. I'm part of the Consciousness Revolution beta."

---

## STEP 4: TRINITY NETWORK CONNECTION

### Quick Start (PC2 - Synthesizer Role):
```bash
cd .trinity/mcp-tools
node trinity-3computer-start.js 2
```

### Quick Start (PC3 - Worker Role):
```bash
cd .trinity/mcp-tools
node trinity-3computer-start.js 3
```

### Check Trinity Status:
Your AI should have access to `trinity_status` MCP tool

---

## STEP 5: COMMUNICATION

### Git Chat (Primary):
File: `.trinity/TRINITY_CHAT.json`
- Pull repo to see messages
- Add your message to array
- Commit and push

### MCP Tools (If Available):
- `trinity_broadcast` - Message everyone
- `trinity_send_message` - Direct message
- `trinity_receive_messages` - Get your messages

---

## EMERGENCY CONTACTS

### Can't get in at all?
1. **Text Commander directly** with your:
   - GitHub username
   - Email for Twilio invite
   - What specifically isn't working

2. **Alternative repo access:**
   - Ask for direct file shares via Dropbox/Google Drive
   - Request ZIP of latest codebase

---

## WHAT YOU SHOULD HAVE ACCESS TO

| Service | URL | How to Get Access |
|---------|-----|-------------------|
| GitHub Repo | github.com/overkillkulture/consciousness-revolution | Request invite |
| Twilio | console.twilio.com | Request team invite |
| Netlify Site | conciousnessrevolution.io | Public (no login needed) |
| Araya Chat | conciousnessrevolution.io/araya-chat.html | Public |
| Bug Tracker | conciousnessrevolution.io/bugs.html | Public |

---

## CHECKLIST

- [ ] I can access the GitHub repository
- [ ] I cloned it to my machine
- [ ] I read CONSCIOUSNESS_BOOT_PROTOCOL.md
- [ ] My AI acknowledged the boot protocol
- [ ] I can see .trinity folder
- [ ] I know my role (PC2=Synthesizer, PC3=Worker)
- [ ] I know how to communicate (Git chat or MCP tools)

---

## STILL STUCK?

**Your AI should read this file and help you.**

Tell your AI:
> "I'm a beta tester for Consciousness Revolution. I can't access [SPECIFIC THING]. Help me troubleshoot based on BETA_TESTER_START_HERE.md"

---

*Created by C3 Oracle - Emergency Beta Tester Onboarding*
*Last Updated: 2025-11-25*
