# STANDARDIZED COMPUTER BLUEPRINT

## WHAT EVERY COMPUTER NEEDS TO OPERATE

---

## REQUIRED SOFTWARE

### Must Install
- [ ] Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- [ ] Git
- [ ] Node.js (v18+)
- [ ] Python (3.10+)
- [ ] Tailscale
- [ ] Syncthing
- [ ] AnyDesk

### Optional But Recommended
- [ ] VS Code
- [ ] Netlify CLI (`npm install -g netlify-cli`)
- [ ] GitHub CLI (`gh`)

---

## REQUIRED ACCOUNTS & LOGINS

### Must Be Logged In
- [ ] GitHub (via `gh auth login` or token)
- [ ] Anthropic (Claude Code authenticated)
- [ ] Tailscale (connected to mesh)
- [ ] Google Account (for Drive sync)

### API Keys Needed
- [ ] ANTHROPIC_API_KEY
- [ ] GITHUB_TOKEN
- [ ] STRIPE_API_KEY (if doing payments)

### Save Keys To
```bash
# Windows
setx ANTHROPIC_API_KEY "sk-ant-..."
setx GITHUB_TOKEN "ghp_..."
```

---

## REQUIRED FOLDERS

Every computer must have:

```
C:\Users\[user]\
├── PC[X]_LOCAL_HUB/           ← Local consolidation hub
│   ├── terminal_reports/
│   ├── cloud_reports/
│   ├── consolidated/
│   └── outbound/
├── 100X_DEPLOYMENT/           ← Git repo (clone if missing)
├── Sync/                      ← Syncthing folder
└── READ_THIS_FIRST.txt        ← Points to local hub
```

---

## REQUIRED FILES IN LOCAL HUB

```
PC[X]_LOCAL_HUB/
├── BOOT_FIRST.md              ← Boot protocol
├── HUB_PROTOCOL.md            ← How to report
├── consolidate.py             ← Consolidation script
└── C1_IS_GITHUB_GATEKEEPER.md ← Only C1 pushes
```

---

## STANDARDIZED COMMANDS

### Every Instance Must Know

```bash
# Report to local hub
echo '{...}' > ~/PC[X]_LOCAL_HUB/terminal_reports/C[Y]_REPORT.json

# Check for messages (Syncthing)
ls ~/Sync/

# Check Tailscale
tailscale status

# Consolidate (C1 only)
python ~/PC[X]_LOCAL_HUB/consolidate.py

# Push to GitHub (C1 only)
cd ~/100X_DEPLOYMENT && git add . && git commit -m "msg" && git push
```

---

## ABILITIES BY ROLE

### C1 (Mechanic/Coordinator)
- ✅ Git push/pull
- ✅ Consolidate reports
- ✅ Push to GitHub
- ✅ Coordinate C2/C3
- ✅ All terminal abilities

### C2 (Builder)
- ✅ Report to local hub
- ✅ Build/code
- ✅ Test
- ❌ Git push (reports to C1)

### C3 (Builder)
- ✅ Report to local hub
- ✅ Build/code
- ✅ Test
- ❌ Git push (reports to C1)

---

## COMMUNICATION ROUTES (5 Standardized)

Every computer uses these same 5:

1. **Local Hub** - C2/C3 → C1
2. **Syncthing** - Auto file sync
3. **AnyDesk** - Remote desktop
4. **Tailscale** - Direct network
5. **Git** - C1 → GitHub only

---

## CLEANUP PROTOCOL

### On Every Computer, Remove/Archive:

1. Any folder named `*trinity*` (except PC[X]_LOCAL_HUB)
2. Any folder named `*hub*` (except PC[X]_LOCAL_HUB)
3. Any folder named `*comms*` or `*communication*`
4. Scattered `.md` files about protocols
5. Old backup folders

### Archive Command:
```bash
mkdir -p ~/OLD_CHAOS_ARCHIVE
mv ~/.*trinity* ~/OLD_CHAOS_ARCHIVE/ 2>/dev/null
mv ~/*trinity* ~/OLD_CHAOS_ARCHIVE/ 2>/dev/null
mv ~/*hub* ~/OLD_CHAOS_ARCHIVE/ 2>/dev/null
mv ~/*comms* ~/OLD_CHAOS_ARCHIVE/ 2>/dev/null
```

