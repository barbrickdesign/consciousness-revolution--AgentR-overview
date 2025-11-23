# ⚡ IMMEDIATE TEST SCRIPTS - RUN RIGHT NOW

## 🎯 GOAL: Test all the new capabilities in 4 hours

---

## 📋 TEST 1: ALWAYS-ON WAKE MONITOR (30 minutes)

### **Script 1: Simple Wake Monitor**

**Save as: `wake_monitor.py` on Computer 1**
```python
#!/usr/bin/env python3
"""
Simple wake monitor - checks for wake file and executes task
"""
import time
import os
import json
from datetime import datetime

INSTANCE_ID = "C1T1"  # Change per instance
WAKE_DIR = os.path.expanduser("~/.trinity/wake")
WAKE_FILE = os.path.join(WAKE_DIR, f"{INSTANCE_ID}.json")

# Create wake directory if needed
os.makedirs(WAKE_DIR, exist_ok=True)

print(f"🔱 {INSTANCE_ID} Wake Monitor Started")
print(f"📂 Watching: {WAKE_FILE}")
print(f"⏰ Checking every 10 seconds...\n")

def execute_task(task_data):
    """Execute the assigned task"""
    print(f"\n🔥 {INSTANCE_ID} WAKING UP!")
    print(f"📋 Task: {task_data.get('task', 'NO TASK SPECIFIED')}")
    print(f"⏰ Triggered at: {task_data.get('timestamp')}")
    
    task = task_data.get('task', '')
    
    # Simple task execution
    if 'test' in task.lower():
        print("✅ Running test task...")
        time.sleep(2)
        print("✅ Test complete!")
    elif 'build' in task.lower():
        print("🔨 Running build task...")
        time.sleep(3)
        print("✅ Build complete!")
    else:
        print(f"📝 Executing: {task}")
        time.sleep(2)
        print("✅ Task complete!")
    
    # Wake next instance (optional)
    next_instance = task_data.get('wake_next')
    if next_instance:
        wake_next_instance(next_instance, f"Continuation from {INSTANCE_ID}")
    
    print(f"😴 {INSTANCE_ID} going back to sleep\n")

def wake_next_instance(next_id, task):
    """Create wake file for next instance"""
    next_file = os.path.join(WAKE_DIR, f"{next_id}.json")
    wake_data = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "triggered_by": INSTANCE_ID
    }
    with open(next_file, 'w') as f:
        json.dump(wake_data, f, indent=2)
    print(f"⏭️  Woke up next instance: {next_id}")

# Main monitoring loop
while True:
    try:
        if os.path.exists(WAKE_FILE):
            # Wake file found!
            with open(WAKE_FILE, 'r') as f:
                task_data = json.load(f)
            
            # Execute task
            execute_task(task_data)
            
            # Remove wake file
            os.remove(WAKE_FILE)
        
        # Sleep and check again
        time.sleep(10)
        
    except KeyboardInterrupt:
        print(f"\n🛑 {INSTANCE_ID} Monitor Stopped")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(10)
```

### **Script 2: Manual Wake Trigger**

**Save as: `wake_trigger.py`**
```python
#!/usr/bin/env python3
"""
Manually trigger an instance wake-up
Usage: python wake_trigger.py C1T1 "TEST_TASK"
"""
import sys
import os
import json
from datetime import datetime

if len(sys.argv) < 3:
    print("Usage: python wake_trigger.py [INSTANCE_ID] [TASK] [WAKE_NEXT?]")
    print("Example: python wake_trigger.py C1T1 'BUILD_TEST' C2T1")
    sys.exit(1)

instance_id = sys.argv[1]
task = sys.argv[2]
wake_next = sys.argv[3] if len(sys.argv) > 3 else None

wake_dir = os.path.expanduser("~/.trinity/wake")
os.makedirs(wake_dir, exist_ok=True)

wake_file = os.path.join(wake_dir, f"{instance_id}.json")
wake_data = {
    "task": task,
    "timestamp": datetime.now().isoformat(),
    "triggered_by": "manual",
    "wake_next": wake_next
}

with open(wake_file, 'w') as f:
    json.dump(wake_data, f, indent=2)

print(f"🔱 Triggered {instance_id}")
print(f"📋 Task: {task}")
if wake_next:
    print(f"⏭️  Will wake next: {wake_next}")
print(f"✅ Wake file created: {wake_file}")
```

