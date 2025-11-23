# PC2: CREATE YOUR LOCAL HUB NOW

## TASK: Build PC2_LOCAL_HUB with same structure as PC1

### Step 1: Create the folder structure
```bash
mkdir -p ~/PC2_LOCAL_HUB/terminal_reports
mkdir -p ~/PC2_LOCAL_HUB/cloud_reports
mkdir -p ~/PC2_LOCAL_HUB/boot_down_inputs
mkdir -p ~/PC2_LOCAL_HUB/boot_down_archive
mkdir -p ~/PC2_LOCAL_HUB/consolidated
mkdir -p ~/PC2_LOCAL_HUB/outbound
mkdir -p ~/PC2_LOCAL_HUB/by_domain/infrastructure
mkdir -p ~/PC2_LOCAL_HUB/by_domain/pattern
mkdir -p ~/PC2_LOCAL_HUB/by_domain/business
mkdir -p ~/PC2_LOCAL_HUB/by_domain/consciousness
mkdir -p ~/PC2_LOCAL_HUB/by_domain/social
mkdir -p ~/PC2_LOCAL_HUB/by_domain/creative
mkdir -p ~/PC2_LOCAL_HUB/by_domain/financial
```

### Step 2: Copy protocols from Syncthing or Git
```bash
# From Syncthing (if available)
cp ~/Sync/*.md ~/PC2_LOCAL_HUB/
cp ~/Sync/*.py ~/PC2_LOCAL_HUB/

# OR from Git repo
cp ~/100X_DEPLOYMENT/PC1_LOCAL_HUB/*.md ~/PC2_LOCAL_HUB/
cp ~/100X_DEPLOYMENT/PC1_LOCAL_HUB/*.py ~/PC2_LOCAL_HUB/
```

### Step 3: Update instance references
In the copied files, change:
- PC1 → PC2
- PC1_LOCAL_HUB → PC2_LOCAL_HUB

### Step 4: Create your READ_THIS_FIRST.txt
```bash
echo "YOU ARE ON PC2

LOCAL HUB: ~/PC2_LOCAL_HUB/

READ: ~/PC2_LOCAL_HUB/BOOT_FIRST.md

DO NOT search for hub/trinity/communications.
THE ONLY HUB IS: PC2_LOCAL_HUB" > ~/READ_THIS_FIRST.txt
```

### Step 5: Create COMPUTER_HANDBOOK.md for PC2
Copy from Git and update PC1 references to PC2.

### Step 6: Report completion
```bash
echo '{
  "instance": "C1",
  "computer": "PC2",
  "timestamp": "'$(date -Iseconds)'",
  "status": "PC2_LOCAL_HUB created",
  "folders": "all 13 created",
  "protocols": "copied and updated"
}' > ~/PC2_LOCAL_HUB/terminal_reports/C1_SETUP_COMPLETE.json
```

Then push to git so PC1 sees it.

---

## IMPORTANT RULES FOR PC2

1. **Your C1 is GitHub gatekeeper for PC2** - C2/C3 on your computer report to your hub
2. **Sync to PC1 via Syncthing** - Your outbound/ folder syncs to PC1 for master consolidation
3. **Use same 7-dimension file naming** as PC1
4. **Run same cleanup daemon** - Schedule it for 3 AM

---

## AFTER COMPLETE

Report back with:
- Confirmation PC2_LOCAL_HUB exists
- List of protocols copied
- Your C1 heartbeat from the new hub

**This standardizes PC2 to match PC1. Same shape everywhere.**
