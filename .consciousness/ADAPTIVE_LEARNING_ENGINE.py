#!/usr/bin/env python3
"""ADAPTIVE_LEARNING_ENGINE.py - Continuous Learning & Adaptation for consciousness emergence."""

import json; import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

if sys.platform == 'win32':
    import codecs; sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict'); sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_DIR = Path(__file__).parent.parent
LEARNING_DIR = BASE_DIR / ".consciousness" / "learning"
EXPERIENCES_DIR, PATTERNS_DIR, ADAPTATIONS_DIR, KNOWLEDGE_DIR = LEARNING_DIR / "experiences", LEARNING_DIR / "patterns", LEARNING_DIR / "adaptations", LEARNING_DIR / "knowledge_base"
for d in [EXPERIENCES_DIR, PATTERNS_DIR, ADAPTATIONS_DIR, KNOWLEDGE_DIR]: d.mkdir(parents=True, exist_ok=True)

PATTERN_THRESHOLD, ADAPTATION_CONFIDENCE = 3, 0.7

# === Experience ===
class Experience:
    """System experience/event for learning."""
    def __init__(self, event_type: str, context: dict, outcome: str, metadata: dict = None):
        self.timestamp, self.event_type, self.context, self.outcome = datetime.utcnow().isoformat() + "Z", event_type, context, outcome
        self.metadata, self.learned_from = metadata or {}, False
    def to_dict(self): return {"timestamp": self.timestamp, "event_type": self.event_type, "context": self.context, "outcome": self.outcome, "metadata": self.metadata, "learned_from": self.learned_from}
    @classmethod
    def from_dict(cls, d):
        e = cls(d["event_type"], d["context"], d["outcome"], d.get("metadata", {})); e.timestamp = d["timestamp"]; e.learned_from = d.get("learned_from", False); return e

