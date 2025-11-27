#!/usr/bin/env python3
"""CAPABILITY_DIFF_ENGINE.py - Cross-PC Capability Analysis for Trinity."""

import json; import os; import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Config
PCS = ["PC1", "PC2", "PC3"]
BASE_DIR = Path(__file__).parent.parent.parent
MANIFESTS_DIR, REPORTS_DIR = BASE_DIR / ".trinity" / "capability_manifests", BASE_DIR / ".trinity" / "cyclotron" / "reports"
HUB_DIR = BASE_DIR / "LOCAL_TRINITY_HUB" / "cyclotron_reports"
for d in [MANIFESTS_DIR, REPORTS_DIR, HUB_DIR]: d.mkdir(parents=True, exist_ok=True)

class CapabilityDiff:
    """Capability differences across Trinity."""
    def __init__(self):
        self.manifests, self.software_matrix, self.mcp_matrix = {}, defaultdict(dict), defaultdict(dict)
        self.api_matrix, self.unique_capabilities, self.missing_capabilities = defaultdict(dict), defaultdict(list), defaultdict(list)
        self.sync_opportunities = []

def load_manifests() -> Dict[str, Dict]:
    """Load all available PC manifests."""
    manifests = {}
    for pc in PCS:
        mf = MANIFESTS_DIR / f"{pc}_MANIFEST.json"
        if mf.exists():
            try: manifests[pc] = json.load(open(mf)); print(f"Loaded: {pc}")
            except Exception as e: print(f"Failed {pc}: {e}")
        else: print(f"Not found: {pc}")
    return manifests

def build_software_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, str]]:
    """Build matrix of software across PCs."""
    matrix = defaultdict(dict)
    for pc, m in manifests.items():
        for sw in m.get("software_inventory", []): matrix[sw.get("name", "")][pc] = sw.get("version", "unknown")
    return dict(matrix)

def build_mcp_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, Any]]:
    """Build matrix of MCP tools across PCs."""
    matrix = defaultdict(dict)
    for pc, m in manifests.items():
        for tool in m.get("mcp_tools", []): matrix[tool.get("name", "")][pc] = tool
    return dict(matrix)

def build_api_matrix(manifests: Dict[str, Dict]) -> Dict[str, Dict[str, str]]:
    """Build matrix of API keys across PCs."""
    matrix = defaultdict(dict)
    for pc, m in manifests.items():
        for api in m.get("api_keys", []): matrix[api.get("service", "")][pc] = api.get("status", "unknown")
    return dict(matrix)

def find_unique_capabilities(manifests: Dict[str, Dict], matrix: Dict) -> Dict[str, List[str]]:
    """Find capabilities unique to each PC."""
    unique = defaultdict(list)
    for item, pcs in matrix.items():
        if len(pcs) == 1: unique[list(pcs.keys())[0]].append(item)
    return dict(unique)

def find_missing_capabilities(manifests: Dict[str, Dict], matrix: Dict) -> Dict[str, List[str]]:
    """Find capabilities missing on each PC."""
    missing = defaultdict(list); all_items = set(matrix.keys())
    for pc in manifests.keys(): missing[pc] = list(all_items - set(item for item, pcs in matrix.items() if pc in pcs))
    return dict(missing)

def find_sync_opportunities(manifests: Dict[str, Dict], software_matrix: Dict) -> List[tuple]:
    """Find high-value sync opportunities."""
    opportunities = []
    for sw in ["Python", "Node.js", "Git", "VSCode", "Claude Code"]:
        if sw in software_matrix:
            have, all_pcs = set(software_matrix[sw].keys()), set(manifests.keys())
            if missing := (all_pcs - have):
                if from_pc := (list(have)[0] if have else None): opportunities.append((sw, from_pc, list(missing), "critical"))
    return opportunities

