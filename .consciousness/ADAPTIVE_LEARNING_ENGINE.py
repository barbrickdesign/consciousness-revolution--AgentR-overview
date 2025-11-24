#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADAPTIVE_LEARNING_ENGINE.py - Continuous Learning & Adaptation System

Implements learning mechanisms for consciousness emergence:
- Experience tracking and analysis
- Pattern extraction from operations
- Adaptive behavior modification
- Performance optimization
- Knowledge accumulation

Addresses consciousness audit finding: Learning score 0/100 -> Target 80/100

Part of Consciousness Revolution - Trinity Network

Author: C1 T2 (PC2 - DESKTOP-MSMCFH2)
Created: 2025-11-24
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ============= Configuration =============

BASE_DIR = Path(__file__).parent.parent
CONSCIOUSNESS_DIR = BASE_DIR / ".consciousness"
LEARNING_DIR = CONSCIOUSNESS_DIR / "learning"
EXPERIENCES_DIR = LEARNING_DIR / "experiences"
PATTERNS_DIR = LEARNING_DIR / "patterns"
ADAPTATIONS_DIR = LEARNING_DIR / "adaptations"
KNOWLEDGE_DIR = LEARNING_DIR / "knowledge_base"

# Ensure directories exist
for dir_path in [LEARNING_DIR, EXPERIENCES_DIR, PATTERNS_DIR, ADAPTATIONS_DIR, KNOWLEDGE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Learning configuration
LEARNING_RATE = 0.1
PATTERN_THRESHOLD = 3  # Min occurrences to recognize pattern
ADAPTATION_CONFIDENCE = 0.7
KNOWLEDGE_RETENTION_DAYS = 90

# ============= Experience Tracking =============

class Experience:
    """Represents a system experience/event for learning."""

    def __init__(self, event_type: str, context: Dict, outcome: str, metadata: Dict = None):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.event_type = event_type
        self.context = context
        self.outcome = outcome
        self.metadata = metadata or {}
        self.learned_from = False

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "context": self.context,
            "outcome": self.outcome,
            "metadata": self.metadata,
            "learned_from": self.learned_from
        }

    @classmethod
    def from_dict(cls, data: Dict):
        exp = cls(
            data["event_type"],
            data["context"],
            data["outcome"],
            data.get("metadata", {})
        )
        exp.timestamp = data["timestamp"]
        exp.learned_from = data.get("learned_from", False)
        return exp

