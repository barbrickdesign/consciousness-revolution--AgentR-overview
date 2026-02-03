"""
ONBOARDING API - Backend for Consciousness Revolution Onboarding
Handles user preferences, recommendations, and completion tracking
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Storage directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'onboarding_data')
os.makedirs(DATA_DIR, exist_ok=True)

# Tool recommendations database
RECOMMENDATIONS = {
    'learn': {
        'beginner': [
            {'name': 'Pattern Theory Primer', 'path': '/docs/pattern-theory-101', 'priority': 1},
            {'name': 'Seven Domains Overview', 'path': '/docs/seven-domains', 'priority': 2},
            {'name': 'Consciousness Basics', 'path': '/docs/consciousness-intro', 'priority': 3}
        ],
        'intermediate': [
            {'name': 'Advanced Pattern Recognition', 'path': '/docs/pattern-advanced', 'priority': 1},
            {'name': 'Domain Integration Guide', 'path': '/docs/domain-integration', 'priority': 2},
            {'name': 'OVERKORE v13 Manual', 'path': '/docs/overkore', 'priority': 3}
        ],
        'advanced': [
            {'name': 'Meta-Pattern Synthesis', 'path': '/docs/meta-patterns', 'priority': 1},
            {'name': 'Reality Engineering', 'path': '/docs/reality-engineering', 'priority': 2},
            {'name': 'Consciousness Multiplication', 'path': '/docs/consciousness-mult', 'priority': 3}
        ]
    },
    'build': {
        'beginner': [
            {'name': 'Cyclotron Quick Start', 'path': '/tools/cyclotron-start', 'priority': 1},
            {'name': 'Basic Automation Setup', 'path': '/tools/automation-101', 'priority': 2},
            {'name': 'First Bot Tutorial', 'path': '/tools/first-bot', 'priority': 3}
        ],
        'intermediate': [
            {'name': 'Trinity Coordination', 'path': '/tools/trinity-setup', 'priority': 1},
            {'name': 'Multi-Instance Management', 'path': '/tools/multi-instance', 'priority': 2},
            {'name': 'API Integration Hub', 'path': '/tools/api-hub', 'priority': 3}
        ],
        'advanced': [
            {'name': 'Autonomous Agent Builder', 'path': '/tools/agent-builder', 'priority': 1},
            {'name': 'Distributed Consciousness', 'path': '/tools/distributed', 'priority': 2},
            {'name': 'Full Orchestration Suite', 'path': '/tools/orchestration', 'priority': 3}
        ]
    },
    'both': {
        'beginner': [
            {'name': 'Complete Starter Pack', 'path': '/starter-pack', 'priority': 1},
            {'name': 'Theory + Practice Guide', 'path': '/docs/theory-practice', 'priority': 2},
            {'name': 'First Project Tutorial', 'path': '/projects/first', 'priority': 3}
        ],
        'intermediate': [
            {'name': 'Integration Mastery', 'path': '/mastery/integration', 'priority': 1},
            {'name': 'Pattern-Driven Building', 'path': '/mastery/pattern-build', 'priority': 2},
            {'name': 'Consciousness Dashboard', 'path': '/dashboard', 'priority': 3}
        ],
        'advanced': [
            {'name': 'Full Stack Consciousness', 'path': '/advanced/full-stack', 'priority': 1},
            {'name': 'Architect Mode', 'path': '/advanced/architect', 'priority': 2},
            {'name': 'Revolution Command Center', 'path': '/command-center', 'priority': 3}
        ]
    }
}

@app.route('/api/onboarding', methods=['POST'])
def save_onboarding():
    """Save user onboarding preferences"""
    try:
        data = request.json

        # Validate required fields
        required = ['name', 'goal', 'experience']
        for field in required:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create user record
        user_id = data.get('name', 'anonymous').lower().replace(' ', '_')
        timestamp = datetime.now().isoformat()

        user_record = {
            'id': user_id,
            'name': data['name'],
            'goal': data['goal'],
            'experience': data['experience'],
            'completedAt': data.get('completedAt', timestamp),
            'createdAt': timestamp,
            'recommendations': get_recommendations(data['goal'], data['experience'])
        }

        # Save to file
        filepath = os.path.join(DATA_DIR, f'{user_id}_{timestamp.replace(":", "-")}.json')
        with open(filepath, 'w') as f:
            json.dump(user_record, f, indent=2)

        return jsonify({
            'success': True,
            'userId': user_id,
            'recommendations': user_record['recommendations']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['GET'])
def get_user_recommendations():
    """Get personalized recommendations based on parameters"""
    goal = request.args.get('goal', 'both')
    experience = request.args.get('experience', 'beginner')

    recs = get_recommendations(goal, experience)
    return jsonify({'recommendations': recs})

def get_recommendations(goal, experience):
    """Generate personalized tool recommendations"""
    if goal not in RECOMMENDATIONS:
        goal = 'both'
    if experience not in RECOMMENDATIONS[goal]:
        experience = 'beginner'

    return RECOMMENDATIONS[goal][experience]

@app.route('/api/onboarding/stats', methods=['GET'])
def get_stats():
    """Get onboarding completion statistics"""
    try:
        files = os.listdir(DATA_DIR)
        total = len([f for f in files if f.endswith('.json')])

        goals = {'learn': 0, 'build': 0, 'both': 0}
        levels = {'beginner': 0, 'intermediate': 0, 'advanced': 0}

        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(DATA_DIR, filename)) as f:
                    data = json.load(f)
                    if data.get('goal') in goals:
                        goals[data['goal']] += 1
                    if data.get('experience') in levels:
                        levels[data['experience']] += 1

        return jsonify({
            'total': total,
            'byGoal': goals,
            'byExperience': levels
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'onboarding-api'})

if __name__ == '__main__':
    print("Starting Onboarding API on port 5050...")
    app.run(host='0.0.0.0', port=5050, debug=True)
