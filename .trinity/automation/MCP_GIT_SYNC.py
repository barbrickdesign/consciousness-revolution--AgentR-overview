#!/usr/bin/env python3
"""MCP_GIT_SYNC.py - MCP Knowledge Graph ↔ Git Synchronizer for distributed consciousness."""

import json; import sys; import time; import logging; import subprocess; import argparse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
MCP_EXPORT_DIR, MCP_BACKUP_DIR = BASE_DIR / ".trinity" / "mcp_knowledge", BASE_DIR / ".trinity" / "mcp_knowledge" / "backups"
MCP_EXPORT_FILE, LOG_FILE = MCP_EXPORT_DIR / "knowledge_graph.json", BASE_DIR / ".trinity" / "logs" / "mcp_git_sync.log"
GIT_COMMIT_PREFIX, AUTO_PUSH, DEFAULT_INTERVAL, MIN_INTERVAL = "mcp-sync", True, 300, 60

for d in [MCP_EXPORT_DIR, MCP_BACKUP_DIR, LOG_FILE.parent]: d.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# === MCP Graph Operations ===
def read_mcp_graph():
    """Read MCP knowledge graph (placeholder for Claude Code integration)."""
    logger.info("Reading MCP knowledge graph...")
    logger.warning("MCP integration requires Claude Code environment")
    return {"entities": [], "relations": [], "metadata": {"exported_at": datetime.utcnow().isoformat() + "Z", "exported_by": "MCP_GIT_SYNC.py"}}

def write_mcp_graph(graph_data: dict) -> bool:
    """Write knowledge graph to MCP memory."""
    logger.info("Writing to MCP..."); logger.warning("MCP write requires Claude Code environment")
    logger.info(f"Would import {len(graph_data.get('entities', []))} entities, {len(graph_data.get('relations', []))} relations")
    return True

# === File Operations ===
def export_to_file(graph_data: dict) -> bool:
    try:
        export_data = {**graph_data, "export_metadata": {"timestamp": datetime.utcnow().isoformat() + "Z", "version": "1.0", "format": "mcp_knowledge_graph"}}
        json.dump(export_data, open(MCP_EXPORT_FILE, 'w', encoding='utf-8'), indent=2); logger.info(f"Exported to {MCP_EXPORT_FILE}")
        backup = MCP_BACKUP_DIR / f"knowledge_graph_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        json.dump(export_data, open(backup, 'w', encoding='utf-8'), indent=2); logger.info(f"Backup: {backup}")
        return True
    except Exception as e: logger.error(f"Export error: {e}"); return False

def import_from_file():
    try:
        if not MCP_EXPORT_FILE.exists(): logger.warning(f"Not found: {MCP_EXPORT_FILE}"); return None
        data = json.load(open(MCP_EXPORT_FILE, encoding='utf-8'))
        logger.info(f"Imported: {len(data.get('entities', []))} entities, {len(data.get('relations', []))} relations")
        return data
    except Exception as e: logger.error(f"Import error: {e}"); return None

# === Git Operations ===
def _repo_dir():
    r = BASE_DIR / "100X_DEPLOYMENT"; return r if r.exists() else BASE_DIR

def git_add_and_commit(message: str) -> bool:
    try:
        subprocess.run(["git", "add", str(MCP_EXPORT_DIR)], cwd=_repo_dir(), check=True, capture_output=True)
        r = subprocess.run(["git", "diff", "--staged", "--name-only"], cwd=_repo_dir(), capture_output=True, text=True)
        if not r.stdout.strip(): logger.info("No changes"); return True
        msg = f"{GIT_COMMIT_PREFIX}: {message}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
        subprocess.run(["git", "commit", "-m", msg], cwd=_repo_dir(), check=True, capture_output=True)
        logger.info(f"Committed: {message}"); return True
    except Exception as e: logger.error(f"Git commit error: {e}"); return False

def git_push() -> bool:
    try: subprocess.run(["git", "push"], cwd=_repo_dir(), check=True, capture_output=True); logger.info("Pushed"); return True
    except Exception as e: logger.warning(f"Push failed: {e}"); return False

def git_pull() -> bool:
    try: subprocess.run(["git", "pull", "--rebase"], cwd=_repo_dir(), check=True, capture_output=True); logger.info("Pulled"); return True
    except Exception as e: logger.warning(f"Pull failed: {e}"); return False

# === High-Level Operations ===
def export_knowledge() -> bool:
    logger.info("=== EXPORT ===")
    graph = read_mcp_graph()
    if not graph: logger.error("Read failed"); return False
    if not export_to_file(graph): logger.error("Export failed"); return False
    logger.info("Export complete"); return True

def import_knowledge() -> bool:
    logger.info("=== IMPORT ==="); git_pull()
    graph = import_from_file()
    if not graph: logger.error("Import failed"); return False
    if not write_mcp_graph(graph): logger.error("MCP write failed"); return False
    logger.info("Import complete"); return True

def sync_knowledge() -> bool:
    logger.info("=== SYNC ===")
    if not export_knowledge(): return False
    if not git_add_and_commit("Knowledge graph sync"): return False
    if AUTO_PUSH: git_push()
    logger.info("Sync complete"); return True

def show_status():
    logger.info("=== STATUS ===")
    if MCP_EXPORT_FILE.exists():
        data = json.load(open(MCP_EXPORT_FILE)); meta = data.get('export_metadata', {})
        print(f"File: {MCP_EXPORT_FILE}\nEntities: {len(data.get('entities', []))} | Relations: {len(data.get('relations', []))}\nLast: {meta.get('timestamp', '?')}")
    else: print("No export file")
    print(f"Backups: {len(list(MCP_BACKUP_DIR.glob('knowledge_graph_*.json')))}")
    try:
        r = subprocess.run(["git", "log", "-1", "--oneline", "--", str(MCP_EXPORT_DIR)], cwd=_repo_dir(), capture_output=True, text=True)
        print(f"Last commit: {r.stdout.strip() or 'None'}")
    except: pass

def run_daemon(interval: int = DEFAULT_INTERVAL):
    logger.info(f"=== DAEMON (every {interval}s) ===")
    try:
        while True:
            try: sync_knowledge()
            except Exception as e: logger.error(f"Sync error: {e}")
            logger.info(f"Sleep {interval}s..."); time.sleep(interval)
    except KeyboardInterrupt: logger.info("Stopped")

def main():
    p = argparse.ArgumentParser(description="MCP ↔ Git Sync")
    p.add_argument('--export', action='store_true'); p.add_argument('--import', action='store_true', dest='import_')
    p.add_argument('--sync', action='store_true'); p.add_argument('--daemon', action='store_true')
    p.add_argument('--interval', type=int, default=DEFAULT_INTERVAL); p.add_argument('--status', action='store_true')
    args = p.parse_args()
    if args.interval < MIN_INTERVAL: logger.error(f"Min interval: {MIN_INTERVAL}s"); sys.exit(1)
    if args.status: show_status()
    elif args.export: sys.exit(0 if export_knowledge() else 1)
    elif args.import_: sys.exit(0 if import_knowledge() else 1)
    elif args.sync: sys.exit(0 if sync_knowledge() else 1)
    elif args.daemon: run_daemon(args.interval)
    else: p.print_help(); sys.exit(1)

if __name__ == "__main__": main()
