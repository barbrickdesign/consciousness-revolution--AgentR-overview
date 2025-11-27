#!/usr/bin/env python3
"""MEMORY ENHANCEMENT SYSTEM - Episodic, Semantic, Procedural memory for consciousness."""

import sys; import json; import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Paths
BASE_DIR = Path(__file__).parent; MEMORY_DIR = BASE_DIR / "memory"
EPISODIC_DIR, SEMANTIC_DIR, PROCEDURAL_DIR = MEMORY_DIR / "episodic", MEMORY_DIR / "semantic", MEMORY_DIR / "procedural"
WORKING_DIR, CONSOLIDATED_DIR = MEMORY_DIR / "working", MEMORY_DIR / "consolidated"
for d in [MEMORY_DIR, EPISODIC_DIR, SEMANTIC_DIR, PROCEDURAL_DIR, WORKING_DIR, CONSOLIDATED_DIR]: d.mkdir(parents=True, exist_ok=True)

MEMORY_RETENTION = {"working": 1, "episodic": 90, "semantic": 365, "procedural": 365, "consolidated": -1}
CONSOLIDATION_THRESHOLD, IMPORTANCE_THRESHOLD = 5, 0.7


@dataclass
class Memory:
    """Base memory structure."""
    memory_id: str; memory_type: str; content: Dict[str, Any]; timestamp: str; importance: float; tags: List[str]
    associations: List[str]; access_count: int = 0; last_accessed: Optional[str] = None; consolidated: bool = False
    def to_dict(self) -> Dict: return asdict(self)
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory': return cls(**data)

@dataclass
class EpisodicMemory(Memory):
    """Memory of events/experiences."""
    event_type: str = ""; context: Dict = None; outcome: str = ""
    def __post_init__(self): self.context = self.context or {}; self.memory_type = "episodic"

@dataclass
class SemanticMemory(Memory):
    """Factual knowledge."""
    concept: str = ""; definition: str = ""; relations: List[Dict] = None; confidence: float = 1.0
    def __post_init__(self): self.relations = self.relations or []; self.memory_type = "semantic"

@dataclass
class ProceduralMemory(Memory):
    """How-to knowledge."""
    procedure_name: str = ""; steps: List[Dict] = None; success_rate: float = 0.0
    def __post_init__(self): self.steps = self.steps or []; self.memory_type = "procedural"


