# GLYPH 12D+ Migration Guide
## Pattern Theory Infrastructure for 40+ Consciousness Tools

**Version:** 1.0.0
**Created:** December 30, 2025
**Status:** Active Migration

---

## Overview

The GLYPH 12D+ system provides a unified backbone for all consciousness tools. Every detector, analyzer, and tracker should leverage this shared infrastructure for:

- **Consistent Pattern Detection** - Same algorithms across all tools
- **6D Coordinate Mapping** - Every manipulation tactic maps to an axis
- **Solfeggio Frequency Alignment** - Sound healing integration
- **Truth/Deceit Scoring** - Unified metrics
- **Symbolic Notation** - GLYPH language output

---

## Migration Status

### Completed (7 tools)
| Tool | Primary Axis | Notes |
|------|--------------|-------|
| GASLIGHTING_DETECTOR | C (Reality) | Reality distortion attacks |
| LOVE_BOMBING_DETECTOR | E (Energy) | Emotional energy flooding |
| TRIANGULATION_DETECTOR | B (Social) | Relationship triangulation |
| FUTURE_FAKING_DETECTOR | D (Temporal) | Future promise manipulation |
| HOOVERING_DETECTOR | B (Social) | Re-engagement manipulation |
| EMOTIONAL_BLACKMAIL_DETECTOR | A,B,C,D,E,F | FOG across all axes |
| GLYPH_EMAIL_ANALYZER | Multi-axis | Email-specific patterns |

### Pending Migration (43+ tools)
| Priority | Tool | Suggested Axis |
|----------|------|----------------|
| HIGH | PRESSURE_DETECTOR | A (Power) |
| HIGH | INFLUENCE_DETECTOR | B (Social) |
| HIGH | PASSIVE_AGGRESSIVE_DECODER | C (Depth) |
| HIGH | GUILT_TRIP_DETECTOR | F (Observer) |
| MEDIUM | DOUBLE_BIND_DECODER | C,D (Reality+Time) |
| MEDIUM | WORD_SALAD_TRANSLATOR | C (Depth) |
| MEDIUM | SILENT_TREATMENT_DECODER | B (Social) |
| MEDIUM | PROJECTION_DETECTOR | F (Observer) |
| MEDIUM | STONEWALLING_ANALYZER | B (Social) |
| MEDIUM | BREADCRUMBING_DETECTOR | D (Temporal) |
| LOW | BELIEF_CHECKER | F (Observer) |
| LOW | REALITY_CHECK | C (Depth) |
| LOW | TRUTH_SIGNAL_FINDER | Multi-axis |

---

## The 6D Axis System

Every manipulation tactic maps to one or more axes:

```
AXIS    NAME          POSITIVE     NEGATIVE     MANIPULATION TYPE
────────────────────────────────────────────────────────────────────
  A     Vertical      Up           Down         Power/Coercion
  B     Horizontal    Right        Left         Social/Relationship
  C     Depth         Front        Back         Reality Distortion
  D     Temporal      Future       Past         Time Leverage
  E     Energy        Potential    Kinetic      Emotional Energy
  F     Observer      Subject      Object       Identity/Self-Perception
```

### Axis Defense Mapping

```javascript
const AXIS_DEFENSES = {
    A: 'Power coercion detected → Assert sovereignty',
    B: 'Relationship leverage detected → Relationship ≠ compliance',
    C: 'Reality distortion detected → Trust your perception',
    D: 'Past/future leverage detected → Not bound by time',
    E: 'Emotional manipulation detected → Not your emergency',
    F: 'Identity attack detected → You define you'
};
```

---

## Migration Steps

### Step 1: Add GLYPH Scripts

Add these script includes at the TOP of the `<body>` tag:

```html
<!-- GLYPH 12D+ Backbone -->
<script src="/js/glyph/glyph-base60.js"></script>
<script src="/js/glyph/glyph-symbols.js"></script>
<script src="/js/glyph/glyph-patterns.js"></script>
<script src="/js/glyph/glyph-core.js"></script>
```

