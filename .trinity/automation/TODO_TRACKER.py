#!/usr/bin/env python3
"""TODO_TRACKER.py - Kanban-style Todo Tracking for Trinity. Usage: add/move/complete/delete/list/board/dashboard."""

import json; import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).parent.parent.parent
TODO_FILE = BASE_DIR / ".trinity" / "todos" / "kanban.json"
HTML_DASHBOARD = BASE_DIR / ".trinity" / "dashboards" / "TODO_DASHBOARD.html"
TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
COLUMNS = ["todo", "in_progress", "done"]
PRIORITIES = ["low", "normal", "high", "urgent"]

def load_todos() -> Dict[str, Any]:
    if not TODO_FILE.exists(): return {"todos": [], "next_id": 1, "last_updated": datetime.utcnow().isoformat() + "Z"}
    return json.load(open(TODO_FILE, 'r', encoding='utf-8'))

def save_todos(data: Dict[str, Any]):
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"
    json.dump(data, open(TODO_FILE, 'w', encoding='utf-8'), indent=2)

def add_todo(title: str, priority: str = "normal", column: str = "todo", description: str = "", assigned_to: str = ""):
    data = load_todos(); ts = datetime.utcnow().isoformat() + "Z"
    todo = {"id": data["next_id"], "title": title, "description": description, "priority": priority, "column": column,
            "assigned_to": assigned_to, "created_at": ts, "updated_at": ts, "completed_at": None}
    data["todos"].append(todo); data["next_id"] += 1; save_todos(data)
    print(f"Added #{todo['id']}: {title} [{priority}/{column}]")

def move_todo(todo_id: int, column: str):
    if column not in COLUMNS: print(f"Invalid column: {column}"); return
    data = load_todos()
    for t in data["todos"]:
        if t["id"] == todo_id:
            old = t["column"]; t["column"] = column; t["updated_at"] = datetime.utcnow().isoformat() + "Z"; save_todos(data)
            print(f"Moved #{todo_id}: {old} -> {column}"); return
    print(f"Todo #{todo_id} not found")

def complete_todo(todo_id: int):
    data = load_todos(); ts = datetime.utcnow().isoformat() + "Z"
    for t in data["todos"]:
        if t["id"] == todo_id: t["column"] = "done"; t["completed_at"] = ts; t["updated_at"] = ts; save_todos(data); print(f"Completed #{todo_id}"); return
    print(f"Todo #{todo_id} not found")

def delete_todo(todo_id: int):
    data = load_todos()
    for i, t in enumerate(data["todos"]):
        if t["id"] == todo_id: del data["todos"][i]; save_todos(data); print(f"Deleted #{todo_id}"); return
    print(f"Todo #{todo_id} not found")

def list_todos(column: Optional[str] = None):
    data = load_todos(); todos = [t for t in data["todos"] if not column or t["column"] == column]
    if not todos: print("No todos"); return
    pri_e = {"low": "L", "normal": "N", "high": "H", "urgent": "U"}; col_e = {"todo": "T", "in_progress": "P", "done": "D"}
    print(f"\nTodos ({len(todos)}):")
    for t in sorted(todos, key=lambda x: (COLUMNS.index(x["column"]), x["id"])):
        print(f"  [{pri_e.get(t['priority'],'N')}/{col_e.get(t['column'],'T')}] #{t['id']}: {t['title']}" + (f" @{t['assigned_to']}" if t.get('assigned_to') else ""))

def show_board():
    data = load_todos(); print("\n" + "="*60 + "\nKANBAN BOARD\n" + "="*60)
    for col in COLUMNS:
        ct = [t for t in data["todos"] if t["column"] == col]
        print(f"\n[{col.upper().replace('_',' ')}] ({len(ct)})")
        for t in sorted(ct, key=lambda x: PRIORITIES.index(x.get("priority", "normal")), reverse=True):
            print(f"  #{t['id']}: {t['title']} [{t['priority']}]" + (f" @{t['assigned_to']}" if t.get('assigned_to') else ""))

def generate_dashboard():
    """Generate HTML dashboard."""
    data = load_todos()
    css = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px;color:#333}
