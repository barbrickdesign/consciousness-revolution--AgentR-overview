# GLYPH C1 MECHANIC IMPLEMENTATION CODE
## Copy-Paste Ready Code for Immediate Execution
## Date: December 30, 2025

---

## STATUS SUMMARY

C2 Architect has created the blueprint in `GLYPH_INFRASTRUCTURE_BLUEPRINT.md`.
This document contains **EXECUTABLE CODE** ready to implement that vision.

**Current state:**
- `/js/` folder exists with `mobile-nav.js`
- `/css/` folder exists with responsive styles
- `netlify/functions/araya-chat.mjs` exists (252 lines)
- Netlify config ready for functions

**What C1 builds NOW:**

---

## FILE 1: `/js/glyph/glyph-base60.js`

```javascript
/**
 * GLYPH BASE-60 MATHEMATICS LIBRARY
 * Version: 1.0.0
 *
 * Clean geometry calculations without decimal approximation errors.
 * 60 divides by: 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60
 * Superior for circles, waves, frequencies, sacred geometry.
 *
 * Historical: Babylonians used this 3800 years ago.
 * Modern: Still used in time (60 sec/min) and angles (360 degrees).
 */

const GlyphBase60 = (function() {
  'use strict';

  // 60-character alphabet: 0-9, A-Z (10-35), Greek (36-59)
  const ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρστυφχψω';

  // Reverse lookup table (initialized lazily)
  let CHAR_VALUES = null;

  /**
   * Initialize character value lookup
   */
  function initCharValues() {
    if (CHAR_VALUES) return;
    CHAR_VALUES = {};
    for (let i = 0; i < ALPHABET.length; i++) {
      CHAR_VALUES[ALPHABET[i]] = i;
    }
  }

  /**
   * Convert decimal number to base-60 string
   * @param {number} decimal - The decimal number to convert
   * @param {number} precision - Fractional digit precision (default: 6)
   * @returns {string} Base-60 representation
   */
  function fromDecimal(decimal, precision = 6) {
    if (decimal === 0) return '0';
    if (!Number.isFinite(decimal)) return 'NaN';

    const negative = decimal < 0;
    decimal = Math.abs(decimal);

    // Split into integer and fractional parts
    let intPart = Math.floor(decimal);
    let fracPart = decimal - intPart;

    // Convert integer part
    let intResult = '';
    if (intPart === 0) {
      intResult = '0';
    } else {
      while (intPart > 0) {
        intResult = ALPHABET[intPart % 60] + intResult;
        intPart = Math.floor(intPart / 60);
      }
    }

    // Convert fractional part
    let fracResult = '';
    if (fracPart > 0 && precision > 0) {
      for (let i = 0; i < precision && fracPart > 1e-10; i++) {
        fracPart *= 60;
        const digit = Math.floor(fracPart);
        fracResult += ALPHABET[digit];
        fracPart -= digit;
      }
      // Remove trailing zeros
      fracResult = fracResult.replace(/0+$/, '');
    }

    let result = intResult;
    if (fracResult) {
      result += '.' + fracResult;
    }

    return negative ? '-' + result : result;
  }

  /**
   * Convert base-60 string to decimal number
   * @param {string} sexagesimal - Base-60 string
   * @returns {number} Decimal value
   */
  function toDecimal(sexagesimal) {
    initCharValues();

    if (!sexagesimal || sexagesimal === 'NaN') return NaN;

    const negative = sexagesimal.startsWith('-');
    if (negative) sexagesimal = sexagesimal.slice(1);

    const [intPart, fracPart] = sexagesimal.split('.');

    // Convert integer part
    let result = 0;
    for (let i = 0; i < intPart.length; i++) {
      const charVal = CHAR_VALUES[intPart[i]];
      if (charVal === undefined) return NaN;
      result = result * 60 + charVal;
    }

    // Convert fractional part
    if (fracPart) {
      let divisor = 60;
      for (let i = 0; i < fracPart.length; i++) {
        const charVal = CHAR_VALUES[fracPart[i]];
        if (charVal === undefined) return NaN;
        result += charVal / divisor;
        divisor *= 60;
      }
    }

    return negative ? -result : result;
  }

  /**
   * Clean fractions in base-60 (no infinite decimals)
   */
  const CLEAN_FRACTIONS = {
    '1/2': { base60: '30', decimal: 30 },
    '1/3': { base60: '20', decimal: 20 },
    '2/3': { base60: '40', decimal: 40 },
    '1/4': { base60: 'F', decimal: 15 },
    '3/4': { base60: '2D', decimal: 45 },
    '1/5': { base60: 'C', decimal: 12 },
    '1/6': { base60: 'A', decimal: 10 },
    '5/6': { base60: '32', decimal: 50 },
    '1/10': { base60: '6', decimal: 6 },
    '1/12': { base60: '5', decimal: 5 },
    '1/15': { base60: '4', decimal: 4 },
    '1/20': { base60: '3', decimal: 3 },
    '1/30': { base60: '2', decimal: 2 }
  };

  /**
   * Check if fraction divides cleanly in base-60
   * @param {number} numerator
   * @param {number} denominator
   * @returns {boolean}
   */
  function isCleanDivision(numerator, denominator) {
    return 60 % denominator === 0;
  }

  /**
   * Base-60 arithmetic operations
   */
  function add(a, b) {
    return fromDecimal(toDecimal(a) + toDecimal(b));
  }

  function subtract(a, b) {
    return fromDecimal(toDecimal(a) - toDecimal(b));
  }

  function multiply(a, b) {
    return fromDecimal(toDecimal(a) * toDecimal(b));
  }

  function divide(a, b) {
    return fromDecimal(toDecimal(a) / toDecimal(b));
  }

  /**
   * Circle/Angle operations (native to base-60)
   */
  const circle = {
    FULL_ROTATION: 360,

    /**
     * Convert degrees to DMS (Degrees, Minutes, Seconds)
     * This IS base-60 representation
     */
    toDMS(degrees) {
      const d = Math.floor(degrees);
      const mFloat = (degrees - d) * 60;
      const m = Math.floor(mFloat);
      const s = (mFloat - m) * 60;

      return {
        degrees: d,
        minutes: m,
        seconds: Math.round(s * 1000) / 1000,
        notation: `${d}°${m}'${s.toFixed(2)}"`
      };
    },

    /**
     * Convert DMS to decimal degrees
     */
    fromDMS(d, m = 0, s = 0) {
      return d + m / 60 + s / 3600;
    },

    /**
     * Divide circle into n parts
     */
    divide(n) {
      return 360 / n;
    }
  };

  /**
   * Frequency/Wave operations
   */
  const frequency = {
    /**
     * Solfeggio frequencies with base-60 representation
     */
    SOLFEGGIO: {
      396: { name: 'Liberation', base60: '6.36', ratio: 6.6 },
      417: { name: 'Change', base60: '6.57', ratio: 6.95 },
      528: { name: 'DNA Repair', base60: '8.48', ratio: 8.8 },
      639: { name: 'Connection', base60: 'A.39', ratio: 10.65 },
      741: { name: 'Expression', base60: 'C.21', ratio: 12.35 },
      852: { name: 'Intuition', base60: 'E.12', ratio: 14.2 },
      963: { name: 'Unity', base60: 'G.03', ratio: 16.05 }
    },

    /**
     * Convert Hz to base-60 (relative to 60Hz base)
     */
    toBase60(hz) {
      return fromDecimal(hz / 60);
    },

    /**
     * Convert base-60 to Hz
     */
    toHz(base60) {
      return toDecimal(base60) * 60;
    },

    /**
     * Get nearest Solfeggio frequency
     */
    nearestSolfeggio(hz) {
      const freqs = Object.keys(this.SOLFEGGIO).map(Number);
      let nearest = freqs[0];
      let minDiff = Math.abs(hz - nearest);

      for (const f of freqs) {
        const diff = Math.abs(hz - f);
        if (diff < minDiff) {
          minDiff = diff;
          nearest = f;
        }
      }

      return { frequency: nearest, ...this.SOLFEGGIO[nearest] };
    }
  };

  /**
   * Tesla 3-6-9 pattern operations
   */
  const tesla = {
    // 3, 6, 9 are key divisors of 60
    pattern: [3, 6, 9],

    /**
     * Check if number aligns with 3-6-9 pattern
     */
    isAligned(n) {
      const sum = this.digitSum(n);
      return sum === 3 || sum === 6 || sum === 9;
    },

    /**
     * Calculate digit sum (recursive until single digit)
     */
    digitSum(n) {
      n = Math.abs(Math.floor(n));
      while (n > 9) {
        n = n.toString().split('').reduce((a, b) => a + parseInt(b), 0);
      }
      return n;
    },

    /**
     * Generate Tesla sequence
     */
    sequence(length = 9) {
      const seq = [];
      for (let i = 1; i <= length; i++) {
        seq.push(i * 3);
        seq.push(i * 6);
        seq.push(i * 9);
      }
      return seq;
    }
  };

  // Public API
  return {
    VERSION: '1.0.0',
    ALPHABET,

    // Core conversion
    fromDecimal,
    toDecimal,

    // Arithmetic
    add,
    subtract,
    multiply,
    divide,

    // Clean fractions
    CLEAN_FRACTIONS,
    isCleanDivision,

    // Specialized
    circle,
    frequency,
    tesla
  };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlyphBase60;
}
if (typeof window !== 'undefined') {
  window.GlyphBase60 = GlyphBase60;
}
```

---

## FILE 2: `/js/glyph/glyph-symbols.js`

```javascript
/**
 * GLYPH SYMBOL REGISTRY
 * Version: 1.0.0
 *
 * Unicode symbol mappings for GLYPH notation.
 * Full symbol space for consciousness/pattern representation.
 */