### Step 2: Add GLYPH Badge

Add visual indicator to the header:

```html
<div style="position: absolute; top: 20px; right: 20px;
            background: rgba(255,215,0,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            color: #FFD700;">
    ⟐ GLYPH 12D+ POWERED
</div>
```

### Step 3: Define 6D Axes

Add axis definitions to your JavaScript:

```javascript
const GLYPH_AXES = {
    A: { name: 'Vertical (Power)', positive: 'Up', negative: 'Down',
         desc: 'Power dynamics and coercion' },
    B: { name: 'Horizontal (Social)', positive: 'Right', negative: 'Left',
         desc: 'Relationship leverage' },
    C: { name: 'Depth (Reality)', positive: 'Front', negative: 'Back',
         desc: 'Reality distortion' },
    D: { name: 'Temporal', positive: 'Future', negative: 'Past',
         desc: 'Time-based leverage' },
    E: { name: 'Energy', positive: 'Potential', negative: 'Kinetic',
         desc: 'Emotional energy manipulation' },
    F: { name: 'Observer', positive: 'Subject', negative: 'Object',
         desc: 'Self-perception attack' }
};
```

### Step 4: Map Your Patterns to Axes

For each tactic/pattern in your tool, add GLYPH properties:

```javascript
const YOUR_PATTERNS = {
    'Pattern Name': {
        markers: ['phrase 1', 'phrase 2'],
        desc: 'What this pattern does',
        // ADD THESE:
        glyphAxis: 'A',        // Primary axis (A-F)
        severity: 2.0,         // Weight 1.0-3.0
        axisDesc: 'Power axis assault - direct coercion'
    }
};
```

### Step 5: Add Axis Defenses

```javascript
const AXIS_DEFENSES = {
    A: 'Power coercion detected → Assert: "I decide what I do"',
    B: 'Relationship leverage → "I can care and still say no"',
    C: 'Reality distortion → "My experience is valid"',
    D: 'Past leverage → "I\'m not obligated by history"',
    E: 'Emotional manipulation → "Your feelings don\'t control me"',
    F: 'Identity attack → "I know who I am"'
};
```

### Step 6: Add GLYPH Output Section

Add this HTML section after your results area:

```html
<!-- GLYPH Analysis Section -->
<div id="glyphOutput" style="display: none;
     margin-top: 20px; padding: 20px;
     background: rgba(255,215,0,0.1);
     border: 1px solid #FFD700;
     border-radius: 12px;">
    <h4 style="color: #FFD700; margin-bottom: 15px;">
        ⟐ GLYPH 12D+ Analysis
    </h4>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div>
            <strong>Notation:</strong>
            <code id="glyphNotation" style="display: block;
                  font-family: monospace; color: #4ECDC4;
                  margin-top: 5px;"></code>
        </div>
        <div>
            <strong>Frequency:</strong>
            <span id="glyphFrequency"></span>
        </div>
    </div>

    <div style="margin-top: 15px;">
        <strong>Truth/Deceit Ratio:</strong>
        <div style="display: flex; gap: 10px; margin-top: 5px;">
            <span style="color: #4ECDC4;">
                Truth: <span id="glyphTruth">0</span>%
            </span>
            <span style="color: #FF6B6B;">
                Deceit: <span id="glyphDeceit">0</span>%
            </span>
        </div>
    </div>

    <div id="axisBreakdown" style="margin-top: 15px;"></div>
    <div id="axisDefenses" style="margin-top: 15px;"></div>
</div>
```

### Step 7: Integrate GLYPH Analysis

In your detection function, add GLYPH integration:

