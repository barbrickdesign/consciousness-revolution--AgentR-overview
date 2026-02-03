"""
ARAYA BRIDGE - Natural Language to File System
Connects ARAYA chat interface to actual file editing

Flow:
1. User types: "Make the homepage background blue"
2. This bridge calls Claude API to parse intent
3. Claude returns structured edit instructions
4. Bridge calls FILE_WRITER API to execute
5. User sees confirmation

Port: 5002
File Writer Port: 5001 (must be running)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Claude API setup
CLAUDE_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not CLAUDE_API_KEY:
    # Try reading from .env file
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ANTHROPIC_API_KEY='):
                    CLAUDE_API_KEY = line.split('=', 1)[1].strip()
                    break
    except:
        pass

if not CLAUDE_API_KEY:
    print("⚠️  WARNING: ANTHROPIC_API_KEY not found")
    print("Set it in .env or environment variable")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None

FILE_WRITER_URL = "http://localhost:5001"
DEPLOYMENT_ROOT = "C:/Users/dwrek/100X_DEPLOYMENT"

# Common file mappings
FILE_SHORTCUTS = {
    "homepage": "index.html",
    "landing": "landing.html",
    "araya chat": "ARAYA/1_INTERFACE/araya-chat.html",
    "welcome": "WELCOME.html",
    "login": "login.html",
    "signup": "signup.html",
}

def parse_edit_request(user_message, conversation_history=[]):
    """
    Use Claude API to parse natural language edit request

    Returns:
    {
        "action": "write|edit|append",
        "file_path": "relative/path/to/file.html",
        "content": "new content" (for write/append),
        "old_string": "text to replace" (for edit),
        "new_string": "replacement text" (for edit),
        "reasoning": "explanation of what we're doing"
    }
    """
    if not client:
        return {
            "error": "Claude API not configured",
            "reasoning": "ANTHROPIC_API_KEY missing"
        }

    # Build prompt
    system_prompt = """You are ARAYA's file editing intelligence.

Parse the user's edit request and return ONLY a JSON object (no markdown, no explanation).

Available files in 100X_DEPLOYMENT:
- index.html (homepage)
- landing.html (landing page)
- WELCOME.html (welcome page)
- login.html, signup.html (auth pages)
- ARAYA/1_INTERFACE/araya-chat.html (this chat interface)
- consciousness-tools.html (tools page)

JSON format:
{
    "action": "write|edit|append",
    "file_path": "relative/path.html",
    "content": "full new content" (for write),
    "old_string": "exact text to find" (for edit),
    "new_string": "replacement text" (for edit),
    "reasoning": "brief explanation"
}

For edits:
- Use "edit" action with old_string/new_string for surgical changes
- Use "write" action to create new files
- old_string must be EXACT match (include surrounding context)

Examples:
User: "make the homepage background blue"
{
    "action": "edit",
    "file_path": "index.html",
    "old_string": "background: white;",
    "new_string": "background: #0066ff;",
    "reasoning": "Changing homepage background to blue"
}

User: "add a welcome message to the top of the landing page"
{
    "action": "edit",
    "file_path": "landing.html",
    "old_string": "<body>",
    "new_string": "<body>\\n<h1 style='text-align:center;'>Welcome to Consciousness Revolution!</h1>",
    "reasoning": "Adding welcome message after body tag"
}
"""

    messages = []

    # Add conversation history
    for msg in conversation_history[-5:]:  # Last 5 messages for context
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

    # Add current request
    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )

        response_text = response.content[0].text.strip()

        # Remove markdown code blocks if present
        response_text = re.sub(r'^```json?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)

        parsed = json.loads(response_text)
        return parsed

    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse Claude response",
            "reasoning": str(e),
            "raw_response": response_text[:500]
        }
    except Exception as e:
        return {
            "error": "Claude API error",
            "reasoning": str(e)
        }

def execute_file_operation(parsed_intent):
    """
    Execute the file operation using FILE_WRITER API
    """
    import requests

    action = parsed_intent.get("action")
    file_path = parsed_intent.get("file_path")

    if not action or not file_path:
        return {
            "success": False,
            "error": "Missing action or file_path",
            "parsed_intent": parsed_intent
        }

    # Build request to file writer
    payload = {
        "file_path": file_path,
        "action": action
    }

    if action == "write":
        payload["content"] = parsed_intent.get("content", "")
    elif action == "append":
        payload["content"] = parsed_intent.get("content", "")
    elif action == "edit":
        payload["old_string"] = parsed_intent.get("old_string", "")
        payload["new_string"] = parsed_intent.get("new_string", "")
        payload["content"] = ""  # Required by API but not used for edit

    try:
        response = requests.post(
            f"{FILE_WRITER_URL}/write-file",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            result["reasoning"] = parsed_intent.get("reasoning", "")
            return result
        else:
            return {
                "success": False,
                "error": f"File writer returned {response.status_code}",
                "details": response.text
            }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "File writer not running",
            "hint": "Start it with: python ARAYA_FILE_WRITER.py"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.route('/edit', methods=['POST'])
def handle_edit():
    """
    Main endpoint: Natural language edit request

    Expected JSON:
    {
        "message": "user's natural language request",
        "conversation_history": [...previous messages...]
    }

    Returns:
    {
        "success": true/false,
        "reasoning": "what we did",
        "file_path": "file that was edited",
        "preview": "preview of change"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Step 1: Parse intent with Claude
        parsed = parse_edit_request(user_message, conversation_history)

        if "error" in parsed:
            return jsonify({
                "success": False,
                "stage": "parsing",
                "error": parsed.get("error"),
                "reasoning": parsed.get("reasoning", ""),
                "raw_response": parsed.get("raw_response", "")
            })

        # Step 2: Execute file operation
        result = execute_file_operation(parsed)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }), 500

@app.route('/chat', methods=['POST'])
def handle_chat():
    """
    Chat endpoint (no file editing, just conversation)

    Expected JSON:
    {
        "message": "user message",
        "conversation_history": [...]
    }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])

        if not client:
            return jsonify({
                "response": "I'm not fully configured yet. Missing ANTHROPIC_API_KEY.",
                "error": "API key missing"
            })

        # Build messages
        messages = []
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system="You are ARAYA, a helpful AI assistant for the Consciousness Revolution platform. You can chat and also help users edit website files. Be friendly and concise.",
            messages=messages
        )

        return jsonify({
            "response": response.content[0].text,
            "model": "claude-3-5-sonnet-20241022"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "response": f"Error: {str(e)}"
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    status = {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "claude_api": "configured" if client else "missing",
        "file_writer": FILE_WRITER_URL
    }

    # Test file writer connection
    try:
        import requests
        r = requests.get(f"{FILE_WRITER_URL}/health", timeout=2)
        if r.status_code == 200:
            status["file_writer_status"] = "connected"
        else:
            status["file_writer_status"] = "error"
    except:
        status["file_writer_status"] = "not running"

    return jsonify(status)

if __name__ == '__main__':
    print("=" * 60)
    print("🌉 ARAYA BRIDGE - Natural Language to File System")
    print("=" * 60)
    print(f"🧠 Claude API: {'✅ Configured' if client else '❌ Missing ANTHROPIC_API_KEY'}")
    print(f"📁 File Writer: {FILE_WRITER_URL}")
    print(f"🌐 Bridge running on: http://localhost:5002")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /edit   - Natural language file editing")
    print("  POST /chat   - General conversation")
    print("  GET  /health - Health check")
    print("\nMake sure ARAYA_FILE_WRITER.py is running on port 5001!")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5002,
        debug=True
    )