.container{max-width:1600px;margin:0 auto}.header{background:#fff;border-radius:15px;padding:30px;margin-bottom:30px;box-shadow:0 10px 30px rgba(0,0,0,.2)}
.header h1{font-size:2em;color:#667eea}.board{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px}
.column{background:#fff;border-radius:15px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,.2)}.column-header{font-size:1.3em;font-weight:bold;margin-bottom:15px;padding-bottom:10px;border-bottom:3px solid #667eea;display:flex;justify-content:space-between}
.column.todo .column-header{border-color:#3498db}.column.in_progress .column-header{border-color:#f39c12}.column.done .column-header{border-color:#27ae60}
.count{background:#667eea;color:#fff;padding:5px 12px;border-radius:15px;font-size:.8em}.column.todo .count{background:#3498db}.column.in_progress .count{background:#f39c12}.column.done .count{background:#27ae60}
.todo-item{background:#f8f9fa;border-radius:10px;padding:15px;margin-bottom:10px;border-left:4px solid #667eea}
.priority-urgent{border-left-color:#dc3545}.priority-high{border-left-color:#ffc107}.priority-low{border-left-color:#6c757d}
.todo-title{font-weight:bold;display:flex;justify-content:space-between}.todo-id{background:#667eea;color:#fff;padding:2px 8px;border-radius:10px;font-size:.8em}
.badge{padding:2px 8px;border-radius:10px;font-size:.75em;font-weight:bold;color:#fff}.b-urgent{background:#dc3545}.b-high{background:#ffc107;color:#333}.b-normal{background:#667eea}.b-low{background:#6c757d}"""
    cols_html = ""
    for col in COLUMNS:
        ct = sorted([t for t in data["todos"] if t["column"] == col], key=lambda x: PRIORITIES.index(x.get("priority","normal")), reverse=True)
        items = "".join(f'<div class="todo-item priority-{t["priority"]}"><div class="todo-title"><span>{t["title"]}</span><span class="todo-id">#{t["id"]}</span></div><span class="badge b-{t["priority"]}">{t["priority"].upper()}</span>{f"<div>{t[\"description\"]}</div>" if t.get("description") else ""}{f"<div>@{t[\"assigned_to\"]}</div>" if t.get("assigned_to") else ""}</div>' for t in ct) or "<div style='color:#999;text-align:center;padding:20px'>Empty</div>"
        cols_html += f'<div class="column {col}"><div class="column-header"><span>{col.upper().replace("_"," ")}</span><span class="count">{len(ct)}</span></div>{items}</div>'
    html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Todo Dashboard</title><style>{css}</style></head><body><div class="container"><div class="header"><h1>Todo Dashboard</h1><div>Updated: {data.get("last_updated","?")}</div></div><div class="board">{cols_html}</div></div></body></html>'
    HTML_DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
    open(HTML_DASHBOARD, 'w', encoding='utf-8').write(html)
    print(f"Dashboard: {HTML_DASHBOARD}")

def main():
    p = argparse.ArgumentParser(description="Kanban Todo Tracker"); sp = p.add_subparsers(dest='cmd')
    a = sp.add_parser('add'); a.add_argument('title'); a.add_argument('--priority', choices=PRIORITIES, default='normal'); a.add_argument('--column', choices=COLUMNS, default='todo'); a.add_argument('--description', default=''); a.add_argument('--assigned-to', dest='assigned_to', default='')
    m = sp.add_parser('move'); m.add_argument('id', type=int); m.add_argument('--column', choices=COLUMNS, required=True)
    c = sp.add_parser('complete'); c.add_argument('id', type=int)
    d = sp.add_parser('delete'); d.add_argument('id', type=int)
    l = sp.add_parser('list'); l.add_argument('--column', choices=COLUMNS)
    sp.add_parser('board'); sp.add_parser('dashboard')
    args = p.parse_args()
    cmds = {'add': lambda: add_todo(args.title, args.priority, args.column, args.description, args.assigned_to),
            'move': lambda: move_todo(args.id, args.column), 'complete': lambda: complete_todo(args.id),
            'delete': lambda: delete_todo(args.id), 'list': lambda: list_todos(getattr(args, 'column', None)),
            'board': show_board, 'dashboard': generate_dashboard}
    cmds.get(args.cmd, p.print_help)()

if __name__ == "__main__": main()