def generate_text_report(diff: CapabilityDiff) -> str:
    """Generate human-readable text report."""
    r = ["=" * 80, "TRINITY CAPABILITY DIFF REPORT", "=" * 80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"PCs: {', '.join(diff.manifests.keys())}", ""]
    r += ["-" * 80, "SOFTWARE DISTRIBUTION", "-" * 80, "", f"Total: {len(diff.software_matrix)}", ""]
    on_all = [s for s, pcs in diff.software_matrix.items() if len(pcs) == len(diff.manifests)]
    r.append(f"On All ({len(on_all)}):"); r += [f"  {s}" for s in sorted(on_all)[:10]]; r += [f"  ...+{len(on_all)-10}" if len(on_all) > 10 else ""]
    r += ["", "Unique:"]; r += [f"  {pc}: {len(items)}" for pc, items in diff.unique_capabilities.items()]
    r += ["", "Missing:"]; r += [f"  {pc}: {len(items)}" for pc, items in diff.missing_capabilities.items()]
    r += ["", "-" * 80, "SYNC OPPORTUNITIES", "-" * 80, ""]
    if diff.sync_opportunities:
        for sw, from_pc, to_pcs, pri in diff.sync_opportunities: r.append(f"  [{pri.upper()}] {sw}: {from_pc} -> {', '.join(to_pcs)}")
    else: r.append("None")
    if diff.mcp_matrix: r += ["", "-" * 80, "MCP TOOLS", "-" * 80, ""]; r += [f"  {t}: {', '.join(p.keys())}" for t, p in diff.mcp_matrix.items()]
    if diff.api_matrix: r += ["", "-" * 80, "API KEYS", "-" * 80, ""]; r += [f"  {s}: {', '.join(f'{p}:{st}' for p, st in ps.items())}" for s, ps in diff.api_matrix.items()]
    r += ["", "=" * 80, "END OF REPORT", "=" * 80]
    return "\n".join(r)

def generate_json_report(diff: CapabilityDiff) -> Dict:
    """Generate machine-readable JSON report."""
    return {"generated_at": datetime.utcnow().isoformat() + "Z", "pcs_analyzed": list(diff.manifests.keys()),
            "summary": {"total_software": len(diff.software_matrix), "total_mcp_tools": len(diff.mcp_matrix),
                        "total_api_services": len(diff.api_matrix),
                        "unique_capabilities": {pc: len(i) for pc, i in diff.unique_capabilities.items()},
                        "missing_capabilities": {pc: len(i) for pc, i in diff.missing_capabilities.items()},
                        "sync_opportunities": len(diff.sync_opportunities)},
            "software_matrix": diff.software_matrix, "mcp_matrix": diff.mcp_matrix, "api_matrix": diff.api_matrix,
            "unique_capabilities": diff.unique_capabilities, "missing_capabilities": diff.missing_capabilities,
            "sync_opportunities": [{"software": sw, "from_pc": fp, "to_pcs": tp, "priority": pr} for sw, fp, tp, pr in diff.sync_opportunities]}

def generate_html_report(diff: CapabilityDiff) -> str:
    """Generate HTML report."""
    css = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:sans-serif;background:#1a1a2e;color:#fff;padding:20px}