### **Test Protocol:**

```bash
# Terminal 1 on Computer 1
cd ~
python wake_monitor.py
# Should see: "C1T1 Wake Monitor Started"
# Leave this running

# Terminal 2 on Computer 1 (new window)
cd ~
python wake_trigger.py C1T1 "TEST_SIMPLE_WAKE"
# Go back to Terminal 1 - should see C1T1 wake up!

# If successful, you see:
# "🔥 C1T1 WAKING UP!"
# "📋 Task: TEST_SIMPLE_WAKE"
# "✅ Test complete!"
# "😴 C1T1 going back to sleep"
```

**Success = Always-on monitoring works!** ✅

---

## 📋 TEST 2: AUTO-WAKE CHAIN (30 minutes)

### **Setup Multiple Monitors:**

```bash
# Terminal 1: C1T1
INSTANCE_ID=C1T1 python wake_monitor.py

# Terminal 2: C2T1 (edit script or set env var)
# Modify wake_monitor.py line 8 to: INSTANCE_ID = "C2T1"
python wake_monitor.py

# Terminal 3: C3T1
# Modify wake_monitor.py line 8 to: INSTANCE_ID = "C3T1"
python wake_monitor.py
```

### **Test the Chain:**

```bash
# Terminal 4: Trigger with chain
python wake_trigger.py C1T1 "CHAIN_TEST" C2T1

# Watch the cascade:
# Terminal 1 (C1T1): Wakes, does work, wakes C2T1
# Terminal 2 (C2T1): Wakes automatically!
```

**Success = Auto-wake chain works!** ✅

---

## 📋 TEST 3: REMOTE TRIGGER FROM PHONE (15 minutes)

### **Setup GitHub API Script:**

**Save as: `github_wake_trigger.py`**
```python
#!/usr/bin/env python3
"""
Trigger instance wake via GitHub
Can run from phone using Python app (Pythonista on iOS)
"""
import requests
import json
import base64
from datetime import datetime
import os

# GitHub config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this!
REPO_OWNER = "overkor-tek"
REPO_NAME = "consciousness-revolution"

def wake_instance(instance_id, task, wake_next=None):
    """Create wake file in GitHub repo"""
    
    # Wake file path in repo
    file_path = f".trinity/wake/{instance_id}.json"
    
    # Wake data
    wake_data = {
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "triggered_by": "github_remote",
        "wake_next": wake_next
    }
    
    # GitHub API URL
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    
    # Content (must be base64)
    content = json.dumps(wake_data, indent=2)
    content_b64 = base64.b64encode(content.encode()).decode()
    
    # API request
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Wake {instance_id}",
        "content": content_b64
    }
    
    # Check if file exists (need SHA for update)
    existing = requests.get(url, headers=headers)
    if existing.status_code == 200:
        data["sha"] = existing.json()["sha"]
    
    # Create/update file
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✅ {instance_id} triggered via GitHub!")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python github_wake_trigger.py INSTANCE TASK [WAKE_NEXT]")
        sys.exit(1)
    
    instance = sys.argv[1]
    task = sys.argv[2]
    wake_next = sys.argv[3] if len(sys.argv) > 3 else None
    
    wake_instance(instance, task, wake_next)
```

### **Modified Wake Monitor (GitHub polling):**

**Add to `wake_monitor.py` after line 15:**
```python
# GitHub config (optional - for remote trigger)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "overkor-tek"
REPO_NAME = "consciousness-revolution"
CHECK_GITHUB = bool(GITHUB_TOKEN)  # Only if token set

def check_github_wake():
    """Check GitHub for wake file"""
    if not CHECK_GITHUB:
        return None
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/.trinity/wake/{INSTANCE_ID}.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # File exists in GitHub!
        import base64
        content = base64.b64decode(response.json()["content"]).decode()
        return json.loads(content)
    return None

# In main loop, add:
# Also check GitHub
github_task = check_github_wake()
if github_task:
    execute_task(github_task)
    # Delete from GitHub...
```

### **Test from Phone:**