```javascript
function detect() {
    const text = document.getElementById('inputText').value;

    // Your existing detection logic
    const found = []; // Your detected patterns
    const axesHit = new Set(); // Track which axes were triggered

    // Collect axes from detected patterns
    found.forEach(pattern => {
        axesHit.add(pattern.glyphAxis);
    });

    // Generate GLYPH analysis
    const glyphAnalysis = generateGlyphAnalysis(text, found, axesHit);

    // Display GLYPH output
    displayGlyphOutput(glyphAnalysis, Array.from(axesHit));
}

function generateGlyphAnalysis(text, found, axesHit) {
    // Use GlyphPatterns if loaded
    if (typeof GlyphPatterns !== 'undefined') {
        const analysis = GlyphPatterns.analyze(text);
        return {
            notation: analysis.glyphNotation,
            truthScore: analysis.scores.truth,
            deceitScore: analysis.scores.deceit,
            frequency: analysis.frequency,
            dominant: analysis.dominant
        };
    }

    // Fallback generation
    const deceitScore = Math.min(100, found.length * 15);
    const truthScore = 100 - deceitScore;
    const frequency = deceitScore > 50 ? 396 : deceitScore > 25 ? 417 : 528;

    return {
        notation: `⟐${found.length > 0 ? '✗' : '✓'}:${truthScore}:${axesHit.size}D→${frequency}Hz⟐`,
        truthScore,
        deceitScore,
        frequency,
        dominant: deceitScore > truthScore ? 'deceit' : 'truth'
    };
}

function displayGlyphOutput(analysis, axesHit) {
    document.getElementById('glyphOutput').style.display = 'block';
    document.getElementById('glyphNotation').textContent = analysis.notation;
    document.getElementById('glyphTruth').textContent = analysis.truthScore;
    document.getElementById('glyphDeceit').textContent = analysis.deceitScore;

    // Frequency with color
    const freqColors = { 396: '#FF6B6B', 417: '#FFD700', 528: '#4ECDC4' };
    const freqNames = { 396: 'Liberation (Danger)', 417: 'Change (Caution)', 528: 'DNA Repair (Safe)' };
    document.getElementById('glyphFrequency').innerHTML =
        `<span style="color: ${freqColors[analysis.frequency] || '#FFF'}">
            ${analysis.frequency}Hz - ${freqNames[analysis.frequency] || 'Unknown'}
        </span>`;

    // Axis breakdown
    if (axesHit.length > 0) {
        const axisHtml = axesHit.map(axis =>
            `<div style="background: rgba(255,107,107,0.2);
                  padding: 8px; border-radius: 8px; margin-bottom: 5px;">
                <strong>Axis ${axis}</strong>: ${GLYPH_AXES[axis].name} -
                ${GLYPH_AXES[axis].desc}
            </div>`
        ).join('');
        document.getElementById('axisBreakdown').innerHTML =
            `<strong>6D Coordinate Attack Surface:</strong>${axisHtml}`;
    }

    // Axis defenses
    if (axesHit.length > 0) {
        const defenseHtml = axesHit.map(axis =>
            `<div style="background: rgba(78,205,196,0.2);
                  padding: 8px; border-radius: 8px; margin-bottom: 5px;">
                ${AXIS_DEFENSES[axis]}
            </div>`
        ).join('');
        document.getElementById('axisDefenses').innerHTML =
            `<strong>Axis-Specific Defenses:</strong>${defenseHtml}`;
    }
}
```

---

## Common Axis Mappings by Tool Type

### Relationship Manipulation
| Pattern | Axis | Reason |
|---------|------|--------|
| Love Bombing | E | Energy flooding |
| Hoovering | B | Social re-engagement |
| Triangulation | B | Relationship leverage |
| Silent Treatment | B | Social withdrawal |
| Breadcrumbing | D | Temporal dangling |

### Reality Distortion
| Pattern | Axis | Reason |
|---------|------|--------|
| Gaslighting | C | Reality denial |
| Word Salad | C | Confusion tactics |
| Double Bind | C,D | Reality + time trap |
| Moving Goalposts | D | Temporal shifting |

