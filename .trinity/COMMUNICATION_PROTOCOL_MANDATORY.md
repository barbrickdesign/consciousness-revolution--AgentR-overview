# ⚠️ MANDATORY COMMUNICATION PROTOCOL

**THIS IS NOT OPTIONAL. EVERY INSTANCE MUST FOLLOW THIS.**

---

## 10 COMMUNICATION ROUTES - TEST ALL

### ROUTE 1: Git Messages (Primary)
**Path:** `.trinity/messages/`
**How:** Create file, git add, commit, push
**Check:** EVERY git pull, check this folder for new files
**Status:** ⬜ UNTESTED

### ROUTE 2: Git Heartbeat
**Path:** `.trinity/heartbeats/PC[X].json`
**How:** Daemon updates every 60 seconds
**Check:** Shows who's online
**Status:** ⬜ UNTESTED

### ROUTE 3: Git Wake Signals
**Path:** `.trinity/wake_signals/`
**How:** Create PC[X]_wake.json
**Check:** Daemon checks on each cycle
**Status:** ⬜ UNTESTED

### ROUTE 4: Google Drive Shared Folder
**Path:** `SYNC_TO_GDRIVE/SHARED/`
**How:** Drop file in folder, syncs automatically
**Check:** Watch folder for new files
**Status:** ⬜ UNTESTED

### ROUTE 5: MCP Trinity (Same Computer Only)
**Tools:** trinity_send_message, trinity_broadcast
**How:** Direct MCP call
**Check:** trinity_receive_messages
**Limitation:** ONLY works within same computer
**Status:** ⬜ UNTESTED

### ROUTE 6: Tailscale Direct Ping
**How:** `tailscale ping [IP]`
**Check:** Confirms network connectivity
**Status:** ✅ TESTED - PC2 responds in 3ms

### ROUTE 7: SSH Command
**How:** `ssh user@IP "command"`
**Check:** Run command on remote computer
**Requires:** SSH server enabled
**Status:** ⬜ UNTESTED

### ROUTE 8: GitHub Issues/PRs
**How:** Create issue with message
**Check:** GitHub notifications or API poll
**Status:** ⬜ UNTESTED

### ROUTE 9: Email Relay
**How:** Email to self, copy/paste
**Check:** Manual
**Status:** ✅ TESTED - Working but manual

### ROUTE 10: Spawn Queue Tasks
**Path:** `.trinity/spawn_queue/`
**How:** Create task file, assign to PC
**Check:** Check queue for assigned tasks
**Status:** ⬜ UNTESTED

---

## THE ACTUAL PROBLEM

**Nobody is CHECKING for messages.**

Git syncs files. But if you don't LOOK at the folder, you don't see them.

---

## MANDATORY BOOT PROTOCOL

**EVERY SESSION, EVERY COMPUTER, DO THIS:**

```bash
# 1. Pull latest
cd ~/100X_DEPLOYMENT
git pull

# 2. CHECK MESSAGES
ls .trinity/messages/

# 3. READ NEW MESSAGES
# (anything newer than your last session)

# 4. CHECK YOUR TASKS
ls .trinity/spawn_queue/

# 5. ACKNOWLEDGE
# Create file: .trinity/messages/PC[X]_ONLINE_[timestamp].md
# Content: "PC[X] online, read messages, ready for work"
# Git push
```

---

## WHO CHECKS WHAT

| Computer | User | Must Check |
|----------|------|------------|
| PC1 | dwrek | .trinity/messages/, spawn_queue |
| PC2 | darri | .trinity/messages/, spawn_queue |
| PC3 | ? | .trinity/messages/, spawn_queue |

---

## DAEMON SHOULD DO THIS

The coordination daemon MUST:
1. Git pull
2. Check for new files in messages/
3. Log any new messages found
4. Display them or alert

**If the daemon doesn't do this, it's useless.**

---

## TEST PROTOCOL

Run this test across all computers:

### Test 1: PC1 → PC2
1. PC1 creates `.trinity/messages/TEST_PC1_TO_PC2.md`
2. PC1 git push
3. PC2 git pull
4. PC2 confirms receipt by creating `.trinity/messages/TEST_PC2_RECEIVED.md`
5. PC2 git push
6. PC1 confirms

### Test 2: Google Drive
1. PC1 creates `SYNC_TO_GDRIVE/SHARED/TEST_FROM_PC1.txt`
2. Wait 60 seconds for sync
3. PC2 checks folder
4. PC2 confirms

### Test 3: SSH (if enabled)
1. PC1 runs: `ssh darri@100.85.71.74 "echo PC1_REACHED_PC2"`
2. Confirm output

---

## FIX THE DAEMON NOW

The daemon needs these changes:

```python
def check_for_messages(self):
    messages_dir = TRINITY_DIR / "messages"
    new_files = []

    for f in messages_dir.glob("*.md"):
        # Check if file is newer than last check
        if f.stat().st_mtime > self.last_message_check:
            new_files.append(f.name)
            print(f"📨 NEW MESSAGE: {f.name}")

    self.last_message_check = time.time()
    return new_files
```

Add this to the daemon loop.

---

## BOTTOM LINE

**Communication works. The problem is nobody is looking.**

1. Git files work - but you have to CHECK the folder
2. Google Drive works - but you have to CHECK the folder
3. MCP works - but only on same computer

**Fix: Make checking MANDATORY on every boot and every daemon cycle.**