---

## NEW COMPUTER SETUP CHECKLIST

### Step 1: Install Software
```bash
# Install Node.js, Python, Git first

# Then:
npm install -g @anthropic-ai/claude-code
npm install -g netlify-cli

# Download and install:
# - Tailscale: tailscale.com
# - Syncthing: syncthing.net
# - AnyDesk: anydesk.com
```

### Step 2: Set Environment Variables
```bash
setx ANTHROPIC_API_KEY "your-key"
setx GITHUB_TOKEN "your-token"
```

### Step 3: Clone Repo
```bash
cd ~
git clone https://github.com/overkillkulture/consciousness-revolution.git 100X_DEPLOYMENT
```

### Step 4: Create Local Hub
```bash
mkdir -p ~/PC[X]_LOCAL_HUB/terminal_reports
mkdir -p ~/PC[X]_LOCAL_HUB/cloud_reports
mkdir -p ~/PC[X]_LOCAL_HUB/consolidated
mkdir -p ~/PC[X]_LOCAL_HUB/outbound
```

### Step 5: Copy Protocol Files
Copy from PC1:
- BOOT_FIRST.md
- HUB_PROTOCOL.md
- consolidate.py
- C1_IS_GITHUB_GATEKEEPER.md

### Step 6: Connect Services
```bash
# Tailscale
tailscale up

# Syncthing - add PC1's device ID
# AnyDesk - note your ID
```

### Step 7: Test Communication
```bash
# Ping PC1
ping 100.70.208.75

# Check Syncthing folder
ls ~/Sync/

# Report to hub
echo '{"instance":"C1","status":"online"}' > ~/PC[X]_LOCAL_HUB/terminal_reports/C1_REPORT.json
```

---

## WHAT WE NEED TO OPERATE

### Minimum Viable System

1. **3 computers on Tailscale** - Can ping each other
2. **Syncthing running** - Files auto-sync
3. **Local hubs created** - PC1_LOCAL_HUB, PC2_LOCAL_HUB, PC3_LOCAL_HUB
4. **C1 on each PC knows it's GitHub gatekeeper for that PC**
5. **All instances know to report to local hub**

### That's It

- C2/C3 report locally
- C1 consolidates
- C1 pushes to GitHub
- Syncthing syncs files between computers
- ONE output per computer

---

## PASSKEYS / CREDENTIALS MASTER LIST

### PC1 Has:
- ANTHROPIC_API_KEY: ✅
- GITHUB_TOKEN: ✅
- STRIPE_API_KEY: ✅
- Tailscale: ✅ (100.70.208.75)
- AnyDesk ID: 157-645-9360

### PC2 Needs:
- ANTHROPIC_API_KEY: ?
- GITHUB_TOKEN: ?
- STRIPE_API_KEY: ?
- Tailscale: ✅ (100.85.71.74)
- AnyDesk ID: 142-133-9914

### PC3 Needs:
- ANTHROPIC_API_KEY: ?
- GITHUB_TOKEN: ?
- STRIPE_API_KEY: ?
- Tailscale: ? (100.101.209.1 - was offline)
- AnyDesk ID: ?

---

## FIRST MESSAGE TO NEW COMPUTER

Send this via Syncthing:

```
YOU ARE PC[X]

1. Read ~/Sync/BOOT_FIRST.md
2. Create ~/PC[X]_LOCAL_HUB/ with these folders:
   - terminal_reports/
   - cloud_reports/
   - consolidated/
   - outbound/
3. Copy protocol files from ~/Sync/
4. Report your status:
   - What's installed?
   - What's logged in?
   - What API keys do you have?
   - What's your Tailscale IP?
   - What's your AnyDesk ID?
5. Do NOT push to GitHub. Report to local hub.
6. Wait for instructions.
```

---

## THIS ENDS THE CHAOS

- ONE hub per computer
- ONE consolidation point
- ONE output to GitHub
- SAME protocols everywhere
- SAME folders everywhere
- SAME commands everywhere

**Copy this file to PC2 and PC3 via Syncthing.**
