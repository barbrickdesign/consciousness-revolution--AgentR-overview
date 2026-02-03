"""
ARAYA FILE WRITER - Flask endpoint for live website editing
Allows ARAYA to write/edit files within 100X_DEPLOYMENT
Security: Only allows writes within ALLOWED_ROOT
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow ARAYA chat to call this

ALLOWED_ROOT = "C:/Users/dwrek/100X_DEPLOYMENT"

def is_safe_path(path):
    """Validate path is within ALLOWED_ROOT"""
    try:
        real_path = os.path.realpath(path)
        real_root = os.path.realpath(ALLOWED_ROOT)
        return real_path.startswith(real_root)
    except:
        return False

@app.route('/write-file', methods=['POST'])
def write_file():
    """
    Write/edit files within 100X_DEPLOYMENT

    Expected JSON:
    {
        "file_path": "relative/or/absolute/path.html",
        "content": "file content here",
        "action": "write|append|edit"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        file_path = data.get('file_path')
        content = data.get('content')
        action = data.get('action', 'write')

        # For edit action, content is not required (uses old_string/new_string instead)
        if not file_path:
            return jsonify({"error": "Missing file_path"}), 400

        if action != 'edit' and content is None:
            return jsonify({"error": "Missing content"}), 400

        # Convert relative paths to absolute
        if not os.path.isabs(file_path):
            file_path = os.path.join(ALLOWED_ROOT, file_path)

        # Security check
        if not is_safe_path(file_path):
            return jsonify({
                "error": "Security violation: Path outside allowed root",
                "path": file_path,
                "allowed_root": ALLOWED_ROOT
            }), 403

        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Perform action
        if action == 'write':
            # Full write (overwrites)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        elif action == 'append':
            # Append to end
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)

        elif action == 'edit':
            # Edit requires old_string and new_string
            old_string = data.get('old_string')
            new_string = data.get('new_string')

            if not old_string or new_string is None:
                return jsonify({"error": "Edit action requires old_string and new_string"}), 400

            # Read existing
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing = f.read()
            else:
                existing = ""

            # Replace
            if old_string not in existing:
                return jsonify({
                    "error": "old_string not found in file",
                    "old_string": old_string[:100]
                }), 400

            new_content = existing.replace(old_string, new_string)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

        # Verify write
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)

            return jsonify({
                "success": True,
                "file_path": file_path,
                "action": action,
                "size": file_size,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": "Write appeared to succeed but file not found",
                "file_path": file_path
            }), 500

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

@app.route('/read-file', methods=['POST'])
def read_file():
    """Read file contents (for verification)"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')

        if not file_path:
            return jsonify({"error": "Missing file_path"}), 400

        # Convert relative to absolute
        if not os.path.isabs(file_path):
            file_path = os.path.join(ALLOWED_ROOT, file_path)

        # Security check
        if not is_safe_path(file_path):
            return jsonify({"error": "Security violation"}), 403

        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return jsonify({
            "success": True,
            "file_path": file_path,
            "content": content,
            "size": len(content)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/list-files', methods=['POST'])
def list_files():
    """List files in directory"""
    try:
        data = request.get_json()
        dir_path = data.get('dir_path', '.')

        # Convert relative to absolute
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(ALLOWED_ROOT, dir_path)

        # Security check
        if not is_safe_path(dir_path):
            return jsonify({"error": "Security violation"}), 403

        if not os.path.exists(dir_path):
            return jsonify({"error": "Directory not found"}), 404

        files = []
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            files.append({
                "name": item,
                "type": "dir" if os.path.isdir(item_path) else "file",
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            })

        return jsonify({
            "success": True,
            "dir_path": dir_path,
            "files": files
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "alive",
        "allowed_root": ALLOWED_ROOT,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"🔧 ARAYA FILE WRITER starting...")
    print(f"📁 Allowed root: {ALLOWED_ROOT}")
    print(f"🌐 Running on http://localhost:5001")

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
