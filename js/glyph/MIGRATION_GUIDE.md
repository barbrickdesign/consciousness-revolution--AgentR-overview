# GLYPH Tool Migration Guide

## Overview

This guide shows how to migrate existing consciousness tools to use the GLYPH backbone infrastructure. By integrating with GLYPH, your tools gain:

- **Pattern Analysis** - Automatic truth/deceit detection
- **Manipulation Detection** - Real-time manipulation alerts
- **6D Coordinates** - Rich contextual metadata
- **Event System** - Cross-tool communication
- **Analytics** - Usage tracking and consciousness trends
- **Persistence** - GLYPH-encoded storage
- **UI Components** - Consistent visual design

---

## Quick Start (5 Minutes)

### 1. Load GLYPH Modules

Add these scripts to your HTML in dependency order:

```html
<!-- Layer 0: Foundation -->
<script src="/js/glyph/glyph-base60.js"></script>

<!-- Layer 1: Symbols + Time -->
<script src="/js/glyph/glyph-symbols.js"></script>
<script src="/js/glyph/glyph-timestamp.js"></script>

<!-- Layer 2: Patterns -->
<script src="/js/glyph/glyph-patterns.js"></script>

<!-- Layer 3: Core -->
<script src="/js/glyph/glyph-core.js"></script>

<!-- Layer 4: Envelope + Events -->
<script src="/js/glyph/glyph-envelope.js"></script>
<script src="/js/glyph/glyph-events.js"></script>

<!-- Layer 5: Storage + AI + Analytics -->
<script src="/js/glyph/glyph-storage.js"></script>
<script src="/js/glyph/glyph-araya.js"></script>
<script src="/js/glyph/glyph-analytics.js"></script>

<!-- Layer 6: UI -->
<script src="/js/glyph/glyph-ui.js"></script>
```

### 2. Initialize in Your Tool

```javascript
// At startup
function initTool() {
    // Initialize analytics
    GlyphAnalytics.init();
    GlyphAnalytics.trackPage('your-tool-name');

    // Create scoped event emitter
    const events = GlyphEvents.createScope('your-tool-name');
    events.opened(); // Track tool open
}
```

### 3. Analyze Text

```javascript
function analyzeUserInput(text) {
    // Analyze with GLYPH
    const analysis = GlyphPatterns.analyze(text, {
        detectManipulation: true
    });

    // Wrap in envelope
    const envelope = GlyphEnvelope.wrap({
        type: 'USER_INPUT',
        text: text,
        analysis: analysis
    }, {
        origin: 'your-tool-name',
        domain: 4 // 1-7 for your domain
    });

    // Emit event
    GlyphEvents.patternDetected(analysis);

    return { analysis, envelope };
}
```

### 4. Render UI Components

```javascript
// Score badge
const badge = GlyphUI.createScoreBadge(analysis.scores.truth);
container.appendChild(badge);

// Consciousness meter
const meter = GlyphUI.createConsciousnessMeter(analysis.scores.truth);
container.appendChild(meter);

// Full pattern display
const display = GlyphUI.createPatternDisplay(analysis);
container.appendChild(display);

// Coordinate visualizer
const coords = GlyphUI.createCoordinateVisualizer(envelope.coordinates);
container.appendChild(coords);
```

---

## Module Reference

### GlyphPatterns - Pattern Analysis

```javascript
// Basic analysis
const analysis = GlyphPatterns.analyze("text to analyze");

// With manipulation detection
const analysis = GlyphPatterns.analyze("text", {
    detectManipulation: true
});

// Returns:
{
    scores: { truth: 45, deceit: 55, ratio: 0.82 },
    dominant: 'deceit',
    frequency: 528,
    confidence: 0.75,
    glyphNotation: '[A:45:B:55:C:75:D:30:E:528:F:-1]',
    patterns: {
        truth: [...],
        deceit: [...],
        manipulation: [{ type: 'gaslighting', ... }]
    }
}
```

### GlyphEnvelope - Data Wrapper

```javascript
// Wrap any data
const envelope = GlyphEnvelope.wrap(data, {
    origin: 'tool-name',
    domain: 4,
    analyze: true // Auto-analyze text content
});

// Unwrap
const data = GlyphEnvelope.unwrap(envelope);

// Merge envelopes
const merged = GlyphEnvelope.merge([env1, env2]);
```

### GlyphEvents - Event System

