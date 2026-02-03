#!/usr/bin/env python3
"""Create all 17 detector/analyzer HTML files for consciousness-tools.html"""

tools = [
    ('GASLIGHTING_DETECTOR', 'Gaslighting Detector', '🌀', 'Identify reality distortion attempts and consciousness manipulation patterns.', 'Analyze communications for signs of gaslighting - reality distortion, denial of facts, questioning your perception, and making you doubt your memory.'),
    ('EMOTIONAL_BLACKMAIL_DETECTOR', 'Emotional Blackmail Detector', '⚡', 'Detect guilt trips, fear tactics, and emotional leverage attempts.', 'Identify FOG patterns (Fear, Obligation, Guilt), threats, ultimatums, and emotional manipulation tactics.'),
    ('LOVE_BOMBING_DETECTOR', 'Love Bombing Detector', '💣', 'Recognize excessive early affection as manipulation strategy.', 'Detect overwhelming flattery, excessive gifts, constant attention, and premature intimacy used to gain control.'),
    ('TRIANGULATION_DETECTOR', 'Triangulation Detector', '📐', 'Identify divide-and-conquer relationship manipulation.', 'Recognize when a third party is being used to create jealousy, competition, or conflict in relationships.'),
    ('FUTURE_FAKING_DETECTOR', 'Future Faking Detector', '🔮', 'Detect false promises and unrealistic future projections.', 'Identify vague promises, postponed commitments, and unrealistic future plans used to maintain control.'),
    ('HOOVERING_DETECTOR', 'Hoovering Detector', '🌪️', 'Recognize manipulation attempts to pull you back in.', 'Detect attempts to reestablish contact after no-contact, including apologies, emergencies, and nostalgia tactics.'),
    ('EMAIL_ANALYZER', 'Email Analyzer', '📧', 'Deep analysis of email communication for hidden patterns.', 'Paste an email to analyze tone, manipulation tactics, hidden meanings, and recommended responses.'),
    ('WORD_SALAD_TRANSLATOR', 'Word Salad Translator', '🥗', 'Decode confusing circular language and deflection.', 'Translate confusing, circular, or evasive language into clear, direct statements.'),
    ('DOUBLE_BIND_DECODER', 'Double Bind Decoder', '🔀', 'Identify no-win situations and contradictory demands.', "Recognize when you're given contradictory options where every choice leads to criticism or failure."),
    ('PASSIVE_AGGRESSIVE_DECODER', 'Passive Aggressive Decoder', '🎭', 'Recognize indirect hostility and hidden anger.', 'Identify sarcasm, backhanded compliments, silent treatment, and other indirect expressions of anger.'),
    ('REALITY_CHECK', 'Reality Check', '✅', 'Ground yourself in objective facts vs. feelings.', 'Separate facts from feelings, external from internal, and verify your perception against objective reality.'),
    ('TRUTH_SIGNAL_FINDER', 'Truth Signal Finder', '📡', 'Filter through noise to find authentic truth signals.', 'Identify authentic communications vs. manipulation, deception, or hidden agendas.'),
    ('SOURCE_VERIFIER', 'Source Verifier', '🔍', 'Verify information sources and check credibility.', 'Evaluate the credibility of information sources and check for bias, accuracy, and reliability.'),
    ('BELIEF_CHECKER', 'Belief Checker', '💭', 'Examine beliefs for accuracy and usefulness.', 'Question limiting beliefs, identify cognitive distortions, and evaluate whether beliefs serve you.'),
    ('BOUNDARY_SETTER', 'Boundary Setter', '🚧', 'Create and communicate clear personal boundaries.', 'Draft clear boundary statements, practice saying no, and create scripts for boundary conversations.'),
    ('BOUNDARY_VIOLATION_TRACKER', 'Boundary Violation Tracker', '⚠️', 'Track and pattern boundary violations over time.', 'Log boundary violations, identify patterns, and track escalation or improvement over time.'),
    ('RESPONSE_PLANNER', 'Response Planner', '🎯', 'Plan strategic responses to manipulation attempts.', 'Create strategic response scripts, practice gray rock technique, and plan exit strategies.'),
]

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Consciousness Tools</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #2e1a1a 100%);
            color: #f4f4f4;
            min-height: 100vh;
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 2rem; }}
        .header {{ text-align: center; padding: 3rem 0; border-bottom: 2px solid rgba(255, 95, 86, 0.3); margin-bottom: 2rem; }}
        .header .icon {{ font-size: 4rem; margin-bottom: 1rem; }}
        .header h1 {{ font-size: 2.5rem; color: #ff5f56; text-shadow: 0 0 30px rgba(255, 95, 86, 0.6); margin-bottom: 0.5rem; }}
        .header p {{ color: rgba(255, 95, 86, 0.7); }}
        .back-button {{
            position: fixed; top: 2rem; left: 2rem;
            padding: 0.75rem 1.5rem; background: rgba(255, 95, 86, 0.1);
            border: 2px solid rgba(255, 95, 86, 0.3); border-radius: 8px;
            color: #ff5f56; text-decoration: none; font-weight: 600;
            transition: all 0.3s ease; z-index: 100;
        }}
        .back-button:hover {{ background: rgba(255, 95, 86, 0.2); transform: translateX(-5px); }}
        .tool-section {{
            background: rgba(46, 26, 26, 0.6); border: 2px solid rgba(255, 95, 86, 0.2);
            border-radius: 12px; padding: 2rem; margin-bottom: 2rem;
        }}
        .tool-section h2 {{ color: #ff5f56; margin-bottom: 1rem; }}
        textarea {{
            width: 100%; min-height: 200px; padding: 1rem;
            background: rgba(0, 0, 0, 0.3); border: 2px solid rgba(255, 95, 86, 0.3);
            border-radius: 8px; color: #f4f4f4; font-size: 1rem; resize: vertical;
        }}
        textarea:focus {{ outline: none; border-color: #ff5f56; }}
        .analyze-btn {{
            width: 100%; padding: 1rem; margin-top: 1rem;
            background: linear-gradient(135deg, #ff5f56, #ff8c56);
            border: none; border-radius: 8px; color: white;
            font-size: 1.2rem; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease;
        }}
        .analyze-btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(255, 95, 86, 0.3); }}
        .results {{ margin-top: 2rem; padding: 1.5rem; background: rgba(0, 0, 0, 0.3); border-radius: 8px; display: none; }}
        .results.active {{ display: block; }}
        .results h3 {{ color: #ff5f56; margin-bottom: 1rem; }}
        .result-item {{ padding: 0.75rem 0; border-bottom: 1px solid rgba(255, 95, 86, 0.1); }}
        .result-item:last-child {{ border-bottom: none; }}
        .warning {{ color: #ff5f56; }}
        .safe {{ color: #00ff88; }}
        @media (max-width: 768px) {{
            .back-button {{ position: static; margin-bottom: 1rem; display: inline-block; }}
        }}
    </style>
</head>
<body>
    <a href="consciousness-tools.html" class="back-button">← Tools</a>
    <div class="container">
        <div class="header">
            <div class="icon">{icon}</div>
            <h1>{title}</h1>
            <p>{short_desc}</p>
        </div>
        <div class="tool-section">
            <h2>Enter Text to Analyze</h2>
            <p style="color: rgba(255,255,255,0.6); margin-bottom: 1rem;">{long_desc}</p>
            <textarea id="inputText" placeholder="Paste the text you want to analyze here..."></textarea>
            <button class="analyze-btn" onclick="analyzeText()">🔍 Analyze</button>
        </div>
        <div class="results" id="results">
            <h3>Analysis Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
    <script>
        function analyzeText() {{
            const text = document.getElementById('inputText').value;
            if (!text.trim()) {{
                console.warn('Please enter text to analyze');
                return;
            }}
            const results = document.getElementById('results');
            const content = document.getElementById('resultsContent');
            results.classList.add('active');
            content.innerHTML = '<div class="result-item"><span class="warning">⚠️ Analysis requires Araya AI connection.</span></div><div class="result-item">For now, review the text manually using these guidelines:</div><div class="result-item">1. Look for patterns that match the tool\\'s purpose</div><div class="result-item">2. Trust your instincts</div><div class="result-item">3. Consider the source and context</div><div class="result-item"><a href="araya-chat.html" style="color: #ff5f56;">→ Discuss with Araya AI</a></div>';
        }}
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.location.href = 'consciousness-tools.html';
        }});
    </script>
</body>
</html>'''

if __name__ == '__main__':
    import os
    os.chdir('C:/Users/dwrek/100X_DEPLOYMENT')

    for filename, title, icon, short_desc, long_desc in tools:
        html = template.format(title=title, icon=icon, short_desc=short_desc, long_desc=long_desc)
        with open(f'{filename}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Created {filename}.html')

    print(f'\\nDone! Created {len(tools)} detector files.')