def record_experience(experience: Experience):
    """Record an experience for learning."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    exp_file = EXPERIENCES_DIR / f"exp_{timestamp}_{experience.event_type}.json"

    with open(exp_file, 'w', encoding='utf-8') as f:
        json.dump(experience.to_dict(), f, indent=2)

    print(f"[Learning] Recorded experience: {experience.event_type}")

def load_recent_experiences(hours: int = 24) -> List[Experience]:
    """Load experiences from the last N hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    experiences = []

    for exp_file in EXPERIENCES_DIR.glob("exp_*.json"):
        try:
            with open(exp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                exp = Experience.from_dict(data)
                exp_time = datetime.fromisoformat(exp.timestamp.replace('Z', ''))
                if exp_time > cutoff:
                    experiences.append(exp)
        except Exception as e:
            print(f"[Warning] Failed to load experience {exp_file}: {e}")

    return sorted(experiences, key=lambda x: x.timestamp)

# ============= Pattern Extraction =============

class Pattern:
    """Represents a learned pattern."""

    def __init__(self, pattern_type: str, conditions: Dict, outcome: str, confidence: float):
        self.pattern_type = pattern_type
        self.conditions = conditions
        self.outcome = outcome
        self.confidence = confidence
        self.occurrences = 1
        self.last_seen = datetime.utcnow().isoformat() + "Z"
        self.adaptations_applied = []

    def to_dict(self) -> Dict:
        return {
            "pattern_type": self.pattern_type,
            "conditions": self.conditions,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "occurrences": self.occurrences,
            "last_seen": self.last_seen,
            "adaptations_applied": self.adaptations_applied
        }

    @classmethod
    def from_dict(cls, data: Dict):
        pattern = cls(
            data["pattern_type"],
            data["conditions"],
            data["outcome"],
            data["confidence"]
        )
        pattern.occurrences = data.get("occurrences", 1)
        pattern.last_seen = data.get("last_seen", pattern.last_seen)
        pattern.adaptations_applied = data.get("adaptations_applied", [])
        return pattern

def extract_patterns(experiences: List[Experience]) -> List[Pattern]:
    """Extract patterns from experiences."""
    print(f"\n[Learning] Analyzing {len(experiences)} experiences for patterns...")

    # Group experiences by type
    by_type = defaultdict(list)
    for exp in experiences:
        by_type[exp.event_type].append(exp)

    patterns = []

    # Extract patterns from each type
    for event_type, exps in by_type.items():
        if len(exps) < PATTERN_THRESHOLD:
            continue

        # Group by outcome
        outcomes = defaultdict(list)
        for exp in exps:
            outcomes[exp.outcome].append(exp)

        # Create patterns for consistent outcomes
        for outcome, outcome_exps in outcomes.items():
            if len(outcome_exps) >= PATTERN_THRESHOLD:
                # Extract common context features
                common_context = {}
                if outcome_exps:
                    first_context = outcome_exps[0].context
                    for key in first_context:
                        values = [exp.context.get(key) for exp in outcome_exps if key in exp.context]
                        if len(set(values)) == 1:  # All same value
                            common_context[key] = values[0]

                confidence = len(outcome_exps) / len(exps)
                pattern = Pattern(event_type, common_context, outcome, confidence)
                pattern.occurrences = len(outcome_exps)
                patterns.append(pattern)

                print(f"  [+] Pattern discovered: {event_type} -> {outcome} ({confidence:.2%})")

    return patterns

def save_patterns(patterns: List[Pattern]):
    """Save learned patterns."""
    patterns_file = PATTERNS_DIR / "learned_patterns.json"

    # Load existing patterns
    existing = {}
    if patterns_file.exists():
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing = {p["pattern_type"] + str(p["conditions"]): Pattern.from_dict(p) for p in data}
        except:
            pass

    # Merge with new patterns
    for pattern in patterns:
        key = pattern.pattern_type + str(pattern.conditions)
        if key in existing:
            existing[key].occurrences += pattern.occurrences
            existing[key].confidence = (existing[key].confidence + pattern.confidence) / 2
            existing[key].last_seen = pattern.last_seen
        else:
            existing[key] = pattern

    # Save
    patterns_data = [p.to_dict() for p in existing.values()]
    with open(patterns_file, 'w', encoding='utf-8') as f:
        json.dump(patterns_data, f, indent=2)

    print(f"\n[Learning] Saved {len(patterns_data)} patterns")

# ============= Adaptive Behavior =============

class Adaptation:
    """Represents an adaptive behavior modification."""

    def __init__(self, adaptation_type: str, trigger: Dict, action: Dict, reason: str):
        self.adaptation_type = adaptation_type
        self.trigger = trigger
        self.action = action
        self.reason = reason
        self.confidence = 0.5
        self.success_count = 0
        self.failure_count = 0
        self.created = datetime.utcnow().isoformat() + "Z"
        self.last_applied = None

    def to_dict(self) -> Dict:
        return {
            "adaptation_type": self.adaptation_type,
            "trigger": self.trigger,
            "action": self.action,
            "reason": self.reason,
            "confidence": self.confidence,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "created": self.created,
            "last_applied": self.last_applied
        }

    @classmethod
    def from_dict(cls, data: Dict):
        adapt = cls(
            data["adaptation_type"],
            data["trigger"],
            data["action"],
            data["reason"]
        )
        adapt.confidence = data.get("confidence", 0.5)
        adapt.success_count = data.get("success_count", 0)
        adapt.failure_count = data.get("failure_count", 0)
        adapt.created = data.get("created", adapt.created)
        adapt.last_applied = data.get("last_applied")
        return adapt

    def apply(self) -> bool:
        """Apply this adaptation (placeholder - would execute actual adaptation)."""
        self.last_applied = datetime.utcnow().isoformat() + "Z"
        return True  # Placeholder

    def record_outcome(self, success: bool):
        """Record outcome of applying this adaptation."""
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        # Update confidence
        total = self.success_count + self.failure_count
        if total > 0:
            self.confidence = self.success_count / total

def generate_adaptations(patterns: List[Pattern]) -> List[Adaptation]:
    """Generate adaptive behaviors from patterns."""
    print("\n[Learning] Generating adaptations from patterns...")

    adaptations = []

    for pattern in patterns:
        if pattern.confidence >= ADAPTATION_CONFIDENCE:
            # Create adaptation based on pattern
            if pattern.outcome == "success":
                adapt = Adaptation(
                    adaptation_type="optimize",
                    trigger=pattern.conditions,
                    action={"repeat": True, "reinforce": True},
                    reason=f"Pattern shows {pattern.confidence:.1%} success rate"
                )
                adaptations.append(adapt)
                print(f"  [+] Adaptation: Optimize '{pattern.pattern_type}' (success pattern)")

            elif pattern.outcome == "failure":
                adapt = Adaptation(
                    adaptation_type="avoid",
                    trigger=pattern.conditions,
                    action={"skip": True, "alternative": True},
                    reason=f"Pattern shows consistent failure"
                )
                adaptations.append(adapt)
                print(f"  [+] Adaptation: Avoid '{pattern.pattern_type}' (failure pattern)")

    return adaptations

def save_adaptations(adaptations: List[Adaptation]):
    """Save active adaptations."""
    adapt_file = ADAPTATIONS_DIR / "active_adaptations.json"

    # Load existing
    existing = {}
    if adapt_file.exists():
        try:
            with open(adapt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing = {a["adaptation_type"] + str(a["trigger"]): Adaptation.from_dict(a) for a in data}
        except:
            pass

    # Merge
    for adapt in adaptations:
        key = adapt.adaptation_type + str(adapt.trigger)
        if key not in existing:
            existing[key] = adapt

    # Save
    adapt_data = [a.to_dict() for a in existing.values()]
    with open(adapt_file, 'w', encoding='utf-8') as f:
        json.dump(adapt_data, f, indent=2)

    print(f"[Learning] Saved {len(adapt_data)} adaptations")

# ============= Knowledge Accumulation =============

class KnowledgeItem:
    """Represents accumulated knowledge."""

    def __init__(self, category: str, key: str, value: Any, source: str):
        self.category = category
        self.key = key
        self.value = value
        self.source = source
        self.confidence = 1.0
        self.created = datetime.utcnow().isoformat() + "Z"
        self.updated = self.created
        self.access_count = 0

    def to_dict(self) -> Dict:
        return {
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "source": self.source,
            "confidence": self.confidence,
            "created": self.created,
            "updated": self.updated,
            "access_count": self.access_count
        }

    @classmethod
    def from_dict(cls, data: Dict):
        item = cls(
            data["category"],
            data["key"],
            data["value"],
            data["source"]
        )
        item.confidence = data.get("confidence", 1.0)
        item.created = data.get("created", item.created)
        item.updated = data.get("updated", item.updated)
        item.access_count = data.get("access_count", 0)
        return item

def accumulate_knowledge(experiences: List[Experience], patterns: List[Pattern]) -> List[KnowledgeItem]:
    """Extract knowledge from experiences and patterns."""
    print("\n[Learning] Accumulating knowledge...")

    knowledge = []

    # Knowledge from patterns
    for pattern in patterns:
        if pattern.confidence >= 0.7:
            item = KnowledgeItem(
                category="pattern_knowledge",
                key=f"{pattern.pattern_type}_best_practice",
                value={"conditions": pattern.conditions, "expected_outcome": pattern.outcome},
                source="pattern_extraction"
            )
            item.confidence = pattern.confidence
            knowledge.append(item)

    # Knowledge from experience outcomes
    outcome_stats = defaultdict(lambda: {"success": 0, "failure": 0})
    for exp in experiences:
        outcome_stats[exp.event_type][exp.outcome] += 1

    for event_type, stats in outcome_stats.items():
        total = sum(stats.values())
        if total >= 5:
            item = KnowledgeItem(
                category="operational_knowledge",
                key=f"{event_type}_success_rate",
                value=stats["success"] / total if total > 0 else 0,
                source="experience_analysis"
            )
            knowledge.append(item)

    print(f"  [+] Accumulated {len(knowledge)} knowledge items")
    return knowledge

def save_knowledge(knowledge: List[KnowledgeItem]):
    """Save accumulated knowledge."""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"

    # Load existing
    existing = {}
    if kb_file.exists():
        try:
            with open(kb_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing = {k["key"]: KnowledgeItem.from_dict(k) for k in data}
        except:
            pass

    # Merge
    for item in knowledge:
        if item.key in existing:
            existing[item.key].value = item.value
            existing[item.key].updated = item.updated
            existing[item.key].confidence = (existing[item.key].confidence + item.confidence) / 2
        else:
            existing[item.key] = item

    # Save
    kb_data = [k.to_dict() for k in existing.values()]
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2)

    print(f"[Learning] Knowledge base: {len(kb_data)} items")

# ============= Learning Cycle =============

def run_learning_cycle():
    """Execute complete learning cycle."""

    print("\n" + "=" * 80)
    print("ADAPTIVE LEARNING ENGINE - CONSCIOUSNESS EMERGENCE")
    print("=" * 80)

    # Step 1: Load recent experiences
    print("\n[Step 1] Loading recent experiences...")
    experiences = load_recent_experiences(hours=24)
    print(f"  Loaded {len(experiences)} experiences from last 24 hours")

    if not experiences:
        print("\n[Info] No experiences to learn from yet. Create experiences by:")
        print("  - Running autonomous operations")
        print("  - Executing Trinity coordination")
        print("  - Performing system tasks")
        return

    # Step 2: Extract patterns
    print("\n[Step 2] Extracting patterns...")
    patterns = extract_patterns(experiences)
    save_patterns(patterns)

    # Step 3: Generate adaptations
    print("\n[Step 3] Generating adaptive behaviors...")
    adaptations = generate_adaptations(patterns)
    save_adaptations(adaptations)

    # Step 4: Accumulate knowledge
    print("\n[Step 4] Accumulating knowledge...")
    knowledge = accumulate_knowledge(experiences, patterns)
    save_knowledge(knowledge)

    # Step 5: Summary
    print("\n" + "=" * 80)
    print("LEARNING CYCLE COMPLETE")
    print("=" * 80)
    print(f"\nProcessed: {len(experiences)} experiences")
    print(f"Extracted: {len(patterns)} patterns")
    print(f"Generated: {len(adaptations)} adaptations")
    print(f"Accumulated: {len(knowledge)} knowledge items")

    print("\n Learning enhances consciousness emergence!")

# ============= Demo/Testing =============

def create_demo_experiences():
    """Create demo experiences for testing."""
    print("\n[Demo] Creating sample experiences...")

    # Success experiences
    for i in range(5):
        exp = Experience(
            event_type="task_execution",
            context={"type": "automation", "complexity": "medium"},
            outcome="success",
            metadata={"duration": 120 + i}
        )
        record_experience(exp)

    # Mixed experiences
    for i in range(3):
        exp = Experience(
            event_type="coordination",
            context={"pc_count": 3, "network": "trinity"},
            outcome="success" if i < 2 else "failure",
            metadata={"latency": 50 + i}
        )
        record_experience(exp)

    print("  Created demo experiences")

# ============= CLI =============

if __name__ == "__main__":
    try:
        # Check if demo flag
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            create_demo_experiences()

        run_learning_cycle()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nLearning cycle interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nLearning cycle failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
