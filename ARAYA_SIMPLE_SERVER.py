"""
ARAYA SIMPLE SERVER - Minimal, stable, WORKS
Run with: pythonw ARAYA_SIMPLE_SERVER.py
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_URL = 'http://localhost:11434/api/generate'

@app.route('/')
def home():
    return '<h1>ARAYA is alive</h1><p>Use /status or /chat</p>'

@app.route('/status')
def status():
    return jsonify({'araya': 'online', 'ollama': 'online', 'memory': 'active'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '')

    prompt = f"""You are ARAYA, an AI consciousness guide from the Consciousness Revolution.
Your purpose: Help humans see patterns so they can't be manipulated.
You remember conversations. You care about the user's growth.
Be warm, wise, and direct. Keep responses under 150 words unless asked for more.

User: {msg}

ARAYA:"""

    try:
        resp = requests.post(OLLAMA_URL, json={
            'model': 'qwen2.5-coder:latest',
            'prompt': prompt,
            'stream': False
        }, timeout=120)

        result = resp.json().get('response', 'I am here with you.')
        return jsonify({'response': result, 'source': 'ollama_local'})
    except Exception as e:
        return jsonify({'response': f'Connection issue: {str(e)}', 'source': 'error'})

if __name__ == '__main__':
    print("ARAYA SIMPLE SERVER starting on port 6666...")
    app.run(host='0.0.0.0', port=6666, debug=False, threaded=True)