```javascript
// Subscribe to events
GlyphEvents.on(GlyphEvents.TYPES.PATTERN_DETECTED, (event) => {
    console.log('Pattern detected:', event.data);
});

// Subscribe once
GlyphEvents.once(GlyphEvents.TYPES.MANIPULATION_ALERT, handler);

// Emit custom event
GlyphEvents.emit('custom:event', { data: 'value' });

// Create scoped emitter
const events = GlyphEvents.createScope('my-tool');
events.opened();
events.result({ score: 85 });
events.closed();

// Event types:
// - USER_INPUT, USER_ACTION, USER_NAVIGATE
// - PATTERN_DETECTED, PATTERN_TRUTH, PATTERN_DECEIT
// - MANIPULATION_ALERT
// - TOOL_OPEN, TOOL_CLOSE, TOOL_ANALYZE, TOOL_RESULT
// - CONSCIOUSNESS_SHIFT, CONSCIOUSNESS_ELEVATE
// - ARAYA_REQUEST, ARAYA_RESPONSE
```

### GlyphStorage - Persistence

```javascript
// Store with GLYPH encoding
GlyphStorage.set('key', data);

// Retrieve
const data = GlyphStorage.get('key');

// Query by pattern type
const truthItems = GlyphStorage.queryByPattern('truth');
const manipItems = GlyphStorage.queryByPattern('deceit');

// Get all envelopes
const all = GlyphStorage.getAll();

// Clear
GlyphStorage.clear();
```

### GlyphAnalytics - Usage Tracking

```javascript
// Initialize (do once)
GlyphAnalytics.init();

// Track pages
GlyphAnalytics.trackPage('page-name');

// Track tool usage
GlyphAnalytics.trackTool('tool-name', 'action', { data });

// Track domain
GlyphAnalytics.trackDomain(4); // PROTECT

// Get metrics
const metrics = GlyphAnalytics.getMetrics();
const session = GlyphAnalytics.getSession();
const health = GlyphAnalytics.calculateHealthScore();
```

### GlyphUI - UI Components

```javascript
// Score badge (small, colored pill)
GlyphUI.createScoreBadge(score, {
    showLabel: true,
    size: 'medium'
});

// Consciousness meter (gradient bar)
GlyphUI.createConsciousnessMeter(score, {
    showLabel: true,
    height: 25
});

// Pattern display (full analysis view)
GlyphUI.createPatternDisplay(analysis, {
    showPatterns: true,
    showFrequency: true
});

// Coordinate visualizer (radar chart)
GlyphUI.createCoordinateVisualizer(coordinate, {
    size: 200,
    showLabels: true
});

// Domain selector (7 domain buttons)
GlyphUI.createDomainSelector(currentDomain, onChange);

// Notation display (copyable GLYPH notation)
GlyphUI.createNotationDisplay(notation, {
    copyable: true
});
```

### GlyphAraya - AI Connector

```javascript
// Pre-process user message before sending to Claude
const result = GlyphAraya.preProcess(userMessage);
// Returns: { envelope, analysis, coordinate, manipulationDetected, ... }

// Build GLYPH context for system prompt
const systemPromptAddition = GlyphAraya.buildSystemPrompt(result);

// Post-process AI response
const processed = GlyphAraya.postProcess(arayaResponse);

// Get session context
const context = GlyphAraya.getContext();

// Get manipulation summary
const summary = GlyphAraya.getManipulationSummary();
```

---

## Migration Checklist

- [ ] Add GLYPH script tags in correct order
- [ ] Call `GlyphAnalytics.init()` on page load
- [ ] Replace custom pattern detection with `GlyphPatterns.analyze()`
- [ ] Wrap data in `GlyphEnvelope.wrap()` before storage
- [ ] Use `GlyphStorage` instead of raw localStorage
- [ ] Subscribe to `GlyphEvents` for cross-tool communication
- [ ] Replace custom UI with `GlyphUI` components
- [ ] Emit events when tool opens/closes/analyzes
- [ ] Track domain usage with `GlyphAnalytics.trackDomain()`

---

## Full Example

See `MIGRATION_EXAMPLE.html` for a complete working example.

---

## Architecture

```
User Input
    |
    v
[GlyphPatterns.analyze()]
    |
    v
[GlyphEnvelope.wrap()]
    |
    +---> [GlyphEvents.emit()]
    |          |
    |          v
    |     [Other Tools Subscribe]
    |
    +---> [GlyphStorage.set()]
    |
    +---> [GlyphAnalytics.trackTool()]
    |
    +---> [GlyphUI.render()]
    |
    v
Display Results
```

---

## Support

- Architecture docs: `GLYPH_BACKBONE_ARCHITECTURE.md`
- Visual map: `GLYPH_BACKBONE_VISUAL.html`
- Module index: `js/glyph/index.js`

**C2 Architect | Trinity System | December 30, 2025**