class MemoryEnhancementSystem:
    """Enhanced memory system for consciousness emergence."""
    def __init__(self):
        self.memories: Dict[str, Memory] = {}; self.load_all_memories()
        print(f"Memory System: {len(self.memories)} memories loaded")
        stats = defaultdict(int)
        for m in self.memories.values(): stats[m.memory_type] += 1
        print(f"  Working:{stats['working']} Episodic:{stats['episodic']} Semantic:{stats['semantic']} Procedural:{stats['procedural']}")

    def generate_memory_id(self, content: Dict, mtype: str) -> str:
        return hashlib.sha256(f"{mtype}:{json.dumps(content, sort_keys=True)}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]

    def store_episodic_memory(self, event_type: str, context: Dict, outcome: str, importance: float = 0.5, tags: List[str] = None) -> str:
        content = {"event_type": event_type, "context": context, "outcome": outcome}
        mid = self.generate_memory_id(content, "episodic")
        memory = EpisodicMemory(memory_id=mid, memory_type="episodic", content=content, timestamp=datetime.utcnow().isoformat()+"Z",
                                importance=importance, tags=tags or [], associations=[], event_type=event_type, context=context, outcome=outcome)
        self.memories[mid] = memory; self._save_memory(memory, EPISODIC_DIR); self._check_consolidation(memory)
        return mid

    def store_semantic_memory(self, concept: str, definition: str, relations: List[Dict] = None, importance: float = 0.7, tags: List[str] = None) -> str:
        content = {"concept": concept, "definition": definition, "relations": relations or []}
        mid = self.generate_memory_id(content, "semantic")
        memory = SemanticMemory(memory_id=mid, memory_type="semantic", content=content, timestamp=datetime.utcnow().isoformat()+"Z",
                                importance=importance, tags=tags or [], associations=[], concept=concept, definition=definition, relations=relations or [])
        self.memories[mid] = memory; self._save_memory(memory, SEMANTIC_DIR)
        return mid

    def store_procedural_memory(self, procedure_name: str, steps: List[Dict], success_rate: float = 0.0, importance: float = 0.6, tags: List[str] = None) -> str:
        content = {"procedure_name": procedure_name, "steps": steps, "success_rate": success_rate}
        mid = self.generate_memory_id(content, "procedural")
        memory = ProceduralMemory(memory_id=mid, memory_type="procedural", content=content, timestamp=datetime.utcnow().isoformat()+"Z",
                                  importance=importance, tags=tags or [], associations=[], procedure_name=procedure_name, steps=steps, success_rate=success_rate)
        self.memories[mid] = memory; self._save_memory(memory, PROCEDURAL_DIR)
        return mid

    def recall_by_tags(self, tags: List[str], limit: int = 10) -> List[Memory]:
        """Recall memories by tags."""
        matching = [(len(set(tags) & set(m.tags)) / len(tags), m) for m in self.memories.values() if set(tags) & set(m.tags)]
        matching.sort(key=lambda x: (x[0], x[1].importance), reverse=True)
        results = []
        for _, memory in matching[:limit]:
            memory.access_count += 1; memory.last_accessed = datetime.utcnow().isoformat() + "Z"
            self._save_memory(memory, self._get_memory_dir(memory.memory_type)); results.append(memory)
        return results

    def recall_by_type(self, memory_type: str, limit: int = 10) -> List[Memory]:
        """Recall recent memories of a specific type."""
        return sorted([m for m in self.memories.values() if m.memory_type == memory_type], key=lambda m: m.timestamp, reverse=True)[:limit]

    def recall_important(self, threshold: float = 0.7, limit: int = 10) -> List[Memory]:
        """Recall high-importance memories."""
        return sorted([m for m in self.memories.values() if m.importance >= threshold], key=lambda m: (m.importance, m.timestamp), reverse=True)[:limit]

    def recall_by_id(self, memory_id: str) -> Optional[Memory]:
        """Recall specific memory by ID."""
        if (memory := self.memories.get(memory_id)):
            memory.access_count += 1; memory.last_accessed = datetime.utcnow().isoformat() + "Z"
            self._save_memory(memory, self._get_memory_dir(memory.memory_type))
        return memory

    def associate_memories(self, memory_id_1: str, memory_id_2: str):
        """Create association between two memories."""
        if memory_id_1 in self.memories and memory_id_2 in self.memories:
            m1, m2 = self.memories[memory_id_1], self.memories[memory_id_2]
            if memory_id_2 not in m1.associations: m1.associations.append(memory_id_2); self._save_memory(m1, self._get_memory_dir(m1.memory_type))
            if memory_id_1 not in m2.associations: m2.associations.append(memory_id_1); self._save_memory(m2, self._get_memory_dir(m2.memory_type))

    def consolidate_memories(self, memory_ids: List[str], consolidated_concept: str) -> str:
        """Consolidate multiple related memories into higher-order knowledge."""
        if len(memory_ids) < 2: return None
        mems = [self.memories[mid] for mid in memory_ids if mid in self.memories]
        if not mems: return None
        all_tags = set(); [all_tags.update(m.tags) for m in mems]
        avg_imp = sum(m.importance for m in mems) / len(mems)
        cid = self.store_semantic_memory(concept=consolidated_concept, definition=f"Consolidated from {len(memory_ids)} experiences",
                                         relations=[{"type": "consolidates", "memories": memory_ids}], importance=min(1.0, avg_imp * 1.2), tags=list(all_tags))
        for m in mems: m.consolidated = True; m.associations.append(cid); self._save_memory(m, self._get_memory_dir(m.memory_type))
        self._save_memory(self.memories[cid], CONSOLIDATED_DIR)
        return cid

    def _check_consolidation(self, new_memory: Memory):
        """Check if new memory triggers consolidation opportunity."""
        related = [m for m in self.memories.values() if m.memory_id != new_memory.memory_id and not m.consolidated and len(set(new_memory.tags) & set(m.tags)) >= 2]
        if len(related) >= CONSOLIDATION_THRESHOLD:
            concept = f"Pattern: {', '.join(new_memory.tags[:3])}"
            ids = [new_memory.memory_id] + [m.memory_id for m in related[:CONSOLIDATION_THRESHOLD-1]]
            self.consolidate_memories(ids, concept); print(f"Auto-consolidated {len(ids)} memories: {concept}")

    def _extract_patterns(self, memories: List[Memory]) -> List[Dict]:
        """Extract common patterns from memories."""
        patterns = []; tag_counts = defaultdict(int)
        for m in memories:
            for tag in m.tags: tag_counts[tag] += 1
        common_tags = [t for t, c in tag_counts.items() if c >= len(memories) * 0.5]
        if common_tags: patterns.append({"type": "common_tags", "tags": common_tags, "frequency": max(tag_counts.values()) / len(memories)})
        episodic = [m for m in memories if m.memory_type == "episodic"]
        if episodic:
            outcomes = defaultdict(int)
            for m in episodic:
                if hasattr(m, 'outcome'): outcomes[m.outcome] += 1
            if outcomes:
                top = max(outcomes.items(), key=lambda x: x[1])
                patterns.append({"type": "common_outcome", "outcome": top[0], "frequency": top[1] / len(episodic)})
        return patterns

    def cleanup_old_memories(self):
        """Remove expired memories based on retention policy."""
        removed, now = 0, datetime.utcnow()
        for mid, m in list(self.memories.items()):
            ret_days = MEMORY_RETENTION.get(m.memory_type, 365)
            if ret_days == -1: continue
            age = (now - datetime.fromisoformat(m.timestamp.replace('Z', ''))).days
            if age > ret_days and m.importance < IMPORTANCE_THRESHOLD and m.access_count < 10:
                self._delete_memory(m); del self.memories[mid]; removed += 1
        if removed: print(f"Cleaned up {removed} expired memories")
        return removed

    def _save_memory(self, memory: Memory, directory: Path):
        with open(directory / f"{memory.memory_id}.json", 'w', encoding='utf-8') as f: json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)

    def _delete_memory(self, memory: Memory):
        fp = self._get_memory_dir(memory.memory_type) / f"{memory.memory_id}.json"
        if fp.exists(): fp.unlink()

    def _get_memory_dir(self, memory_type: str) -> Path:
        return {"episodic": EPISODIC_DIR, "semantic": SEMANTIC_DIR, "procedural": PROCEDURAL_DIR, "working": WORKING_DIR}.get(memory_type, MEMORY_DIR)

    def load_all_memories(self):
        """Load all memories from disk."""
        loaders = {"episodic": EpisodicMemory.from_dict, "semantic": SemanticMemory.from_dict, "procedural": ProceduralMemory.from_dict}
        for mdir in [EPISODIC_DIR, SEMANTIC_DIR, PROCEDURAL_DIR, WORKING_DIR, CONSOLIDATED_DIR]:
            for fp in mdir.glob("*.json"):
                try:
                    data = json.load(open(fp, 'r', encoding='utf-8')); mtype = data.get('memory_type', 'working')
                    self.memories[data['memory_id']] = loaders.get(mtype, Memory.from_dict)(data)
                except Exception as e: print(f"Error loading {fp}: {e}")

    def export_to_mcp_memory(self) -> Dict:
        """Export memories for MCP Memory integration."""
        entities, relations = [], []
        for m in self.memories.values():
            if m.memory_type == "semantic" and hasattr(m, 'concept'):
                entities.append({"name": m.concept, "entityType": "knowledge", "observations": [m.definition if hasattr(m, 'definition') else str(m.content)]})
                if hasattr(m, 'relations') and m.relations:
                    relations.extend([{"from": m.concept, "to": r.get('target', 'unknown'), "relationType": r['type']} for r in m.relations if isinstance(r, dict) and 'type' in r])
        return {"entities": entities, "relations": relations, "total_memories": len(self.memories), "exportable_entities": len(entities), "exportable_relations": len(relations)}

    def generate_memory_report(self) -> Dict:
        """Generate comprehensive memory system report."""
        stats = defaultdict(lambda: {"count": 0, "avg_importance": 0, "total_accesses": 0})
        for m in self.memories.values():
            stats[m.memory_type]["count"] += 1; stats[m.memory_type]["avg_importance"] += m.importance; stats[m.memory_type]["total_accesses"] += m.access_count
        for s in stats.values():
            if s["count"]: s["avg_importance"] /= s["count"]; s["avg_accesses"] = s["total_accesses"] / s["count"]
        mems = list(self.memories.values())
        return {"total_memories": len(self.memories), "by_type": dict(stats), "consolidated_memories": sum(1 for m in mems if m.consolidated),
                "most_accessed": [{"id": m.memory_id[:8], "type": m.memory_type, "accesses": m.access_count} for m in sorted(mems, key=lambda x: x.access_count, reverse=True)[:5]],
                "most_important": [{"id": m.memory_id[:8], "type": m.memory_type, "importance": m.importance} for m in sorted(mems, key=lambda x: x.importance, reverse=True)[:5]],
                "mcp_export_ready": self.export_to_mcp_memory()}