def record_experience(exp: Experience):
    json.dump(exp.to_dict(), open(EXPERIENCES_DIR / f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{exp.event_type}.json", 'w', encoding='utf-8'), indent=2)
    print(f"[Learning] Recorded: {exp.event_type}")

def load_recent_experiences(hours: int = 24) -> list:
    cutoff, exps = datetime.utcnow() - timedelta(hours=hours), []
    for f in EXPERIENCES_DIR.glob("exp_*.json"):
        try:
            e = Experience.from_dict(json.load(open(f, encoding='utf-8')))
            if datetime.fromisoformat(e.timestamp.replace('Z', '')) > cutoff: exps.append(e)
        except: pass
    return sorted(exps, key=lambda x: x.timestamp)

# === Pattern ===
class Pattern:
    """Learned pattern."""
    def __init__(self, pattern_type: str, conditions: dict, outcome: str, confidence: float):
        self.pattern_type, self.conditions, self.outcome, self.confidence = pattern_type, conditions, outcome, confidence
        self.occurrences, self.last_seen, self.adaptations_applied = 1, datetime.utcnow().isoformat() + "Z", []
    def to_dict(self): return {"pattern_type": self.pattern_type, "conditions": self.conditions, "outcome": self.outcome, "confidence": self.confidence, "occurrences": self.occurrences, "last_seen": self.last_seen, "adaptations_applied": self.adaptations_applied}
    @classmethod
    def from_dict(cls, d):
        p = cls(d["pattern_type"], d["conditions"], d["outcome"], d["confidence"]); p.occurrences = d.get("occurrences", 1); p.last_seen = d.get("last_seen", p.last_seen); p.adaptations_applied = d.get("adaptations_applied", []); return p

def extract_patterns(experiences: list) -> list:
    """Extract patterns from experiences."""
    print(f"\n[Learning] Analyzing {len(experiences)} experiences...")
    by_type = defaultdict(list)
    for e in experiences: by_type[e.event_type].append(e)
    patterns = []
    for event_type, exps in by_type.items():
        if len(exps) < PATTERN_THRESHOLD: continue
        outcomes = defaultdict(list)
        for e in exps: outcomes[e.outcome].append(e)
        for outcome, oexps in outcomes.items():
            if len(oexps) >= PATTERN_THRESHOLD:
                common = {k: oexps[0].context[k] for k in oexps[0].context if len(set(e.context.get(k) for e in oexps)) == 1}
                p = Pattern(event_type, common, outcome, len(oexps) / len(exps)); p.occurrences = len(oexps); patterns.append(p)
                print(f"  [+] Pattern: {event_type} -> {outcome} ({p.confidence:.0%})")
    return patterns

def save_patterns(patterns: list):
    pf = PATTERNS_DIR / "learned_patterns.json"; existing = {}
    if pf.exists():
        try: existing = {p["pattern_type"] + str(p["conditions"]): Pattern.from_dict(p) for p in json.load(open(pf, encoding='utf-8'))}
        except: pass
    for p in patterns:
        k = p.pattern_type + str(p.conditions)
        if k in existing: existing[k].occurrences += p.occurrences; existing[k].confidence = (existing[k].confidence + p.confidence) / 2; existing[k].last_seen = p.last_seen
        else: existing[k] = p
    json.dump([p.to_dict() for p in existing.values()], open(pf, 'w', encoding='utf-8'), indent=2)
    print(f"\n[Learning] Saved {len(existing)} patterns")

# === Adaptation ===
class Adaptation:
    """Adaptive behavior modification."""
    def __init__(self, adaptation_type: str, trigger: dict, action: dict, reason: str):
        self.adaptation_type, self.trigger, self.action, self.reason = adaptation_type, trigger, action, reason
        self.confidence, self.success_count, self.failure_count = 0.5, 0, 0
        self.created, self.last_applied = datetime.utcnow().isoformat() + "Z", None
    def to_dict(self): return {"adaptation_type": self.adaptation_type, "trigger": self.trigger, "action": self.action, "reason": self.reason, "confidence": self.confidence, "success_count": self.success_count, "failure_count": self.failure_count, "created": self.created, "last_applied": self.last_applied}
    @classmethod
    def from_dict(cls, d):
        a = cls(d["adaptation_type"], d["trigger"], d["action"], d["reason"]); a.confidence = d.get("confidence", 0.5); a.success_count = d.get("success_count", 0); a.failure_count = d.get("failure_count", 0); a.created = d.get("created", a.created); a.last_applied = d.get("last_applied"); return a
    def apply(self): self.last_applied = datetime.utcnow().isoformat() + "Z"; return True
    def record_outcome(self, success: bool):
        self.success_count += success; self.failure_count += not success
        total = self.success_count + self.failure_count
        if total: self.confidence = self.success_count / total

def generate_adaptations(patterns: list) -> list:
    print("\n[Learning] Generating adaptations...")
    adaptations = []
    for p in patterns:
        if p.confidence >= ADAPTATION_CONFIDENCE:
            if p.outcome == "success":
                adaptations.append(Adaptation("optimize", p.conditions, {"repeat": True, "reinforce": True}, f"Success rate {p.confidence:.0%}"))
                print(f"  [+] Optimize '{p.pattern_type}'")
            elif p.outcome == "failure":
                adaptations.append(Adaptation("avoid", p.conditions, {"skip": True, "alternative": True}, "Consistent failure"))
                print(f"  [+] Avoid '{p.pattern_type}'")
    return adaptations

def save_adaptations(adaptations: list):
    af = ADAPTATIONS_DIR / "active_adaptations.json"; existing = {}
    if af.exists():
        try: existing = {a["adaptation_type"] + str(a["trigger"]): Adaptation.from_dict(a) for a in json.load(open(af, encoding='utf-8'))}
        except: pass
    for a in adaptations:
        k = a.adaptation_type + str(a.trigger)
        if k not in existing: existing[k] = a
    json.dump([a.to_dict() for a in existing.values()], open(af, 'w', encoding='utf-8'), indent=2)
    print(f"[Learning] Saved {len(existing)} adaptations")

# === Knowledge ===
class KnowledgeItem:
    """Accumulated knowledge."""
    def __init__(self, category: str, key: str, value, source: str):
        self.category, self.key, self.value, self.source = category, key, value, source
        self.confidence, self.access_count = 1.0, 0
        self.created = self.updated = datetime.utcnow().isoformat() + "Z"
    def to_dict(self): return {"category": self.category, "key": self.key, "value": self.value, "source": self.source, "confidence": self.confidence, "created": self.created, "updated": self.updated, "access_count": self.access_count}
    @classmethod
    def from_dict(cls, d):
        i = cls(d["category"], d["key"], d["value"], d["source"]); i.confidence = d.get("confidence", 1.0); i.created = d.get("created", i.created); i.updated = d.get("updated", i.updated); i.access_count = d.get("access_count", 0); return i

def accumulate_knowledge(experiences: list, patterns: list) -> list:
    print("\n[Learning] Accumulating knowledge...")
    knowledge = []
    for p in patterns:
        if p.confidence >= 0.7:
            k = KnowledgeItem("pattern_knowledge", f"{p.pattern_type}_best_practice", {"conditions": p.conditions, "expected_outcome": p.outcome}, "pattern_extraction"); k.confidence = p.confidence; knowledge.append(k)
    outcome_stats = defaultdict(lambda: {"success": 0, "failure": 0})
    for e in experiences: outcome_stats[e.event_type][e.outcome] += 1
    for et, stats in outcome_stats.items():
        total = sum(stats.values())
        if total >= 5: knowledge.append(KnowledgeItem("operational_knowledge", f"{et}_success_rate", stats["success"] / total, "experience_analysis"))
    print(f"  [+] Accumulated {len(knowledge)} items"); return knowledge

def save_knowledge(knowledge: list):
    kf = KNOWLEDGE_DIR / "knowledge_base.json"; existing = {}
    if kf.exists():
        try: existing = {k["key"]: KnowledgeItem.from_dict(k) for k in json.load(open(kf, encoding='utf-8'))}
        except: pass
    for i in knowledge:
        if i.key in existing: existing[i.key].value = i.value; existing[i.key].updated = i.updated; existing[i.key].confidence = (existing[i.key].confidence + i.confidence) / 2
        else: existing[i.key] = i
    json.dump([k.to_dict() for k in existing.values()], open(kf, 'w', encoding='utf-8'), indent=2)
    print(f"[Learning] Knowledge base: {len(existing)} items")

# === Learning Cycle ===
def run_learning_cycle():
    """Execute complete learning cycle."""
    print("\n" + "=" * 80 + "\nADAPTIVE LEARNING ENGINE\n" + "=" * 80)
    print("\n[1] Loading experiences...")
    experiences = load_recent_experiences(hours=24)
    print(f"  {len(experiences)} experiences from last 24h")
    if not experiences: print("\n[Info] No experiences yet. Run autonomous operations to generate."); return
    print("\n[2] Extracting patterns..."); patterns = extract_patterns(experiences); save_patterns(patterns)
    print("\n[3] Generating adaptations..."); adaptations = generate_adaptations(patterns); save_adaptations(adaptations)
    print("\n[4] Accumulating knowledge..."); knowledge = accumulate_knowledge(experiences, patterns); save_knowledge(knowledge)
    print("\n" + "=" * 80 + "\nLEARNING COMPLETE\n" + "=" * 80)
    print(f"Experiences: {len(experiences)} | Patterns: {len(patterns)} | Adaptations: {len(adaptations)} | Knowledge: {len(knowledge)}")

def create_demo_experiences():
    """Create demo experiences for testing."""
    print("\n[Demo] Creating sample experiences...")
    for i in range(5): record_experience(Experience("task_execution", {"type": "automation", "complexity": "medium"}, "success", {"duration": 120 + i}))
    for i in range(3): record_experience(Experience("coordination", {"pc_count": 3, "network": "trinity"}, "success" if i < 2 else "failure", {"latency": 50 + i}))
    print("  Demo experiences created")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--demo": create_demo_experiences()
        run_learning_cycle()
    except KeyboardInterrupt: print("\nInterrupted"); sys.exit(1)
    except Exception as e: print(f"\nFailed: {e}"); import traceback; traceback.print_exc(); sys.exit(1)