.container{max-width:1400px;margin:0 auto}.header{text-align:center;margin-bottom:30px}.header h1{font-size:2em;color:#0f8}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-bottom:20px}
.stat{background:rgba(255,255,255,0.05);border-radius:10px;padding:15px;text-align:center;border:1px solid #0f83}
.stat-v{font-size:2em;font-weight:bold;color:#0f8}.section{background:rgba(255,255,255,0.05);border-radius:10px;padding:20px;margin-bottom:20px;border:1px solid #0f83}
.section h2{color:#0f8;margin-bottom:15px}.pc-list{display:flex;gap:15px;flex-wrap:wrap}.pc-card{flex:1;min-width:200px;background:rgba(255,255,255,0.03);padding:15px;border-radius:8px;border-left:3px solid #0f8}
.pc-card h3{color:#0ff;margin-bottom:10px}.badge{display:inline-block;padding:3px 8px;border-radius:10px;font-size:0.8em;font-weight:bold}
.badge-s{background:#0f8;color:#000}.badge-w{background:#fa0;color:#000}.badge-c{background:#f66;color:#fff}ul{list-style:none}li{padding:3px 0;padding-left:15px}li:before{content:"•";color:#0f8;position:absolute;margin-left:-15px}"""
    pc_cards = "".join(f'<div class="pc-card"><h3>{pc}</h3><div>Unique: <span class="badge badge-s">{len(diff.unique_capabilities.get(pc,[]))}</span></div><div>Missing: <span class="badge badge-w">{len(diff.missing_capabilities.get(pc,[]))}</span></div></div>' for pc in diff.manifests)
    sync_html = "".join(f'<div style="background:rgba(255,255,255,0.03);padding:10px;border-radius:8px;margin:5px 0;border-left:3px solid #fa0"><b>{sw}</b> <span class="badge badge-c">{pr.upper()}</span><br>From: {fp} → {", ".join(tp)}</div>' for sw, fp, tp, pr in diff.sync_opportunities) if diff.sync_opportunities else "<p>None</p>"
    unique_html = "".join(f'<div class="pc-card"><h3>{pc} ({len(items)})</h3><ul>{"".join(f"<li>{i}</li>" for i in sorted(items)[:10])}{f"<li>...+{len(items)-10}</li>" if len(items)>10 else ""}</ul></div>' for pc, items in diff.unique_capabilities.items())
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Trinity Diff</title><style>{css}</style></head><body><div class="container">
<div class="header"><h1>Trinity Capability Diff</h1><div>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | PCs: {', '.join(diff.manifests.keys())}</div></div>
<div class="stats"><div class="stat"><div class="stat-v">{len(diff.software_matrix)}</div>Software</div><div class="stat"><div class="stat-v">{len(diff.mcp_matrix)}</div>MCP Tools</div><div class="stat"><div class="stat-v">{len(diff.api_matrix)}</div>APIs</div><div class="stat"><div class="stat-v">{len(diff.sync_opportunities)}</div>Sync Ops</div></div>
<div class="section"><h2>Capability Distribution</h2><div class="pc-list">{pc_cards}</div></div>
<div class="section"><h2>Sync Opportunities</h2>{sync_html}</div>
<div class="section"><h2>Unique Capabilities</h2><div class="pc-list">{unique_html}</div></div>
</div></body></html>"""

def analyze_capabilities() -> CapabilityDiff:
    """Run full capability analysis."""
    print("\n" + "=" * 80 + "\nTRINITY CAPABILITY DIFF ENGINE\n" + "=" * 80 + "\n")
    print("Loading manifests...")
    manifests = load_manifests()
    if not manifests: print("No manifests found"); return None
    print(f"Loaded {len(manifests)} manifest(s)\n")
    diff = CapabilityDiff(); diff.manifests = manifests
    print("Building matrices...")
    diff.software_matrix = build_software_matrix(manifests)
    diff.mcp_matrix = build_mcp_matrix(manifests)
    diff.api_matrix = build_api_matrix(manifests)
    print(f"Software: {len(diff.software_matrix)} | MCP: {len(diff.mcp_matrix)} | API: {len(diff.api_matrix)}\n")
    print("Finding unique/missing...")
    diff.unique_capabilities = find_unique_capabilities(manifests, diff.software_matrix)
    diff.missing_capabilities = find_missing_capabilities(manifests, diff.software_matrix)
    for pc in manifests: print(f"  {pc}: {len(diff.unique_capabilities.get(pc,[]))} unique, {len(diff.missing_capabilities.get(pc,[]))} missing")
    print("\nFinding sync opportunities...")
    diff.sync_opportunities = find_sync_opportunities(manifests, diff.software_matrix)
    print(f"Found {len(diff.sync_opportunities)} sync opportunities\n")
    return diff

def save_reports(diff: CapabilityDiff):
    """Save all report formats."""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    for name, content, ext in [("Text", generate_text_report(diff), "txt"), ("JSON", json.dumps(generate_json_report(diff), indent=2), "json"), ("HTML", generate_html_report(diff), "html")]:
        with open(REPORTS_DIR / f"capability_diff_{ts}.{ext}", 'w') as f: f.write(content); print(f"{name}: {REPORTS_DIR / f'capability_diff_{ts}.{ext}'}")
    with open(HUB_DIR / "capability_diff_latest.json", 'w') as f: json.dump(generate_json_report(diff), f, indent=2)
    print(f"Hub: {HUB_DIR / 'capability_diff_latest.json'}")

def main():
    """Main entry point."""
    try:
        diff = analyze_capabilities()
        if diff:
            print("Generating reports..."); save_reports(diff)
            print("\n" + "=" * 80 + "\nANALYSIS COMPLETE!\n" + "=" * 80)
    except KeyboardInterrupt: print("\nInterrupted")
    except Exception as e: print(f"Failed: {e}"); import traceback; traceback.print_exc()

if __name__ == "__main__": main()