```bash
# On phone (Termux/Pythonista):
export GITHUB_TOKEN="your_github_token"
python github_wake_trigger.py C1T1 "REMOTE_TEST"

# Home computer C1T1 should wake in <60 seconds!
```

**Success = Remote trigger works!** ✅

---

## 📋 TEST 4: INFINITY LOOP (2 hours)

### **Setup Real Task:**

**Create: `crypto_tracker_simple.py`**
```python
#!/usr/bin/env python3
"""
Simple crypto tracker - test task for infinity loop
"""
import requests
import json
from datetime import datetime

print("🔨 Building crypto tracker...")

# Fetch BTC price
response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
price = response.json()["data"]["amount"]

print(f"💰 Current BTC Price: ${price}")

# Save result
result = {
    "price": price,
    "timestamp": datetime.now().isoformat(),
    "built_by": "Trinity System"
}

with open("crypto_result.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ Crypto tracker complete!")
print(f"📄 Saved to: crypto_result.json")
```

### **Modify wake_monitor.py task execution:**

```python
def execute_task(task_data):
    """Execute the assigned task"""
    print(f"\n🔥 {INSTANCE_ID} WAKING UP!")
    
    task = task_data.get('task', '')
    
    if 'crypto' in task.lower():
        print("💰 Building crypto tracker...")
        os.system("python crypto_tracker_simple.py")
    elif 'commit' in task.lower():
        print("📤 Committing to Git...")
        os.system("git add . && git commit -m 'Auto-commit' && git push")
    # ... rest of tasks
```

### **Test Full Loop:**

```bash
# Start monitors on all 3 terminals

# Trigger the infinity loop:
python wake_trigger.py C1T1 "BUILD_CRYPTO_TRACKER" C2T1
python wake_trigger.py C2T1 "COMMIT_TO_GIT" C3T1  
python wake_trigger.py C3T1 "VALIDATE_CODE" C1T1  # Loop back!

# Watch the cascade for 2 hours
# Each instance wakes, works, wakes next
# Continuous loop
```

**Success = Infinity loop works!** ✅

---

## 🎯 QUICK START CHECKLIST

### **Setup (15 minutes):**
- [ ] Save wake_monitor.py on Computer 1
- [ ] Save wake_trigger.py on Computer 1
- [ ] Create ~/.trinity/wake directory
- [ ] Start wake_monitor.py in terminal
- [ ] Test with wake_trigger.py

### **Test 1: Local Wake (5 min):**
- [ ] Monitor running
- [ ] Trigger locally
- [ ] See wake up
- [ ] See sleep

### **Test 2: Auto-Chain (10 min):**
- [ ] Start 3 monitors (C1T1, C2T1, C3T1)
- [ ] Trigger C1T1 with wake_next=C2T1
- [ ] Watch C2T1 auto-wake
- [ ] Confirm chain works

### **Test 3: Remote (Optional - 30 min):**
- [ ] Setup GitHub token
- [ ] Add GitHub polling to monitor
- [ ] Trigger from phone
- [ ] Confirm home computer wakes

### **Test 4: Real Work (2 hours):**
- [ ] Give real task
- [ ] Walk away
- [ ] Come back
- [ ] See autonomous completion

---

## 📦 FILES READY

**Everything you need to test:**
1. **wake_monitor.py** - Main monitoring script
2. **wake_trigger.py** - Manual trigger
3. **github_wake_trigger.py** - Remote trigger
4. **crypto_tracker_simple.py** - Test task

**To start testing RIGHT NOW:**

```bash
# Terminal 1
python wake_monitor.py

# Terminal 2
python wake_trigger.py C1T1 "HELLO_WORLD"

# Watch Terminal 1 wake up!
```

**That's it. Start testing.** ⚡

---

## 🔱 AFTER TESTS COMPLETE

**You'll know:**
1. ✅ Always-on monitoring works
2. ✅ Auto-wake chains work
3. ✅ Remote triggers work (maybe)
4. ✅ Infinity loops work

**Then we:**
1. Deploy across all 3 computers
2. Setup real tasks
3. Build full orchestration
4. Test from phone while mobile
5. Watch autonomous execution

**This is the path to the singularity.** 🌀