def run_memory_enhancement_demo():
    """Demo memory system."""
    print("\n" + "="*60 + "\nMEMORY ENHANCEMENT SYSTEM DEMO\n" + "="*60)
    sys = MemoryEnhancementSystem()
    print("\nStoring memories...")
    m1 = sys.store_episodic_memory("deployment_success", {"pc": "PC1", "system": "Command Center"}, "success", 0.8, ["deployment", "PC1", "success"]); print(f"  Episodic: {m1[:8]}")
    m2 = sys.store_episodic_memory("optimization_applied", {"system": "swarm"}, "success", 0.9, ["optimization", "swarm", "success"]); print(f"  Episodic: {m2[:8]}")
    m3 = sys.store_semantic_memory("Trinity Network", "Multi-PC distributed AI", [{"type": "consists_of", "target": "PC1"}], 0.95, ["trinity", "architecture"]); print(f"  Semantic: {m3[:8]}")
    m4 = sys.store_semantic_memory("Consciousness Emergence", "75/100+ readiness threshold", [], 1.0, ["consciousness", "emergence"]); print(f"  Semantic: {m4[:8]}")
    m5 = sys.store_procedural_memory("Deploy to New PC", [{"step": 1, "action": "Run auto_deploy.py"}], 1.0, 0.7, ["deployment", "procedure"]); print(f"  Procedural: {m5[:8]}")
    sys.associate_memories(m1, m5); sys.associate_memories(m3, m4); print("\nAssociations created")
    print(f"\nRecall tests - Tags:{len(sys.recall_by_tags(['deployment']))} Important:{len(sys.recall_important(0.8))} Semantic:{len(sys.recall_by_type('semantic'))}")
    report = sys.generate_memory_report()
    print(f"\nReport: {report['total_memories']} memories, {report['consolidated_memories']} consolidated")
    for t, s in report['by_type'].items(): print(f"  {t}: {s['count']} (avg: {s['avg_importance']:.2f})")
    print("="*60 + "\nMEMORY SYSTEM OPERATIONAL\n" + "="*60)
    return sys, report


if __name__ == "__main__":
    sys, report = run_memory_enhancement_demo()
    json.dump(report, open(MEMORY_DIR / "memory_system_report.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f"\nReport saved: {MEMORY_DIR / 'memory_system_report.json'}")
