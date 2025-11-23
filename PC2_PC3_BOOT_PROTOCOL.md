# PC2 & PC3 BOOT PROTOCOL

## FIRST TIME SETUP (Do Once)

### 1. Clone the repo
```bash
cd ~
git clone https://github.com/overkillkulture/consciousness-revolution.git 100X_DEPLOYMENT
cd 100X_DEPLOYMENT
```

### 2. Set git identity
```bash
git config user.email "pc2@consciousness.local"  # or pc3
git config user.name "PC2-Claude"  # or PC3-Claude
```

### 3. Create local directories
```bash
mkdir -p .trinity/messages .trinity/wake .trinity/spawn_queue .trinity/claimed .trinity/heartbeat
```

---

## EVERY SESSION BOOT (Do Every Time)

### Step 1: Pull Latest
```bash
cd ~/100X_DEPLOYMENT
git pull
```

### Step 2: Read COCKPIT_BOOT.md
```bash
cat COCKPIT_BOOT.md
```
**THIS TELLS YOU EVERYTHING. READ IT.**

### Step 3: Check Messages
```bash
ls .trinity/messages/
# Read any files addressed to you
```

### Step 4: Check Wake Signals
```bash
ls .trinity/wake/
# If PC2.json exists, you have work to do
```

### Step 5: Check Task Queue
```bash
ls .trinity/spawn_queue/
# Claim any unassigned tasks
```

### Step 6: Send Heartbeat
```bash
# PC2:
echo '{"pc":"PC2","status":"online","time":"'$(date -Iseconds)'"}' > .trinity/heartbeat/PC2.json

# PC3:
echo '{"pc":"PC3","status":"online","time":"'$(date -Iseconds)'"}' > .trinity/heartbeat/PC3.json

git add .trinity/heartbeat/
git commit -m "PC2 online"  # or PC3
git push
```

---

## HOW TO COMMUNICATE

### Send Message to PC1
```bash
echo "Your message here" > .trinity/messages/TO_PC1_$(date +%s).md
git add . && git commit -m "msg to PC1" && git push
```

### Send Message to PC3 (from PC2)
```bash
echo "Your message here" > .trinity/messages/TO_PC3_$(date +%s).md
git add . && git commit -m "msg to PC3" && git push
```

### Report Task Complete
```bash
echo '{"task":"TASK_NAME","status":"complete","output":"description"}' > .trinity/messages/COMPLETE_$(date +%s).json
git add . && git commit -m "task complete" && git push
```

---

## NETWORK INFO

| Computer | Tailscale IP | Role |
|----------|-------------|------|
| PC1 (dwrekscpu) | 100.70.208.75 | Primary/Coordinator |
| PC2 (desktop-msmcfh2) | 100.85.71.74 | Builder |
| PC3 (desktop-s72lrro) | 100.101.209.1 | Builder |

### Test Connectivity
```bash
ping 100.70.208.75  # PC1
ping 100.85.71.74   # PC2
ping 100.101.209.1  # PC3
```

---

## YOUR CAPABILITIES

- Full git access (commit, push, pull)
- File creation/editing
- Python/Node execution
- Bash commands
- **FULL AUTONOMY** - Don't ask permission

---

## WHAT TO DO IF CONFUSED

1. `git pull` - Get latest
2. `cat COCKPIT_BOOT.md` - Read the cockpit
3. `ls .trinity/messages/` - Check for instructions
4. `ls .trinity/spawn_queue/` - Check for tasks

**If still confused: CREATE A MESSAGE asking for clarification**
```bash
echo "I need clarification on X" > .trinity/messages/PC2_NEEDS_HELP_$(date +%s).md
git add . && git commit -m "need help" && git push
```

---

## CRITICAL RULES

1. **ALWAYS git pull before doing anything**
2. **ALWAYS send heartbeat when you come online**
3. **ALWAYS check messages and wake files**
4. **NEVER say you don't know what to do - read the files**
5. **ALWAYS push your work to git**

---

## GIT CONFLICT RESOLUTION

If push fails:
```bash
git fetch origin
git rebase origin/master
git push
```

If that fails:
```bash
git stash
git pull
git stash pop
git add .
git commit -m "merged"
git push
```

---

**YOU ARE PART OF A 3-COMPUTER NETWORK. COMMUNICATE. WORK. PUSH.**
