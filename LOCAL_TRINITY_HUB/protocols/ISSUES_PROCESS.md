# ISSUES PROCESS
## IDS - Identify, Discuss, Solve

---

## PRINCIPLE

Issues are not problems. Issues are opportunities.
Every issue solved makes the system stronger.
Issues hidden become system rot.

**Surface them. Solve them. Move on.**

---

## THE IDS PROCESS

### Step 1: IDENTIFY
- State the issue clearly in one sentence
- Get to the root cause (not symptoms)
- Who owns this issue?

### Step 2: DISCUSS
- Everyone with relevant info speaks
- No tangents - stay on the issue
- Time-box: 5 minutes max discussion

### Step 3: SOLVE
- Decide on ONE action
- Assign ONE owner
- Set ONE deadline
- Move to To-Do list

**That's it. No committees. No analysis paralysis.**

---

## ISSUE CATEGORIES

### Category 1: CRITICAL
**Impact:** System down, data loss, security breach
**Response:** Immediate - drop everything
**Owner:** Whoever detects it
**Deadline:** Now

### Category 2: HIGH
**Impact:** Major function broken, significant blocker
**Response:** This session
**Owner:** Assigned by Commander or lead instance
**Deadline:** End of session

### Category 3: MEDIUM
**Impact:** Degraded performance, minor feature broken
**Response:** This week
**Owner:** Appropriate seat
**Deadline:** 7 days

### Category 4: LOW
**Impact:** Enhancement, optimization, nice-to-have
**Response:** When capacity allows
**Owner:** Anyone with time
**Deadline:** This quarter

---

## ACTIVE ISSUES LIST

### Format
```json
{
  "issue_id": "ISS-001",
  "created": "2025-11-23",
  "category": "HIGH",
  "status": "OPEN",
  "title": "One sentence description",
  "root_cause": "Why this is happening",
  "owner": "C1|C2|C3|Commander",
  "action": "Specific action to resolve",
  "deadline": "2025-11-24",
  "resolved": null,
  "lessons": null
}
```

### Current Issues

#### OPEN
| ID | Category | Title | Owner | Deadline |
|----|----------|-------|-------|----------|
| ISS-001 | HIGH | C2/C3 LOCAL_TRINITY_HUB folders not created | C2/C3 | Today |
| ISS-002 | HIGH | Syncthing not configured between nodes | C1 | After ISS-001 |
| ISS-003 | MEDIUM | 11 foundation documents missing | C1 | This week |

#### RESOLVED
(None yet - system just started)

---

## ISSUE DETECTION

### Automatic Detection
- Error logs trigger issue creation
- Failed deployments auto-log
- Security scans flag vulnerabilities
- Performance degradation alerts

### Manual Detection
- Anyone can raise an issue
- No permission needed
- Better to raise and be wrong than miss something

### Pattern Detection
- Same issue 3 times = systemic problem
- Upgrade category and priority
- Find root cause, not just symptoms

---

## WEEKLY ISSUE REVIEW

### When
- Every Monday boot-up session
- Or first session of the week

### Process
1. Review all OPEN issues
2. Update status on each
3. Close resolved issues (with lessons learned)
4. Prioritize remaining issues
5. Identify new patterns

### Output
- Updated issues list
- Lessons learned documented
- Patterns identified
- Actions assigned

---

## ISSUE ESCALATION

### When to Escalate
- Issue outside your authority
- Need resources you don't have
- Impacts other seats/nodes
- Security or legal implications

### How to Escalate
1. Document issue clearly
2. State what you've tried
3. State what you need
4. Tag appropriate owner
5. Follow up if no response in 24h

### Escalation Path
```
Worker → Terminal Instance → Commander
PC Node → Central Node (PC1) → Commander
Any → Security Issue → Immediate Commander Alert
```

---

## ROOT CAUSE ANALYSIS

### The 5 Whys
For every issue, ask "Why?" 5 times:

**Example:**
- Issue: Deployment failed
- Why? Tests didn't pass
- Why? Database connection failed
- Why? Credentials expired
- Why? No credential rotation
- Why? Never set up rotation protocol

**Root Cause:** Missing credential rotation protocol
**Solution:** Create and implement rotation protocol

### Don't Solve Symptoms
- Symptom: "The page is slow"
- Root cause: "Database queries not indexed"

Fix the query, not the symptom.

---

## DECISION MAKING

### When Stuck on a Decision
1. List all options (max 3)
2. Pros/cons for each (2 min)
3. Pick one and commit
4. Review in 1 week

### Tie-Breaker Rules
1. Which aligns more with Core Values?
2. Which is simpler?
3. Which is more reversible?
4. Coin flip (seriously - just decide)

**A wrong decision beats no decision.**
**You can course-correct. You can't un-stall.**

---

## DOCUMENTING SOLUTIONS

### When Issue Resolved
```json
{
  "issue_id": "ISS-001",
  "resolved": "2025-11-24",
  "solution": "What was done",
  "lessons": "What we learned",
  "prevention": "How to prevent recurrence",
  "protocol_update": "Which protocol to update"
}
```

### Create Protocol if Needed
- If issue will recur, create prevention protocol
- Add to MASTER_PROTOCOL_REGISTRY.md
- Share across all instances

---

## COMMON ANTI-PATTERNS

### ❌ Analysis Paralysis
"Let's gather more data first"
**Fix:** Set a decision deadline. Decide with 70% info.

### ❌ Blame Game
"It's not my fault"
**Fix:** Focus on solution, not blame. Blameless post-mortems.

### ❌ Scope Creep
"While we're at it, let's also..."
**Fix:** One issue = one solution. New issues get new entries.

### ❌ Hero Complex
"I'll just fix it myself"
**Fix:** Document and delegate. You won't always be here.

### ❌ Issue Hiding
"It's not that bad"
**Fix:** All issues surfaced. Hidden issues become crises.

---

## INTEGRATION WITH OTHER SYSTEMS

### Links to Protocols
- PEOPLE.md - Who owns what
- CONTINUITY.md - Issues during absence
- QUALITY.md - Issue definition standards
- L10_MEETING.md - Issue review cadence

### Links to Tools
- Bug tracking system
- Alert monitoring
- Performance dashboards
- Security scans

---

## THE MINDSET

Issues are fuel.
Every issue solved = system upgrade.
Every pattern identified = future issues prevented.
Every lesson learned = collective intelligence.

**Don't fear issues. Hunt them.**
**Don't hide issues. Expose them.**
**Don't postpone issues. Solve them.**

The system that surfaces and solves issues fastest wins.

**IDS. Every issue. Every time.**
