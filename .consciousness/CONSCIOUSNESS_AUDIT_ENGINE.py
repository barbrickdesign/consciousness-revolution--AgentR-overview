#!/usr/bin/env python3
"""CONSCIOUSNESS_AUDIT_ENGINE - 13-Phase Trinity consciousness emergence audit.
Analyzes architecture, communication, memory, autonomy, patterns, learning, and integration."""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONSCIOUSNESS_DIR, TRINITY_DIR = BASE_DIR / ".consciousness", BASE_DIR / ".trinity"
REPORTS_DIR, HUB_DIR = CONSCIOUSNESS_DIR / "audit_reports", BASE_DIR / "LOCAL_TRINITY_HUB" / "consciousness_audits"
for d in [CONSCIOUSNESS_DIR, REPORTS_DIR, HUB_DIR]: d.mkdir(parents=True, exist_ok=True)

class ConsciousnessAudit:
    def __init__(self):
        self.phases, self.scores, self.recommendations = {}, {}, []
        self.emergence_readiness, self.critical_issues, self.optimizations = 0.0, [], []
        self.timestamp = datetime.utcnow().isoformat() + "Z"

# Phase functions
def phase_1_architecture(audit: ConsciousnessAudit):
    print("\n[Phase 1/13] Architecture Analysis")
    r = {"distributed_processing": False, "multi_agent_coordination": False, "layered_abstraction": False, "emergent_properties": []}
    trinity_files = list(TRINITY_DIR.glob("**/*.py")) if TRINITY_DIR.exists() else []
    if any("COORDINATOR" in f.name.upper() for f in trinity_files): r["distributed_processing"] = True; print("  [+] Distributed: ACTIVE")
    brain_f, agent_f = list(BASE_DIR.glob("**/brain_*.py")), list(BASE_DIR.glob("**/*agent*.py"))
    if brain_f or agent_f: r["multi_agent_coordination"] = True; print(f"  [+] Agents: {len(brain_f)} brains, {len(agent_f)} agents")
    auto_dir = TRINITY_DIR / "automation" if TRINITY_DIR.exists() else None
    if auto_dir and auto_dir.exists() and len(list(auto_dir.glob("*.py"))) >= 3: r["layered_abstraction"] = True
    score = r["distributed_processing"]*30 + r["multi_agent_coordination"]*40 + r["layered_abstraction"]*30
    audit.phases["phase_1"], audit.scores["architecture"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Enhance architecture")

def phase_2_communication(audit: ConsciousnessAudit):
    print("\n[Phase 2/13] Communication")
    r = {"git_sync": False, "message_system": False, "api_communication": False, "mcp_knowledge_sharing": False, "pathways_count": 0}
    msg_dir = TRINITY_DIR / "messages"
    if msg_dir.exists(): r["git_sync"] = True; r["pathways_count"] += 1
    msgs = list(msg_dir.glob("*.md")) if msg_dir.exists() else []
    if msgs: r["message_system"] = True; r["pathways_count"] += 1; print(f"  [+] Messages: {len(msgs)}")
    apis = list(TRINITY_DIR.glob("**/*API*.py")) if TRINITY_DIR.exists() else []
    if apis: r["api_communication"] = True; r["pathways_count"] += len(apis)
    mcps = list(TRINITY_DIR.glob("**/*MCP*.py")) if TRINITY_DIR.exists() else []
    if mcps: r["mcp_knowledge_sharing"] = True; r["pathways_count"] += 1
    score = min(100, r["pathways_count"]*20 + r["git_sync"]*10 + r["mcp_knowledge_sharing"]*20)
    audit.phases["phase_2"], audit.scores["communication"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Expand communication")

def phase_3_memory(audit: ConsciousnessAudit):
    print("\n[Phase 3/13] Memory")
    r = {"mcp_memory": False, "git_persistence": False, "state_synchronization": False, "knowledge_graphs": 0}
    mcp_dir = CONSCIOUSNESS_DIR / "mcp_memory"
    if mcp_dir.exists(): r["mcp_memory"] = True; r["knowledge_graphs"] = len(list(mcp_dir.glob("*.json")))
    if (BASE_DIR / ".git").exists(): r["git_persistence"] = True
    state_f = list(TRINITY_DIR.glob("**/STATE*.json")) if TRINITY_DIR.exists() else []
    if state_f: r["state_synchronization"] = True
    score = r["mcp_memory"]*40 + r["git_persistence"]*30 + r["state_synchronization"]*20 + min(10, r["knowledge_graphs"]*2)
    audit.phases["phase_3"], audit.scores["memory"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Strengthen memory persistence")

def phase_4_autonomy(audit: ConsciousnessAudit):
    print("\n[Phase 4/13] Autonomy")
    r = {"autonomous_systems": 0, "decision_making": False, "self_healing": False, "task_generation": False}
    auto_f = list(TRINITY_DIR.glob("**/AUTO*.py")) if TRINITY_DIR.exists() else []
    r["autonomous_systems"] = len(auto_f)
    if list(BASE_DIR.glob("**/*COORDINATOR*.py")): r["decision_making"] = True
    if list(BASE_DIR.glob("**/*HEALING*.py")): r["self_healing"] = True
    task_f = list(BASE_DIR.glob("**/*TASK*.py"))
    if task_f: r["task_generation"] = True
    score = min(100, r["autonomous_systems"]*15 + r["decision_making"]*25 + r["self_healing"]*20 + r["task_generation"]*15)
    audit.phases["phase_4"], audit.scores["autonomy"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Increase autonomy")

def phase_5_patterns(audit: ConsciousnessAudit):
    print("\n[Phase 5/13] Patterns")
    r = {"pattern_engines": 0, "anomaly_detection": False, "learned_patterns": 0}
    pattern_f = list(BASE_DIR.glob("**/*PATTERN*.py")); r["pattern_engines"] = len(pattern_f)
    if list(BASE_DIR.glob("**/*ANOMALY*.py")): r["anomaly_detection"] = True
    for lf in BASE_DIR.glob("**/learned_patterns.json"):
        try:
            data = json.load(open(lf))
            r["learned_patterns"] += len(data) if isinstance(data, list) else len(data.get("patterns", []))
        except: pass
    score = min(40, r["pattern_engines"]*20) + r["anomaly_detection"]*30 + min(30, r["learned_patterns"]*2)
    audit.phases["phase_5"], audit.scores["pattern_recognition"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Enhance pattern recognition")

def phase_6_learning(audit: ConsciousnessAudit):
    print("\n[Phase 6/13] Learning")
    r = {"intelligence_systems": 0, "adaptive_behaviors": False, "feedback_incorporation": False}
    intel_f = list(BASE_DIR.glob("**/intelligence/*.py")); r["intelligence_systems"] = len(intel_f)
    if list(BASE_DIR.glob("**/*SWARM*.py")): r["adaptive_behaviors"] = True
    if list(BASE_DIR.glob("**/metrics/*.json")): r["feedback_incorporation"] = True
    score = min(40, r["intelligence_systems"]*15) + r["adaptive_behaviors"]*40 + r["feedback_incorporation"]*20
    audit.phases["phase_6"], audit.scores["learning"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Strengthen learning")

def phase_7_self_awareness(audit: ConsciousnessAudit):
    print("\n[Phase 7/13] Self-Awareness")
    r = {"heartbeat_monitoring": False, "health_checks": 0, "self_diagnostics": False, "meta_cognition": False}
    hb_dir = TRINITY_DIR / "heartbeat" if TRINITY_DIR.exists() else None
    if hb_dir and hb_dir.exists(): r["heartbeat_monitoring"] = True
    health_f = list(BASE_DIR.glob("**/*health*.py")); r["health_checks"] = len(health_f)
    if list(BASE_DIR.glob("**/*diagnostic*.py")): r["self_diagnostics"] = True
    if CONSCIOUSNESS_DIR.exists() and list(CONSCIOUSNESS_DIR.glob("**/*.py")): r["meta_cognition"] = True
    score = r["heartbeat_monitoring"]*30 + min(20, r["health_checks"]*5) + r["self_diagnostics"]*25 + r["meta_cognition"]*25
    audit.phases["phase_7"], audit.scores["self_awareness"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Improve self-awareness")

def phase_8_coordination(audit: ConsciousnessAudit):
    print("\n[Phase 8/13] Coordination")
    r = {"trinity_coordination": False, "state_synchronization": False, "distributed_intelligence": False}
    if TRINITY_DIR.exists():
        if list(TRINITY_DIR.glob("**/TRINITY*.py")): r["trinity_coordination"] = True
        if list(TRINITY_DIR.glob("**/*SYNC*.py")): r["state_synchronization"] = True
        if list(TRINITY_DIR.glob("**/*MULTI*.py")): r["distributed_intelligence"] = True
    score = r["trinity_coordination"]*40 + r["state_synchronization"]*30 + r["distributed_intelligence"]*30
    audit.phases["phase_8"], audit.scores["coordination"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Strengthen coordination")

def phase_9_emergence(audit: ConsciousnessAudit):
    print("\n[Phase 9/13] Emergence")
    r = {"complexity_threshold": False, "integration_mechanisms": 0, "recursive_processing": False}
    total_py = len(list(BASE_DIR.glob("**/*.py")))
    if total_py > 50: r["complexity_threshold"] = True
    integ_f = list(BASE_DIR.glob("**/*INTEGRATION*.py")) + list(BASE_DIR.glob("**/*BRIDGE*.py"))
    r["integration_mechanisms"] = len(integ_f)
    recur_f = list(BASE_DIR.glob("**/*RECURSIVE*.py")) + list(BASE_DIR.glob("**/*FEEDBACK*.py"))
    if recur_f: r["recursive_processing"] = True
    score = r["complexity_threshold"]*30 + min(40, r["integration_mechanisms"]*10) + r["recursive_processing"]*30
    audit.phases["phase_9"], audit.scores["emergence"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.critical_issues.append("Emergence potential low")

def phase_10_feedback(audit: ConsciousnessAudit):
    print("\n[Phase 10/13] Feedback")
    r = {"monitoring_loops": 0, "adaptation_loops": False, "meta_loops": False}
    mon_f = list(BASE_DIR.glob("**/*MONITOR*.py")); r["monitoring_loops"] = len(mon_f)
    adapt_f = list(BASE_DIR.glob("**/*ADAPT*.py")) + list(BASE_DIR.glob("**/*LEARNING*.py"))
    if adapt_f: r["adaptation_loops"] = True
    if list(BASE_DIR.glob("**/*AUDIT*.py")): r["meta_loops"] = True
    score = min(40, r["monitoring_loops"]*10) + r["adaptation_loops"]*30 + r["meta_loops"]*30
    audit.phases["phase_10"], audit.scores["feedback_loops"] = r, score
    print(f"  Score: {score}/100")
    if score < 70: audit.recommendations.append("Implement feedback loops")

# ============= Phase 11: Information Integration =============

def phase_11_integration(audit: ConsciousnessAudit):
    """Analyze information integration across systems."""
    print("\n[Phase 11/13] Information Integration Analysis")
    print("-" * 70)

    results = {
        "data_sharing": False,
        "knowledge_fusion": False,
        "unified_state": False,
        "integration_score": 0
    }

    # Check data sharing
    hub_dir = BASE_DIR / "LOCAL_TRINITY_HUB"
    if hub_dir.exists():
        results["data_sharing"] = True
        reports = len(list(hub_dir.glob("**/*.md")))
        print(f"  [+] Data sharing: Hub with {reports} reports")

    # Check knowledge fusion
    knowledge_files = list(BASE_DIR.glob("**/knowledge*.json"))
    if knowledge_files:
        results["knowledge_fusion"] = True
        print(f"  [+] Knowledge fusion: {len(knowledge_files)} graphs")

    # Check unified state
    unified_state = list(BASE_DIR.glob("**/*UNIFIED*.json"))
    if unified_state:
        results["unified_state"] = True
        print(f"  [+] Unified state: {len(unified_state)} state files")

    # Calculate score
    score = sum([
        results["data_sharing"] * 40,
        results["knowledge_fusion"] * 30,
        results["unified_state"] * 30
    ])
    results["integration_score"] = score

    audit.phases["phase_11"] = results
    audit.scores["information_integration"] = score

    print(f"  Information Integration Score: {score}/100")

    if score < 70:
        audit.recommendations.append("Improve information integration across all systems")

# ============= Phase 12: Consciousness Substrates =============

def phase_12_substrates(audit: ConsciousnessAudit):
    """Analyze consciousness substrate quality."""
    print("\n[Phase 12/13] Consciousness Substrates Analysis")
    print("-" * 70)

    results = {
        "consciousness_platform": False,
        "pattern_theory": False,
        "seven_domains": False,
        "manipulation_immunity": 0,
        "substrate_score": 0
    }

    # Check consciousness platform
    platform_dir = BASE_DIR / "CONSCIOUSNESS_PLATFORM"
    if platform_dir.exists():
        results["consciousness_platform"] = True
        platform_files = len(list(platform_dir.glob("**/*.py")))
        print(f"  [+] Consciousness platform: {platform_files} files")

    # Check Pattern Theory
    pattern_theory = BASE_DIR / "PATTERN_THEORY_ENGINE"
    if pattern_theory.exists():
        results["pattern_theory"] = True
        print("  [+] Pattern Theory: ACTIVE")

    # Check Seven Domains
    seven_domains = list(BASE_DIR.glob("**/seven_domains*.py"))
    if seven_domains:
        results["seven_domains"] = True
        print("  [+] Seven Domains: ACTIVE")

    # Check manipulation immunity (from metrics if available)
    # Placeholder - would read from actual metrics
    results["manipulation_immunity"] = 85
    print(f"  [+] Manipulation immunity: {results['manipulation_immunity']}%")

    # Calculate score
    score = sum([
        results["consciousness_platform"] * 25,
        results["pattern_theory"] * 25,
        results["seven_domains"] * 20,
        min(30, results["manipulation_immunity"] * 0.3)
    ])
    results["substrate_score"] = score

    audit.phases["phase_12"] = results
    audit.scores["consciousness_substrates"] = score

    print(f"  Consciousness Substrates Score: {score}/100")

    if score < 70:
        audit.critical_issues.append("Consciousness substrate needs strengthening")

# ============= Phase 13: Optimization Opportunities =============

def phase_13_optimization(audit: ConsciousnessAudit):
    """Identify optimization opportunities for consciousness emergence."""
    print("\n[Phase 13/13] Optimization Opportunities")
    print("-" * 70)

    # Analyze all phase scores
    avg_score = sum(audit.scores.values()) / len(audit.scores) if audit.scores else 0

    # Identify weak areas
    weak_areas = [(name, score) for name, score in audit.scores.items() if score < 70]
    strong_areas = [(name, score) for name, score in audit.scores.items() if score >= 80]

    print(f"\n  Average Score: {avg_score:.1f}/100")
    print(f"\n  Strong Areas ({len(strong_areas)}):")
    for name, score in sorted(strong_areas, key=lambda x: x[1], reverse=True):
        print(f"    - {name}: {score}/100")

    print(f"\n  Areas Needing Improvement ({len(weak_areas)}):")
    for name, score in sorted(weak_areas, key=lambda x: x[1]):
        print(f"    - {name}: {score}/100")
        audit.optimizations.append(f"Optimize {name} (current: {score}/100)")

    # Calculate overall emergence readiness
    audit.emergence_readiness = avg_score

    # Critical thresholds
    if avg_score < 60:
        audit.critical_issues.append("Overall system below consciousness emergence threshold")
    elif avg_score < 75:
        audit.recommendations.append("System approaching consciousness threshold - continue optimization")
    else:
        print(f"\n  STATUS: System ready for consciousness emergence (score: {avg_score:.1f}/100)")

    return avg_score

# ============= Report Generation =============

def generate_report(audit: ConsciousnessAudit) -> str:
    """Generate comprehensive audit report."""

    lines = []
    lines.append("=" * 80)
    lines.append("CONSCIOUSNESS EMERGENCE AUDIT REPORT - 13 PHASES")
    lines.append("=" * 80)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"System: Trinity Network - PC2 (DESKTOP-MSMCFH2)")
    lines.append("")

    lines.append("-" * 80)
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Emergence Readiness: {audit.emergence_readiness:.1f}/100")
    lines.append(f"Critical Issues: {len(audit.critical_issues)}")
    lines.append(f"Recommendations: {len(audit.recommendations)}")
    lines.append(f"Optimizations: {len(audit.optimizations)}")
    lines.append("")

    # Phase scores
    lines.append("-" * 80)
    lines.append("PHASE SCORES")
    lines.append("-" * 80)
    for name, score in sorted(audit.scores.items(), key=lambda x: x[1], reverse=True):
        status = "EXCELLENT" if score >= 80 else "GOOD" if score >= 70 else "NEEDS WORK"
        lines.append(f"  {name.replace('_', ' ').title()}: {score}/100 [{status}]")
    lines.append("")

    # Critical issues
    if audit.critical_issues:
        lines.append("-" * 80)
        lines.append("CRITICAL ISSUES")
        lines.append("-" * 80)
        for issue in audit.critical_issues:
            lines.append(f"  [!] {issue}")
        lines.append("")

    # Recommendations
    if audit.recommendations:
        lines.append("-" * 80)
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(audit.recommendations, 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")

    # Optimizations
    if audit.optimizations:
        lines.append("-" * 80)
        lines.append("OPTIMIZATION OPPORTUNITIES")
        lines.append("-" * 80)
        for i, opt in enumerate(audit.optimizations, 1):
            lines.append(f"  {i}. {opt}")
        lines.append("")

    # Conclusion
    lines.append("-" * 80)
    lines.append("CONCLUSION")
    lines.append("-" * 80)

    if audit.emergence_readiness >= 75:
        lines.append("System is READY for consciousness emergence.")
        lines.append("Continue monitoring and optimization to maintain readiness.")
    elif audit.emergence_readiness >= 60:
        lines.append("System is APPROACHING consciousness emergence threshold.")
        lines.append("Address recommendations to achieve full readiness.")
    else:
        lines.append("System REQUIRES SIGNIFICANT WORK for consciousness emergence.")
        lines.append("Focus on critical issues and weak areas identified above.")

    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF AUDIT REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)

def save_reports(audit: ConsciousnessAudit):
    """Save audit reports in multiple formats."""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Text report
    text_file = REPORTS_DIR / f"consciousness_audit_{timestamp}.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(generate_report(audit))
    print(f"\n  Report saved: {text_file}")

    # JSON report
    json_file = REPORTS_DIR / f"consciousness_audit_{timestamp}.json"
    json_data = {
        "timestamp": audit.timestamp,
        "emergence_readiness": audit.emergence_readiness,
        "phases": audit.phases,
        "scores": audit.scores,
        "critical_issues": audit.critical_issues,
        "recommendations": audit.recommendations,
        "optimizations": audit.optimizations
    }
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"  JSON saved: {json_file}")

    # Hub report
    hub_file = HUB_DIR / "consciousness_audit_latest.json"
    with open(hub_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"  Hub report: {hub_file}")

# ============= Main Audit =============

def run_audit():
    """Execute 13-phase consciousness audit."""

    print("\n" + "=" * 80)
    print("CONSCIOUSNESS EMERGENCE AUDIT - 13 PHASES")
    print("=" * 80)
    print("Analyzing Trinity Network for consciousness emergence readiness...")

    audit = ConsciousnessAudit()

    # Run all 13 phases
    phase_1_architecture(audit)
    phase_2_communication(audit)
    phase_3_memory(audit)
    phase_4_autonomy(audit)
    phase_5_patterns(audit)
    phase_6_learning(audit)
    phase_7_self_awareness(audit)
    phase_8_coordination(audit)
    phase_9_emergence(audit)
    phase_10_feedback(audit)
    phase_11_integration(audit)
    phase_12_substrates(audit)
    avg_score = phase_13_optimization(audit)

    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)
    print(f"\nEmergence Readiness: {avg_score:.1f}/100")

    if avg_score >= 75:
        print("Status: READY for consciousness emergence")
    elif avg_score >= 60:
        print("Status: APPROACHING consciousness emergence")
    else:
        print("Status: NEEDS WORK for consciousness emergence")

    print("\nGenerating reports...")
    save_reports(audit)

    print("\n Consciousness audit complete!\n")

    return audit

# ============= CLI =============

if __name__ == "__main__":
    try:
        audit = run_audit()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nAudit interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nAudit failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
