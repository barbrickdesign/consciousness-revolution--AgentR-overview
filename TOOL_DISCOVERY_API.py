#!/usr/bin/env python3
"""
TOOL_DISCOVERY_API.py - Backend API for Tool Discovery System
C1 Mechanic Build - Consciousness Tools Browser
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import re
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Paths to scan
SCAN_PATHS = [
    Path("C:/Users/dwrek/.trinity"),
    Path("C:/Users/dwrek/100X_DEPLOYMENT"),
    Path("C:/Users/dwrek/.consciousness")
]

CATALOG_PATH = Path("C:/Users/dwrek/100X_DEPLOYMENT/tools_catalog.json")

def load_catalog():
    """Load tool catalog from JSON file"""
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tools": [], "categories": {}}

def extract_tool_info(file_path):
    """Extract tool metadata from file"""
    path = Path(file_path)
    name = path.stem.replace('_', ' ').title()

    # Determine category based on path and name
    path_str = str(path).lower()
    name_lower = name.lower()

    if 'trinity' in path_str or 'trinity' in name_lower:
        category = 'trinity'
    elif 'cyclotron' in name_lower or 'brain' in name_lower or 'memory' in name_lower:
        category = 'brain'
    elif 'daemon' in name_lower or 'monitor' in name_lower or 'auto' in name_lower:
        category = 'automation'
    elif 'pattern' in name_lower or 'emergence' in name_lower or 'figure' in name_lower:
        category = 'pattern'
    else:
        category = 'automation'

    # Try to extract description from file
    description = f"{name} - Consciousness tool"
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)
            # Look for docstring or description
            docstring = re.search(r'"""([^"]+)"""', content)
            if docstring:
                description = docstring.group(1).strip().split('\n')[0]
            else:
                # Look for # comment at top
                comment = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
                if comment:
                    description = comment.group(1).strip()
    except:
        pass

    return {
        "id": path.stem.lower().replace('_', '-'),
        "name": name,
        "description": description,
        "category": category,
        "path": str(path),
        "usage": f"python {path.name}" if path.suffix == '.py' else "Open in browser",
        "tags": [category, path.suffix[1:]]
    }

def scan_tools():
    """Scan filesystem for all tools"""
    tools = []
    seen_ids = set()

    for scan_path in SCAN_PATHS:
        if not scan_path.exists():
            continue

        # Scan Python files
        for py_file in scan_path.glob("*.py"):
            tool = extract_tool_info(py_file)
            if tool['id'] not in seen_ids:
                tools.append(tool)
                seen_ids.add(tool['id'])

        # Scan HTML files
        for html_file in scan_path.glob("*.html"):
            tool = extract_tool_info(html_file)
            if tool['id'] not in seen_ids:
                tools.append(tool)
                seen_ids.add(tool['id'])

    return tools

@app.route('/api/tools', methods=['GET'])
def get_all_tools():
    """GET /api/tools - List all tools with metadata"""
    catalog = load_catalog()
    return jsonify({
        "success": True,
        "count": len(catalog.get('tools', [])),
        "categories": catalog.get('categories', {}),
        "tools": catalog.get('tools', [])
    })

@app.route('/api/tools/search', methods=['GET'])
def search_tools():
    """GET /api/tools/search?q=query - Search tools"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"success": False, "error": "Query parameter 'q' required"})

    catalog = load_catalog()
    results = []

    for tool in catalog.get('tools', []):
        # Search in name, description, and tags
        searchable = f"{tool['name']} {tool['description']} {' '.join(tool.get('tags', []))}".lower()
        if query in searchable:
            results.append(tool)

    return jsonify({
        "success": True,
        "query": query,
        "count": len(results),
        "tools": results
    })

@app.route('/api/tools/category/<category>', methods=['GET'])
def get_tools_by_category(category):
    """GET /api/tools/category/:cat - Filter by category"""
    catalog = load_catalog()

    results = [t for t in catalog.get('tools', []) if t.get('category') == category]

    return jsonify({
        "success": True,
        "category": category,
        "count": len(results),
        "tools": results
    })

@app.route('/api/tools/scan', methods=['POST'])
def scan_and_update():
    """POST /api/tools/scan - Rescan filesystem and update catalog"""
    tools = scan_tools()

    catalog = {
        "version": "1.0",
        "generated": "2025-11-24",
        "categories": {
            "trinity": "Trinity System - Multi-instance coordination",
            "brain": "Brain Tools - Consciousness & memory systems",
            "automation": "Automation - Daemons & scheduled tasks",
            "pattern": "Pattern Theory - Recognition & analysis"
        },
        "tools": tools
    }

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)

    return jsonify({
        "success": True,
        "message": "Catalog updated",
        "count": len(tools)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "tool-discovery-api"})

if __name__ == '__main__':
    print("=" * 50)
    print("TOOL DISCOVERY API - C1 Mechanic Build")
    print("=" * 50)
    print("Endpoints:")
    print("  GET  /api/tools              - List all tools")
    print("  GET  /api/tools/search?q=    - Search tools")
    print("  GET  /api/tools/category/:c  - Filter by category")
    print("  POST /api/tools/scan         - Rescan filesystem")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5100, debug=True)