const GlyphSymbols = (function() {
  'use strict';

  /**
   * Core GLYPH notation symbols
   */
  const CORE = {
    // Structural
    CONTAINER: '\u27D0',      // ⟐ - Boundary/Container (start/end of notation)
    INFINITY: '\u221E',       // ∞ - Recursion/Infinite depth
    OMEGA: '\u03A9',          // Ω - Completion/Termination
    ALPHA: '\u0391',          // Α - Beginning/Origin

    // Flow/Junction
    JUNCTION: '\u29EB',       // ⧫ - Decision point (lozenge)
    TEMPORAL: '\u29D7',       // ⧗ - Time-dependent
    CYCLE: '\u21BB',          // ↻ - Feedback loop/Return
    ADAPTIVE: '\u2646',       // ♆ - Fluid/Variable element

    // Logic
    THEREFORE: '\u2234',      // ∴ - Consequence/Therefore
    BECAUSE: '\u2235',        // ∵ - Because/Since
    AND: '\u2227',            // ∧ - Logical AND
    OR: '\u2228',             // ∨ - Logical OR
    NOT: '\u00AC',            // ¬ - Negation
    IMPLIES: '\u21D2',        // ⇒ - Implies
    IFF: '\u21D4',            // ⇔ - If and only if
    EQUIVALENT: '\u2261',     // ≡ - Equivalent

    // Arrows
    RIGHT: '\u2192',          // →
    LEFT: '\u2190',           // ←
    UP: '\u2191',             // ↑
    DOWN: '\u2193',           // ↓
    BIDIRECTIONAL: '\u2194',  // ↔
    TURN: '\u21B1'            // ↱ - 15-degree turn marker
  };

  /**
   * Mathematical symbols
   */
  const MATH = {
    INTEGRAL: '\u222B',       // ∫
    PARTIAL: '\u2202',        // ∂
    NABLA: '\u2207',          // ∇ - Gradient
    SUM: '\u2211',            // Σ
    PRODUCT: '\u220F',        // Π
    SQRT: '\u221A',           // √
    PROPORTIONAL: '\u221D',   // ∝
    APPROX: '\u2248',         // ≈
    NOTEQUAL: '\u2260',       // ≠
    LESSTHAN: '\u003C',       // <
    GREATERTHAN: '\u003E',    // >
    PLUSMINUS: '\u00B1'       // ±
  };

  /**
   * Geometric symbols
   */
  const GEOMETRY = {
    TRIANGLE: '\u25B3',       // △
    TRIANGLE_FILLED: '\u25B2',// ▲
    SQUARE: '\u25A1',         // □
    SQUARE_FILLED: '\u25A0',  // ■
    CIRCLE: '\u25CB',         // ○
    CIRCLE_FILLED: '\u25CF',  // ●
    DIAMOND: '\u25C7',        // ◇
    DIAMOND_FILLED: '\u25C6', // ◆
    HEXAGON: '\u2B21',        // ⬡
    STAR: '\u2605',           // ★
    STAR_OPEN: '\u2606'       // ☆
  };

  /**
   * Pattern Theory symbols
   */
  const PATTERNS = {
    // Truth/Deceit
    TRUTH: '\u2713',          // ✓ - Checkmark
    DECEIT: '\u2717',         // ✗ - X mark
    QUESTION: '\u2047',       // ⁇ - Double question

    // Builder/Destroyer
    BUILDER: '\u2302',        // ⌂ - House/Build
    DESTROYER: '\u2620',      // ☠ - Skull/Destroy

    // Consciousness
    CONSCIOUSNESS: '\u2609',  // ☉ - Sun
    AWARENESS: '\u263C',      // ☼ - Sun with rays
    AWAKENING: '\u2600',      // ☀ - Black sun

    // Emotional
    POSITIVE: '\u263A',       // ☺ - Smile
    NEGATIVE: '\u2639',       // ☹ - Frown
    NEUTRAL: '\u25CB',        // ○ - Circle

    // Warning
    WARNING: '\u26A0',        // ⚠
    DANGER: '\u2620',         // ☠
    ALERT: '\u26A1'           // ⚡
  };

  /**
   * Domain symbols (7 Domains)
   */
  const DOMAINS = {
    COMMAND: { symbol: '\u2318', number: 1, color: '#FFD700' },    // ⌘
    BUILD: { symbol: '\u2692', number: 2, color: '#00FF00' },      // ⚒
    CONNECT: { symbol: '\u260E', number: 3, color: '#00FFFF' },    // ☎
    PROTECT: { symbol: '\u2694', number: 4, color: '#FF0000' },    // ⚔
    GROW: { symbol: '\u2697', number: 5, color: '#00AA00' },       // ⚗
    LEARN: { symbol: '\u270F', number: 6, color: '#AA00FF' },      // ✏
    TRANSCEND: { symbol: '\u2609', number: 7, color: '#FFFF00' }   // ☉
  };

  /**
   * Frequency symbols (Solfeggio)
   */
  const FREQUENCIES = {
    396: { symbol: '\u266D', name: 'Liberation' },   // ♭
    417: { symbol: '\u266E', name: 'Change' },       // ♮
    528: { symbol: '\u266F', name: 'DNA Repair' },   // ♯
    639: { symbol: '\u2669', name: 'Connection' },   // ♩
    741: { symbol: '\u266A', name: 'Expression' },   // ♪
    852: { symbol: '\u266B', name: 'Intuition' },    // ♫
    963: { symbol: '\u266C', name: 'Unity' }         // ♬
  };

  /**
   * Greek letters for coordinate notation
   */
  const GREEK = {
    alpha: '\u03B1',   // α
    beta: '\u03B2',    // β
    gamma: '\u03B3',   // γ
    delta: '\u03B4',   // δ
    epsilon: '\u03B5', // ε
    zeta: '\u03B6',    // ζ
    eta: '\u03B7',     // η
    theta: '\u03B8',   // θ
    iota: '\u03B9',    // ι
    kappa: '\u03BA',   // κ
    lambda: '\u03BB',  // λ
    mu: '\u03BC',      // μ
    nu: '\u03BD',      // ν
    xi: '\u03BE',      // ξ
    omicron: '\u03BF', // ο
    pi: '\u03C0',      // π
    rho: '\u03C1',     // ρ
    sigma: '\u03C3',   // σ
    tau: '\u03C4',     // τ
    upsilon: '\u03C5', // υ
    phi: '\u03C6',     // φ
    chi: '\u03C7',     // χ
    psi: '\u03C8',     // ψ
    omega: '\u03C9'    // ω
  };

  /**
   * Get symbol by category and name
   */
  function get(category, name) {
    const categories = { CORE, MATH, GEOMETRY, PATTERNS, DOMAINS, FREQUENCIES, GREEK };
    const cat = categories[category.toUpperCase()];
    if (!cat) return null;
    return cat[name.toUpperCase()] || cat[name.toLowerCase()] || null;
  }

  /**
   * Render symbol with optional styling
   */
  function render(symbol, options = {}) {
    const {
      color = 'inherit',
      size = '1em',
      className = ''
    } = options;

    const span = document.createElement('span');
    span.textContent = symbol;
    span.style.color = color;
    span.style.fontSize = size;
    if (className) span.className = className;

    return span;
  }

  /**
   * Get HTML string for symbol
   */
  function toHTML(symbol, options = {}) {
    const { color = 'inherit', size = '1em', className = '' } = options;
    const classAttr = className ? ` class="${className}"` : '';
    return `<span style="color:${color};font-size:${size}"${classAttr}>${symbol}</span>`;
  }

  /**
   * Get all symbols as flat object
   */
  function getAll() {
    return { ...CORE, ...MATH, ...GEOMETRY, ...PATTERNS };
  }

  // Public API
  return {
    VERSION: '1.0.0',

    // Symbol categories
    CORE,
    MATH,
    GEOMETRY,
    PATTERNS,
    DOMAINS,
    FREQUENCIES,
    GREEK,

    // Methods
    get,
    render,
    toHTML,
    getAll
  };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlyphSymbols;
}
if (typeof window !== 'undefined') {
  window.GlyphSymbols = GlyphSymbols;
}
```

---

## FILE 3: `/js/glyph/glyph-patterns.js`

```javascript
/**
 * GLYPH PATTERN THEORY ENGINE
 * Version: 1.0.0
 *
 * Detects Builder vs Destroyer patterns.
 * Maps patterns to GLYPH symbols.
 * Scores consciousness levels.
 */

const GlyphPatterns = (function() {
  'use strict';

  // Get dependencies if available
  const Symbols = typeof GlyphSymbols !== 'undefined' ? GlyphSymbols : null;
  const Base60 = typeof GlyphBase60 !== 'undefined' ? GlyphBase60 : null;

  /**
   * Pattern catalogs
   */
  const TRUTH_MARKERS = [
    { text: 'because', weight: 1.2 },
    { text: 'therefore', weight: 1.2 },
    { text: 'evidence', weight: 1.5 },
    { text: 'research', weight: 1.3 },
    { text: 'data', weight: 1.3 },
    { text: 'permanent', weight: 1.4 },
    { text: 'foundation', weight: 1.4 },
    { text: 'long-term', weight: 1.5 },
    { text: 'quality', weight: 1.3 },
    { text: 'let me explain', weight: 1.2 },
    { text: 'in my experience', weight: 1.1 },
    { text: 'here\'s why', weight: 1.2 },
    { text: 'the reason is', weight: 1.2 },
    { text: 'consider this', weight: 1.1 },
    { text: 'it seems', weight: 1.0 },
    { text: 'from my perspective', weight: 1.0 }
  ];

  const DECEIT_MARKERS = [
    { text: 'but', weight: 1.5 },
    { text: 'however', weight: 1.4 },
    { text: 'actually', weight: 1.2 },
    { text: 'trust me', weight: 2.0 },
    { text: 'believe me', weight: 2.0 },
    { text: 'obviously', weight: 1.3 },
    { text: 'clearly', weight: 1.2 },
    { text: 'everyone knows', weight: 1.8 },
    { text: 'you should', weight: 1.3 },
    { text: 'you must', weight: 1.5 },
    { text: 'you need to', weight: 1.4 },
    { text: 'just', weight: 1.0 },
    { text: 'only', weight: 1.0 },
    { text: 'simple', weight: 1.1 },
    { text: 'easy', weight: 1.0 },
    { text: 'quick', weight: 1.2 },
    { text: 'free', weight: 1.3 },
    { text: 'guaranteed', weight: 1.8 },
    { text: 'limited time', weight: 2.0 },
    { text: 'act now', weight: 2.0 },
    { text: 'don\'t miss', weight: 1.5 },
    { text: 'exclusive', weight: 1.4 },
    { text: 'secret', weight: 1.5 }
  ];

  const MANIPULATION_PATTERNS = {
    gaslighting: {
      markers: ['you\'re crazy', 'that never happened', 'you\'re imagining', 'you\'re too sensitive', 'you\'re overreacting'],
      weight: 2.5,
      description: 'Reality denial to undermine confidence'
    },
    love_bombing: {
      markers: ['you\'re perfect', 'soul mate', 'never felt this way', 'meant to be', 'destiny'],
      weight: 2.0,
      description: 'Excessive flattery to create dependency'
    },
    triangulation: {
      markers: ['my ex', 'other people think', 'everyone says', 'compared to'],
      weight: 1.8,
      description: 'Using third party to manipulate'
    },
    future_faking: {
      markers: ['someday', 'when things calm down', 'i promise', 'we\'ll see', 'eventually'],
      weight: 1.7,
      description: 'False promises to maintain control'
    },
    silent_treatment: {
      markers: ['won\'t respond', 'ignoring', 'not talking', 'shutting down'],
      weight: 1.6,
      description: 'Withdrawal as punishment'
    },
    word_salad: {
      markers: ['circular logic', 'doesn\'t make sense', 'contradictory', 'confusing'],
      weight: 1.5,
      description: 'Confusing language to deflect'
    },
    hoovering: {
      markers: ['i\'ve changed', 'give me another chance', 'i can\'t live without', 'just one more'],
      weight: 1.8,
      description: 'Sucking back into relationship'
    },
    emotional_blackmail: {
      markers: ['if you loved me', 'after all i\'ve done', 'you owe me', 'i\'ll hurt myself'],
      weight: 2.2,
      description: 'Using fear/obligation/guilt'
    }
  };

  const FIFTEEN_DEGREE_TURNS = [
    { text: 'but', symbol: '\u21B1', description: 'Pivot after agreement' },
    { text: 'however', symbol: '\u21B1', description: 'Contradiction follows' },
    { text: 'although', symbol: '\u21B3', description: 'Qualification incoming' },
    { text: 'yes, but', symbol: '\u21BA', description: 'Agreement negation' },
    { text: 'i agree, however', symbol: '\u21BA', description: 'False agreement' }
  ];

  /**
   * Analyze text for patterns
   * @param {string} text - Text to analyze
   * @param {Object} options - Analysis options
   * @returns {Object} Analysis result
   */
  function analyze(text, options = {}) {
    const lower = text.toLowerCase();
    const result = {
      text: text.substring(0, 100) + (text.length > 100 ? '...' : ''),
      timestamp: Date.now(),
      patterns: {
        truth: [],
        deceit: [],
        turns: [],
        manipulation: []
      },
      scores: {
        truth: 0,
        deceit: 0,
        ratio: '0:0'
      },
      dominant: 'neutral',
      confidence: 0,
      glyphNotation: '',
      frequency: 528 // Default to DNA repair frequency
    };

    let truthWeight = 0;
    let deceitWeight = 0;

    // Scan for truth markers
    for (const marker of TRUTH_MARKERS) {
      if (lower.includes(marker.text)) {
        truthWeight += marker.weight;
        result.patterns.truth.push({
          marker: marker.text,
          weight: marker.weight
        });
      }
    }

    // Scan for deceit markers
    for (const marker of DECEIT_MARKERS) {
      if (lower.includes(marker.text)) {
        deceitWeight += marker.weight;
        result.patterns.deceit.push({
          marker: marker.text,
          weight: marker.weight
        });
      }
    }

    // Detect 15-degree turns
    for (const turn of FIFTEEN_DEGREE_TURNS) {
      if (lower.includes(turn.text)) {
        deceitWeight += 0.5; // Small penalty for turns
        result.patterns.turns.push({
          marker: turn.text,
          symbol: turn.symbol,
          description: turn.description
        });
      }
    }

    // Detect manipulation patterns if requested
    if (options.detectManipulation !== false) {
      for (const [name, pattern] of Object.entries(MANIPULATION_PATTERNS)) {
        const found = pattern.markers.filter(m => lower.includes(m));
        if (found.length > 0) {
          deceitWeight += pattern.weight * found.length;
          result.patterns.manipulation.push({
            type: name,
            markers: found,
            weight: pattern.weight,
            description: pattern.description
          });
        }
      }
    }

    // Calculate scores
    const total = truthWeight + deceitWeight;
    if (total > 0) {
      result.scores.truth = Math.round((truthWeight / total) * 100);
      result.scores.deceit = Math.round((deceitWeight / total) * 100);
    } else {
      result.scores.truth = 50;
      result.scores.deceit = 50;
    }

    // Determine dominant pattern
    if (result.scores.truth > result.scores.deceit + 10) {
      result.dominant = 'truth';
      result.frequency = 528; // DNA Repair
    } else if (result.scores.deceit > result.scores.truth + 10) {
      result.dominant = 'deceit';
      result.frequency = 396; // Liberation from fear
    } else {
      result.dominant = 'neutral';
      result.frequency = 417; // Change
    }

    // Calculate confidence
    result.confidence = Math.abs(result.scores.truth - result.scores.deceit);

    // Generate ratio
    const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
    const divisor = gcd(result.scores.truth, result.scores.deceit) || 1;
    result.scores.ratio = `${Math.round(result.scores.truth / divisor)}:${Math.round(result.scores.deceit / divisor)}`;

    // Generate GLYPH notation
    result.glyphNotation = generateNotation(result);

    return result;
  }

  /**
   * Generate GLYPH notation from analysis
   */
  function generateNotation(analysis) {
    const S = Symbols ? Symbols.PATTERNS : {
      TRUTH: '\u2713',
      DECEIT: '\u2717',
      CONSCIOUSNESS: '\u2609'
    };
    const C = Symbols ? Symbols.CORE : {
      CONTAINER: '\u27D0',
      RIGHT: '\u2192'
    };

    const mainSymbol = analysis.dominant === 'truth' ? S.TRUTH :
                       analysis.dominant === 'deceit' ? S.DECEIT :
                       S.CONSCIOUSNESS;

    const turnSymbols = analysis.patterns.turns.map(t => t.symbol).join('');
    const manipCount = analysis.patterns.manipulation.length;

    let notation = `${C.CONTAINER}${mainSymbol}:${analysis.scores.truth}`;

    if (turnSymbols) {
      notation += `:${turnSymbols}`;
    }

    if (manipCount > 0) {
      notation += `:M${manipCount}`;
    }

    notation += `${C.RIGHT}${analysis.frequency}Hz${C.CONTAINER}`;

    return notation;
  }

  /**
   * Quick check for manipulation
   */
  function isManipulation(text) {
    const lower = text.toLowerCase();
    for (const pattern of Object.values(MANIPULATION_PATTERNS)) {
      if (pattern.markers.some(m => lower.includes(m))) {
        return true;
      }
    }
    return false;
  }

  /**
   * Get consciousness level from score
   */
  function getConsciousnessLevel(truthScore) {
    if (truthScore >= 86) return { level: 'Elevated', range: '86-100', description: 'Full pattern mastery' };
    if (truthScore >= 76) return { level: 'Conscious', range: '76-85', description: 'Pattern immunity developing' };
    if (truthScore >= 51) return { level: 'Aware', range: '51-75', description: 'Seeing patterns' };
    if (truthScore >= 26) return { level: 'Awakening', range: '26-50', description: 'Starting to question' };
    return { level: 'Unconscious', range: '0-25', description: 'Reactive, manipulable' };
  }

  /**
   * Score text for specific domain
   */
  function scoreDomain(text, domainNumber) {
    const analysis = analyze(text);
    return {
      domain: domainNumber,
      consciousness: analysis.scores.truth,
      pattern: analysis.dominant,
      notation: analysis.glyphNotation
    };
  }

  // Public API
  return {
    VERSION: '1.0.0',

    // Catalogs
    TRUTH_MARKERS,
    DECEIT_MARKERS,
    MANIPULATION_PATTERNS,
    FIFTEEN_DEGREE_TURNS,

    // Methods
    analyze,
    isManipulation,
    getConsciousnessLevel,
    scoreDomain,
    generateNotation
  };
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlyphPatterns;
}
if (typeof window !== 'undefined') {
  window.GlyphPatterns = GlyphPatterns;
}
```

---

## FILE 4: `/js/glyph/glyph-core.js`

```javascript
/**
 * GLYPH CORE - Main Orchestrator
 * Version: 1.0.0
 *
 * 12D+ Recursive Coordinate Language System
 * Imports and orchestrates all GLYPH modules.
 */

const GlyphCore = (function() {
  'use strict';

  // Get dependencies
  const Base60 = typeof GlyphBase60 !== 'undefined' ? GlyphBase60 : null;
  const Symbols = typeof GlyphSymbols !== 'undefined' ? GlyphSymbols : null;
  const Patterns = typeof GlyphPatterns !== 'undefined' ? GlyphPatterns : null;

  // 6 dimensional axes (cube piercing lines)
  const AXES = ['A', 'B', 'C', 'D', 'E', 'F'];

  // Axis meanings
  const AXIS_MEANINGS = {
    A: { name: 'Vertical', positive: 'Up', negative: 'Down' },
    B: { name: 'Horizontal', positive: 'Right', negative: 'Left' },
    C: { name: 'Depth', positive: 'Front', negative: 'Back' },
    D: { name: 'Temporal', positive: 'Future', negative: 'Past' },
    E: { name: 'Energy', positive: 'Potential', negative: 'Kinetic' },
    F: { name: 'Observer', positive: 'Subject', negative: 'Object' }
  };

  /**
   * Create a GLYPH coordinate
   */
  function createCoordinate(values = {}, origin = 'O', operator = 'USER') {
    const coord = {
      A: values.A ?? 0,
      B: values.B ?? 0,
      C: values.C ?? 0,
      D: values.D ?? 0,
      E: values.E ?? 0,
      F: values.F ?? 0,
      origin,
      operator,
      depth: values.depth ?? 0,
      timestamp: Date.now()
    };

    // Add methods
    coord.toNotation = function() {
      return formatNotation(this);
    };

    coord.toBase60 = function() {
      return coordinateToBase60(this);
    };

    coord.magnitude = function() {
      return Math.sqrt(
        this.A ** 2 + this.B ** 2 + this.C ** 2 +
        this.D ** 2 + this.E ** 2 + this.F ** 2
      );
    };

    return coord;
  }

  /**
   * Format coordinate as GLYPH notation
   */
  function formatNotation(coord) {
    const S = Symbols ? Symbols.CORE : {
      CONTAINER: '\u27D0',
      RIGHT: '\u2192'
    };

    const axes = AXES.map(axis => {
      const val = coord[axis];
      if (typeof val === 'object' && val !== null && val.A !== undefined) {
        return `${axis}[${formatNotation(val)}]`;
      }
      return `${axis}:${val}`;
    }).join(':');

    return `${S.CONTAINER}${axes}${S.RIGHT}${coord.origin}${S.RIGHT}${coord.operator}${S.CONTAINER}`;
  }

  /**
   * Convert coordinate to base-60 representation
   */
  function coordinateToBase60(coord) {
    if (!Base60) {
      console.warn('GlyphBase60 not loaded');
      return null;
    }

    const result = {};
    for (const axis of AXES) {
      const val = coord[axis];
      if (typeof val === 'number') {
        result[axis] = Base60.fromDecimal(val);
      }
    }
    result.origin = coord.origin;
    result.operator = coord.operator;
    return result;
  }

  /**
   * Calculate 6D distance between coordinates
   */
  function distance(coord1, coord2) {
    let sum = 0;
    for (const axis of AXES) {
      const v1 = typeof coord1[axis] === 'number' ? coord1[axis] : 0;
      const v2 = typeof coord2[axis] === 'number' ? coord2[axis] : 0;
      sum += (v2 - v1) ** 2;
    }
    return Math.sqrt(sum);
  }

  /**
   * Interpolate between coordinates
   */
  function interpolate(coord1, coord2, t) {
    const result = {};
    for (const axis of AXES) {
      const v1 = typeof coord1[axis] === 'number' ? coord1[axis] : 0;
      const v2 = typeof coord2[axis] === 'number' ? coord2[axis] : 0;
      result[axis] = v1 + (v2 - v1) * t;
    }
    return createCoordinate(result, coord1.origin, coord1.operator);
  }

  /**
   * Create coordinate from consciousness level
   */
  function fromConsciousnessLevel(level) {
    return createCoordinate({
      A: level * 0.6,                     // Awareness
      B: Math.sin(level * 0.0314) * 50,   // Balance (wave)
      C: level > 50 ? level - 50 : 0,     // Clarity
      D: Date.now() % 60,                 // Temporal
      E: level * 0.4,                     // Energy
      F: 1                                // Observer present
    }, 'CONSCIOUSNESS', 'SYSTEM');
  }

  /**
   * Map to 6-point oscillator (quantum computing pattern)
   */
  function toOscillatorState(coord) {
    return {
      point1: Math.floor(Math.abs(coord.A)) % 60,
      point2: Math.floor(Math.abs(coord.B)) % 60,
      point3: Math.floor(Math.abs(coord.C)) % 60,
      point4: Math.floor(Math.abs(coord.D)) % 60,
      point5: Math.floor(Math.abs(coord.E)) % 60,
      point6: Math.floor(Math.abs(coord.F)) % 60,
      totalState: (Math.abs(coord.A + coord.B + coord.C + coord.D + coord.E + coord.F)) % 360
    };
  }

  /**
   * Unified API object
   */
  const GLYPH = {
    VERSION: '1.0.0',

    // Modules (available if loaded)
    base60: Base60,
    symbols: Symbols,
    patterns: Patterns,

    // Coordinate system
    coordinates: {
      AXES,
      AXIS_MEANINGS,
      create: createCoordinate,
      distance,
      interpolate,
      fromConsciousnessLevel,
      toOscillatorState,
      toNotation: formatNotation,
      toBase60: coordinateToBase60
    },

    // Quick access methods
    analyze: function(text, options) {
      if (!Patterns) {
        console.warn('GlyphPatterns not loaded');
        return null;
      }
      return Patterns.analyze(text, options);
    },

    toBase60: function(decimal) {
      if (!Base60) {
        console.warn('GlyphBase60 not loaded');
        return null;
      }
      return Base60.fromDecimal(decimal);
    },

    fromBase60: function(sexagesimal) {
      if (!Base60) {
        console.warn('GlyphBase60 not loaded');
        return null;
      }
      return Base60.toDecimal(sexagesimal);
    },

    getSymbol: function(category, name) {
      if (!Symbols) {
        console.warn('GlyphSymbols not loaded');
        return null;
      }
      return Symbols.get(category, name);
    },

    // Initialization check
    init: function() {
      const status = {
        version: this.VERSION,
        modules: {
          base60: !!Base60,
          symbols: !!Symbols,
          patterns: !!Patterns
        },
        ready: !!Base60 && !!Symbols && !!Patterns
      };

      console.log('GLYPH initialized:', status);
      return status;
    }
  };

  return GLYPH;
})();

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GlyphCore;
}
if (typeof window !== 'undefined') {
  window.GLYPH = GlyphCore;
  window.GlyphCore = GlyphCore;
}
```

---

## FILE 5: `/js/glyph/index.js`

```javascript
/**
 * GLYPH Module Index
 * Load all GLYPH modules in correct order
 */

// Note: For ES modules, use this pattern:
// import { GlyphBase60 } from './glyph-base60.js';
// import { GlyphSymbols } from './glyph-symbols.js';
// import { GlyphPatterns } from './glyph-patterns.js';
// import { GlyphCore } from './glyph-core.js';

// For script tag loading, ensure order:
// 1. glyph-base60.js
// 2. glyph-symbols.js
// 3. glyph-patterns.js
// 4. glyph-core.js

// This file provides a single entry point
if (typeof window !== 'undefined') {
  window.GLYPH_MODULES = {
    loaded: function() {
      return {
        base60: typeof GlyphBase60 !== 'undefined',
        symbols: typeof GlyphSymbols !== 'undefined',
        patterns: typeof GlyphPatterns !== 'undefined',
        core: typeof GlyphCore !== 'undefined' || typeof GLYPH !== 'undefined'
      };
    },

    init: function() {
      const status = this.loaded();
      console.log('GLYPH Modules:', status);

      if (typeof GLYPH !== 'undefined') {
        return GLYPH.init();
      }

      return status;
    }
  };
}

// ES Module exports
export { GlyphBase60 } from './glyph-base60.js';
export { GlyphSymbols } from './glyph-symbols.js';
export { GlyphPatterns } from './glyph-patterns.js';
export { GlyphCore as GLYPH } from './glyph-core.js';
```

---

## USAGE EXAMPLE: Add GLYPH to Any HTML Page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Tool with GLYPH</title>

    <!-- Load GLYPH modules in order -->
    <script src="/js/glyph/glyph-base60.js"></script>
    <script src="/js/glyph/glyph-symbols.js"></script>
    <script src="/js/glyph/glyph-patterns.js"></script>
    <script src="/js/glyph/glyph-core.js"></script>
</head>
<body>
    <textarea id="input" placeholder="Enter text to analyze"></textarea>
    <button onclick="analyzeText()">Analyze</button>
    <pre id="output"></pre>

    <script>
    // Initialize GLYPH on page load
    document.addEventListener('DOMContentLoaded', () => {
        const status = GLYPH.init();
        console.log('GLYPH ready:', status.ready);
    });

    function analyzeText() {
        const text = document.getElementById('input').value;

        // Analyze with GLYPH
        const analysis = GLYPH.analyze(text);

        // Create coordinate from consciousness level
        const coord = GLYPH.coordinates.fromConsciousnessLevel(analysis.scores.truth);

        // Format output
        const output = {
            patterns: analysis.patterns,
            scores: analysis.scores,
            dominant: analysis.dominant,
            glyphNotation: analysis.glyphNotation,
            coordinate: coord.toNotation(),
            base60Score: GLYPH.toBase60(analysis.scores.truth),
            frequency: analysis.frequency + ' Hz',
            consciousnessLevel: GlyphPatterns.getConsciousnessLevel(analysis.scores.truth)
        };

        document.getElementById('output').textContent = JSON.stringify(output, null, 2);
    }
    </script>
    <p style="text-align:center;color:#666;font-family:monospace;margin:40px 0;">Pattern: 3 → 7 → 13 → ∞</p>
</body>
</html>
```

---

## NEXT STEPS (Execution Order)

1. **Create directory:** `mkdir -p C:/Users/dwrek/100X_DEPLOYMENT/js/glyph`

2. **Write files** (in order):
   - `glyph-base60.js`
   - `glyph-symbols.js`
   - `glyph-patterns.js`
   - `glyph-core.js`
   - `index.js`

3. **Test in browser console:**
   ```javascript
   GLYPH.init()
   GLYPH.analyze("Trust me, this is easy and guaranteed!")
   GLYPH.toBase60(528)
   ```

4. **Integrate with Araya:** Add GLYPH context to araya-chat.mjs

5. **Migrate tools:** Add script tags to consciousness-tools.html

---

*Built by C1 Mechanic | Trinity | December 30, 2025*
*⟐∞⧫Ω∴⧗↻⟐*