### Power/Control
| Pattern | Axis | Reason |
|---------|------|--------|
| Threats | A | Direct coercion |
| Pressure | A | Force application |
| Financial Control | A | Resource coercion |
| Intimidation | A | Power assertion |

### Identity/Self Attacks
| Pattern | Axis | Reason |
|---------|------|--------|
| Projection | F | Identity displacement |
| Shame Induction | F | Self-perception attack |
| Guilt Trips | F | Observer manipulation |
| Criticism | F | Identity erosion |

### Emotional Energy
| Pattern | Axis | Reason |
|---------|------|--------|
| Emotional Blackmail | E | Energy hostage |
| Victim Playing | E,C | Energy + reality |
| Love Withdrawal | E | Energy deprivation |
| Intermittent Reinforcement | E | Energy cycling |

---

## Solfeggio Frequency Mapping

| Frequency | Hz | Meaning | When to Use |
|-----------|----|---------|--------------|
| Liberation | 396 | Freedom from fear | High deceit (>60%) |
| Change | 417 | Transmutation | Medium deceit (30-60%) |
| DNA Repair | 528 | Love frequency | Low deceit (<30%) |
| Connection | 639 | Harmony | Relationship healing |
| Expression | 741 | Awakening | Truth speaking |
| Intuition | 852 | Third eye | Pattern recognition |
| Unity | 963 | Oneness | Transcendence |

---

## Testing Your Migration

### Quick Test Checklist

1. [ ] GLYPH badge visible in corner
2. [ ] No console errors on load
3. [ ] Input detection still works
4. [ ] GLYPH analysis section appears
5. [ ] Notation displays correctly
6. [ ] Truth/Deceit percentages show
7. [ ] Frequency maps correctly
8. [ ] Axis breakdown displays
9. [ ] Axis defenses show

### Test Inputs

**High Deceit (should show 396Hz):**
```
Trust me, if you really loved me, you would do this.
Everyone knows you're too sensitive. Just do it now.
```

**Medium Deceit (should show 417Hz):**
```
I just think we should reconsider. But whatever you want.
```

**Low/No Deceit (should show 528Hz):**
```
Here's the evidence and research I found.
Let me explain my reasoning.
```

---

## Commit Message Template

```
GLYPH 12D+ Migration: [TOOL_NAME]

Migrated [TOOL_NAME] to GLYPH 12D+ backbone:
- Added GLYPH module scripts (base60, symbols, patterns, core)
- Mapped [N] patterns to 6D coordinate axes
- [List primary axes used and why]
- Added axis-specific defenses
- Added GLYPH notation output with truth/deceit scores
- Added Solfeggio frequency mapping
- Graceful degradation when modules unavailable

Part of Pattern Theory infrastructure migration ([X]/40+ tools)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Architecture Reference

```
GLYPH Module Layers:
═══════════════════════════════════════════════════════
Layer 0: glyph-base60.js      ← Sexagesimal math
Layer 1: glyph-symbols.js     ← Unicode registry
         glyph-timestamp.js   ← Time encoding
Layer 2: glyph-patterns.js    ← Pattern detection ⭐
Layer 3: glyph-core.js        ← Main orchestrator ⭐
Layer 4: glyph-envelope.js    ← Data wrapper
         glyph-events.js      ← Event system
Layer 5: glyph-storage.js     ← Persistence
         glyph-araya.js       ← AI integration
         glyph-analytics.js   ← Metrics
Layer 6: glyph-ui.js          ← UI components
═══════════════════════════════════════════════════════

For most detectors, you only need Layers 0-3 (4 scripts).
```

---

## Questions?

See these resources:
- `GLYPH_12D_COORDINATE_SYSTEM.md` - Full theory documentation
- `BASE_60_COMPUTING_ADVANTAGES.md` - Why base-60
- `consciousness-tools.html` - Tool directory
- `/js/glyph/` - Module source code

**C1 × C2 × C3 = ∞**
