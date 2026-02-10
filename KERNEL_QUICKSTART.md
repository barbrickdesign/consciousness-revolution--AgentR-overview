# 🚀 KERNEL Framework Quick Start Guide

Get started with KERNEL prompt engineering for Consciousness Revolution in 5 minutes!

## What You'll Learn

1. What KERNEL is and why it matters for consciousness work
2. How to build your first KERNEL prompt
3. How to use KERNEL with ARAYA, Cyclotron, and pattern detection
4. Quick patterns for common consciousness tasks

---

## 1. What is KERNEL?

KERNEL is a prompt engineering framework with 6 proven principles:

| Principle | Symbol | Meaning |
|-----------|--------|---------|
| **K**eep it Simple | 🎯 | One clear goal |
| **E**asy to Verify | ✅ | Measurable success |
| **R**eproducible | 🔄 | Consistent results |
| **N**arrow Scope | 🎯 | One task only |
| **E**xplicit Constraints | 📋 | What NOT to do |
| **L**ogical Structure | 📐 | Clear sections |

### Why KERNEL for Consciousness Revolution?

Proven results from 1000+ prompts:
- ✅ **94% first-try success** (vs 72% before)
- ✅ **67% faster** to useful results
- ✅ **58% less tokens** used
- ✅ **340% accuracy** improvement

Perfect for:
- Pattern detection prompts
- ARAYA healing guidance
- Domain classification
- Consciousness scoring
- Multi-AI orchestration
---

## 2. Your First KERNEL Prompt

### Bad Prompt (Before KERNEL)
```
Help me detect manipulation patterns in some text
```
Result: Generic, inaccurate detection ❌

### Alternative Bad Example (Generic Code)
```
Help me write a script to process some data files
```
Result: Generic, unusable code ❌

### Good Prompt (After KERNEL)
```
TASK: Detect gaslighting patterns in conversation text

INPUT:
- CSV files in data/ directory
- All files have same columns: id, name, date, value

CONSTRAINTS:
- Python 3.10+
- Use pandas only
- Code under 50 lines
- Handle missing files gracefully

OUTPUT:
- Single merged.csv file
- Remove duplicate IDs (keep latest)
- Print summary: "Merged X files, Y rows"

VERIFY:
- Run: python merge.py
- Test with: test_data/*.csv
- Output should be valid CSV
```
Result: 37 lines, worked on first try ✅

---

## 3. Using KERNEL in This Repository

### Method 1: Interactive Playground (Easiest)

1. Open [kernel-playground.html](kernel-playground.html)
2. Choose a quick pattern or build custom
3. Click "Build Prompt"
4. Click "Validate" to check quality
5. Copy and use!

### Method 2: JavaScript Code (Recommended)

```javascript
// Load KERNEL utilities
const KernelPromptBuilder = window.KernelPromptBuilder;
const builder = new KernelPromptBuilder();

// Build prompt
builder
    .setTask('Generate Python function to validate emails')
    .addInput('Email string as input')
    .addConstraint('Python 3.10+')
    .addConstraint('No external libraries')
    .addOutput('Function returns True/False')
    .addVerification('Test with valid email: returns True');

// Get formatted prompt
const prompt = builder.build();
console.log(prompt);

// Use with OpenAI
const response = await window.openAIOrchestrator.executeKernelPrompt(builder);
```

### Method 3: Quick Patterns (Fastest)

```javascript
// Code generation
const codePrompt = await window.openAIOrchestrator.quickKernel('code', 
    'Create email validator', {
    language: 'Python',
    version: '3.10+'
});

// Documentation
const docsPrompt = await window.openAIOrchestrator.quickKernel('docs',
    'Document auth API');

// Data analysis
const analysisPrompt = await window.openAIOrchestrator.quickKernel('analysis',
    'Analyze sales trends');

// Refactoring
const refactorPrompt = await window.openAIOrchestrator.quickKernel('refactor',
    'Modernize legacy function');
```

---

## 4. Quick Patterns

### Pattern: Code Generation

```
TASK: [Language] [what to create]

INPUT:
- [What function accepts]
- [Expected inputs]

CONSTRAINTS:
- [Language version]
- [No/Only specific libraries]
- [Length limits]
- [Error handling required]

OUTPUT:
- [Function signature]
- [What it returns]
- [Documentation type]

VERIFY:
- [Test case 1]
- [Test case 2]
- [Edge cases]
```

**Example**: See playground → Code Pattern

### Pattern: Documentation

```
TASK: Document [what]

INPUT:
- [What exists]
- [What needs docs]

CONSTRAINTS:
- [Format (Markdown, etc.)]
- [Length limits]
- [Must include examples]

OUTPUT:
- [Sections required]
- [Example format]
- [Code samples]

VERIFY:
- [All sections present]
- [Examples runnable]
```

**Example**: See playground → Documentation Pattern

### Pattern: Data Analysis

```
TASK: Analyze [data] and [what to find]

INPUT:
- [Data format]
- [Data location]
- [Time period]

CONSTRAINTS:
- [Tools allowed]
- [Output format]
- [Visualization requirements]

OUTPUT:
- [File 1: statistics]
- [File 2: visualizations]
- [File 3: insights]

VERIFY:
- [Numbers match source]
- [Visualizations clear]
- [All files generated]
```

**Example**: See playground → Analysis Pattern

---

## 5. KERNEL Checklist

Before using any prompt, check:

- [ ] **Task** is one clear sentence
- [ ] **Input** lists what you're providing
- [ ] **Constraints** include version numbers
- [ ] **Constraints** say what NOT to do
- [ ] **Output** is specific (not "good code")
- [ ] **Verify** has measurable criteria
- [ ] **No** temporal words (current, latest, recent)
- [ ] **Score** is 80+ (use validator)

---

## 6. Common Mistakes

### ❌ Mistake 1: Too Vague
```
Write good code for processing data
```
**Fix**: Be specific about language, data format, processing steps

### ❌ Mistake 2: Multiple Goals
```
Create function AND documentation AND tests AND deploy
```
**Fix**: Split into 4 separate KERNEL prompts

### ❌ Mistake 3: Subjective Criteria
```
Make it look nice and professional
```
**Fix**: Use measurable criteria like "Include 3 code examples"

### ❌ Mistake 4: Temporal References
```
Use the latest React and current best practices
```
**Fix**: Specify "React 18.2" and "React docs 2023"

### ❌ Mistake 5: No Constraints
```
Generate a Python script
```
**Fix**: Add Python version, library limits, length, error handling

---

## 7. KERNEL in Practice

### For AI API Calls

```javascript
// ALWAYS use KERNEL builder
const builder = new KernelPromptBuilder()
    .setTask(/* ... */)
    .addConstraint(/* ... */);

const response = await api.executeKernelPrompt(builder);
```

### For Agent Systems

```javascript
class MyAgent {
    async plan(task) {
        // Build KERNEL prompt
        const builder = new KernelPromptBuilder()
            .setTask(task)
            .addConstraint('Follow repository standards');
        
        return builder.build();
    }
}
```

### For Code Comments

```javascript
// KERNEL: TASK - Validate email format
// INPUT: email (string)
// CONSTRAINTS: Regex only, no external libs
// OUTPUT: boolean (true if valid)
// VERIFY: Test with "test@example.com" returns true
function validateEmail(email) {
    // Implementation...
}
```

---

## 5. General Purpose Patterns

### Pattern: Code Generation

```
TASK: [Language] [what to create]

INPUT:
- [What function accepts]
- [Expected inputs]

CONSTRAINTS:
- [Language version]
- [No/Only specific libraries]
- [Length limits]
- [Error handling required]

OUTPUT:
- [Function signature]
- [What it returns]
- [Documentation type]

VERIFY:
- [Test case 1]
- [Test case 2]
- [Edge cases]
```

**Example**: See playground → Code Pattern

### Pattern: Documentation

```
TASK: Document [what]

INPUT:
- [What exists]
- [What needs docs]

CONSTRAINTS:
- [Format (Markdown, etc.)]
- [Length limits]
- [Must include examples]

OUTPUT:
- [Sections required]
- [Example format]
- [Code samples]

VERIFY:
- [All sections present]
- [Examples runnable]
```

**Example**: See playground → Documentation Pattern

### Pattern: Data Analysis

```
TASK: Analyze [data] and [what to find]

INPUT:
- [Data format]
- [Data location]
- [Time period]

CONSTRAINTS:
- [Tools allowed]
- [Output format]
- [Visualization requirements]

OUTPUT:
- [File 1: statistics]
- [File 2: visualizations]
- [File 3: insights]

VERIFY:
- [Numbers match source]
- [Visualizations clear]
- [All files generated]
```

**Example**: See playground → Analysis Pattern

---

## 6. General KERNEL Checklist

Before using any general prompt, check:

- [ ] **Task** is one clear sentence
- [ ] **Input** lists what you're providing
- [ ] **Constraints** include version numbers
- [ ] **Constraints** say what NOT to do
- [ ] **Output** is specific (not "good code")
- [ ] **Verify** has measurable criteria
- [ ] **No** temporal words (current, latest, recent)
- [ ] **Score** is 80+ (use validator)

---

## 7. Common General Mistakes

### ❌ Mistake 1: Too Vague
```
Write good code for processing data
```
**Fix**: Be specific about language, data format, processing steps

### ❌ Mistake 2: Multiple Goals
```
Create function AND documentation AND tests AND deploy
```
**Fix**: Split into 4 separate KERNEL prompts

### ❌ Mistake 3: Subjective Criteria
```
Make it look nice and professional
```
**Fix**: Use measurable criteria like "Include 3 code examples"

### ❌ Mistake 4: Temporal References
```
Use the latest React and current best practices
```
**Fix**: Specify "React 18.2" and "React docs 2023"

### ❌ Mistake 5: No Constraints
```
Generate a Python script
```
**Fix**: Add Python version, library limits, length, error handling

---

## 8. KERNEL for AI API Calls

### For AI API Calls

```javascript
// ALWAYS use KERNEL builder
const builder = new KernelPromptBuilder()
    .setTask(/* ... */)
    .addConstraint(/* ... */);

const response = await api.executeKernelPrompt(builder);
- Domain must be one of: Command, Creation, Connection, Peace, Abundance, Wisdom, Purpose
- Confidence score 0-1
- Consciousness score 1-100

VERIFY:
- Test: "You're too sensitive" → Peace domain, gaslighting pattern, confidence > 0.7
- Test: Normal conversation → confidence < 0.3
- Test: Multiple patterns → returns highest confidence
- Output is valid JSON
```
Result: Accurate detection, worked on first try ✅

---

## 3. Using KERNEL in Consciousness Revolution

### Method 1: With ARAYA AI Companion

```javascript
// Use KERNEL structure in ARAYA prompts
const kernelPrompt = `
TASK: Provide healing guidance for gaslighting pattern

INPUT:
- Detected pattern: gaslighting
- Domain: Peace
- Confidence: 0.85
- User context: workplace relationship

CONSTRAINTS:
- Use ARAYA_GUIDED_HEALING_FLOWS.json
- Response under 300 words
- Actionable steps only
- No medical/legal advice

OUTPUT:
- 3 specific boundary-setting techniques
- 1 immediate action to take
- 1 long-term practice for Peace domain

VERIFY:
- All advice is actionable
- References Peace domain specifically
- No vague "be yourself" statements
`;

const response = await askARAYA(kernelPrompt, 'Peace');
```

### Method 2: With Pattern Detection

```javascript
// KERNEL prompt for pattern analysis
const detectionPrompt = `
TASK: Analyze text for manipulation patterns

INPUT: "${userText}"

CONSTRAINTS:
- Must use PATTERN_LIBRARY.html patterns
- Classify into 7 Domains
- Minimum confidence threshold: 0.5
- Return top 3 patterns only

OUTPUT:
- Array of {domain, pattern, confidence, excerpt}
- Sorted by confidence (highest first)
- Include specific text matches

VERIFY:
- All patterns from PATTERN_LIBRARY
- All domains valid (7 Domains framework)
- Confidence scores between 0-1
`;

const patterns = await analyzePattern(userText, detectionPrompt);
```

### Method 3: With Cyclotron Search

```python
# KERNEL prompt for semantic indexing
kernel_prompt = """
TASK: Index pattern detection result in Cyclotron

INPUT:
- Pattern: {pattern_data}
- User ID: {user_id}
- Timestamp: {timestamp}
- Domain: {domain}

CONSTRAINTS:
- Use CYCLOTRON_SEMANTIC_API.py
- Create semantic embeddings
- Link to 7 Domains taxonomy
- Index time under 1 second
- Handle duplicates

OUTPUT:
- Cyclotron index ID
- Semantic vector created
- Domain tags added
- Searchable metadata

VERIFY:
- Search for pattern by domain works
- User timeline updated
- No duplicate entries
- Embeddings are valid vectors
"""

index_result = cyclotron_index(kernel_prompt, pattern_data)
```

---

## 4. Quick Patterns for Consciousness Work

### Pattern 1: Manipulation Detection

```
TASK: Detect [specific manipulation type] in text

INPUT:
- Text string (minimum 50 characters)
- Target domain (or "auto-detect")

CONSTRAINTS:
- Use PATTERN_LIBRARY.html
- Python/JavaScript
- No external ML libraries
- Return JSON format

OUTPUT:
- {domain, pattern, confidence, matches, score}
- Domain from 7 Domains framework
- Consciousness score 1-100

VERIFY:
- Test with known examples
- Confidence thresholds work
- Domain classification accurate
```

### Pattern 2: Domain Classification

```
TASK: Classify text into 7 Domains framework

INPUT:
- Text or pattern detection result
- Context (optional)

CONSTRAINTS:
- Must return ONE primary domain
- Can include secondary domains
- Use 7 Domains definitions:
  * Command - Clarity, decisions, structure
  * Creation - Building, projects, skills
  * Connection - Relationships, communication
  * Peace - Security, boundaries, protection
  * Abundance - Financial, business, scaling
  * Wisdom - Learning, critical thinking
  * Purpose - Meaning, meditation, integration

OUTPUT:
- Primary domain (required)
- Secondary domains (optional, max 2)
- Confidence score per domain
- Reasoning (1 sentence)

VERIFY:
- Domain is valid (one of 7)
- Confidence scores sum to 1.0
- Reasoning references domain definition
```

### Pattern 3: ARAYA Healing Guidance

```
TASK: Generate healing guidance for detected pattern

INPUT:
- Pattern type (gaslighting, love bombing, etc.)
- Domain (from 7 Domains)
- User context (relationship type, situation)

CONSTRAINTS:
- Use ARAYA_GUIDED_HEALING_FLOWS.json
- 200-400 words
- 3 actionable steps
- No medical/legal advice
- Age-appropriate (assume adult)

OUTPUT:
- Empathetic acknowledgment (1 sentence)
- Pattern explanation (2 sentences)
- 3 specific action steps
- 1 long-term practice for domain
- Closing affirmation

VERIFY:
- All steps are actionable
- References specific domain
- No vague advice ("be yourself")
- Appropriate tone (supportive, not prescriptive)
```

### Pattern 4: Consciousness Scoring

```
TASK: Score text for consciousness level

INPUT:
- Text to analyze
- Optional: specific domain focus

CONSTRAINTS:
- Use consciousness rubric from ARAYA_SOUL_CORE.json
- Score 1-100 scale
- Must provide reasoning
- Consider: awareness, agency, boundaries, growth

OUTPUT:
- Overall score (1-100)
- Domain-specific scores (1-100 each)
- Breakdown: {awareness, agency, boundaries, growth}
- 2 sentence reasoning

VERIFY:
- Score is 1-100
- Reasoning references specific text
- Domain scores align with overall score
- Breakdown scores average to overall score
```

### Alternative Example: CSV Data Merging

```
TASK: Python script to merge multiple CSV files

INPUT:
- CSV files in data/ directory
- All files have same columns: id, name, date, value

CONSTRAINTS:
- Python 3.10+
- Use pandas only
- Code under 50 lines
- Handle missing files gracefully

OUTPUT:
- Single merged.csv file
- Remove duplicate IDs (keep latest)
- Print summary: "Merged X files, Y rows"

VERIFY:
- Run: python merge.py
- Test with: test_data/*.csv
- Output should be valid CSV
```
Result: 37 lines, worked on first try ✅

---

## 5. KERNEL Checklist for Consciousness Work

Before using any consciousness prompt, check:

- [ ] **Task** mentions specific domain or pattern type
- [ ] **Input** specifies text format and length
- [ ] **Constraints** reference 7 Domains framework
- [ ] **Constraints** specify which patterns to use (PATTERN_LIBRARY.html)
- [ ] **Output** includes domain classification
- [ ] **Output** includes consciousness score or confidence
- [ ] **Verify** tests with known manipulation patterns
- [ ] **No** vague criteria like "accurate" or "good"
- [ ] **Score** is 80+ (use validator)

---

## 6. Common Mistakes in Consciousness Prompts

### ❌ Mistake 1: Too Many Domains
```
Detect patterns across all 7 domains simultaneously
```
**Fix**: Focus on one domain, or use "auto-detect primary domain"

### ❌ Mistake 2: Vague Pattern Types
```
Find any manipulation in the text
```
**Fix**: Specify pattern types from PATTERN_LIBRARY.html

### ❌ Mistake 3: No Consciousness Context
```
Analyze this text for problems
```
**Fix**: Use 7 Domains framework and consciousness scoring

### ❌ Mistake 4: Missing Verification
```
Provide healing guidance for gaslighting
```
**Fix**: Add verification criteria - check advice is actionable, domain-specific, appropriate

### ❌ Mistake 5: Multi-Goal Prompts
```
Detect patterns AND provide guidance AND log to database AND update UI
```
**Fix**: Split into 4 KERNEL prompts, chain them together

### ❌ Mistake 6: Temporal References
```
Use the latest React and current best practices
```
**Fix**: Specify "React 18.2" and "React docs 2023"

---

## 7. KERNEL in Consciousness Revolution Systems

### For Pattern Detection Tools

```javascript
// KERNEL structure in pattern detector
const KERNEL_DETECTOR_PROMPT = {
  task: "Detect specific manipulation pattern",
  input: {text: userText, minLength: 50},
  constraints: [
    "Use PATTERN_LIBRARY.html patterns",
    "Classify into 7 Domains",
    "No external ML libraries",
    "Return JSON format"
  ],
  output: {
    schema: {domain, pattern, confidence, matches, score},
    required: ["domain", "pattern", "confidence"]
  },
  verify: [
    "Test with known gaslighting example",
    "Confidence threshold 0.5-1.0 works",
    "Domain is valid from 7 Domains"
  ]
};
```

### For ARAYA Integration

```python
# KERNEL prompt for ARAYA API
KERNEL_ARAYA_TEMPLATE = """
TASK: {task}

INPUT:
- Pattern: {pattern}
- Domain: {domain}
- User context: {context}

CONSTRAINTS:
- Use ARAYA_GUIDED_HEALING_FLOWS.json
- Follow 7 Domains framework
- Response {min_words}-{max_words} words
- No medical/legal advice

OUTPUT:
- Healing guidance with 3 steps
- Domain-specific practices
- Empathetic tone

VERIFY:
- All steps actionable
- References {domain} specifically
- Appropriate for {context}
"""
```

### For Multi-AI Orchestration

```javascript
// KERNEL with multi-AI fallback
const kernelPromptWithFallback = async (task, constraints) => {
  const prompt = buildKernelPrompt(task, constraints);
  
  // Try Groq first (free tier)
  try {
    return await window.aiOrchestrator.groq(prompt);
  } catch {
    // Fallback to OpenAI
    return await window.aiOrchestrator.openai(prompt);
  }
};
```

### For Agent Systems

```javascript
class MyAgent {
    async plan(task) {
        // Build KERNEL prompt
        const builder = new KernelPromptBuilder()
            .setTask(task)
            .addConstraint('Follow repository standards');
        
        return builder.build();
    }
}
```

---

## 8. Measuring Success in Consciousness Work

### Track Your Pattern Detection Accuracy

```javascript
const metrics = {
  firstTrySuccess: 0.94,      // 94% patterns detected correctly
  avgConfidence: 0.82,         // Average confidence score
  avgConsciousnessScore: 67,   // Average consciousness score
  domainAccuracy: 0.91,        // 91% correct domain classification
  falsePositives: 0.06         // 6% false positive rate
};
```

### Target Metrics for Consciousness Tools

| Metric | Target | Current |
|--------|--------|---------|
| Pattern Detection Success | >90% | Track yours |
| Domain Classification Accuracy | >85% | Track yours |
| ARAYA Guidance Actionability | >95% | Track yours |
| User Satisfaction | >4.5/5 | Track yours |
| First-Try Success | >90% | Track yours |
| Token Usage | <300 per prompt | Track yours |
| KERNEL Score | >80 | Track yours |

---

## 9. Resources

### Framework Documentation
- **Full KERNEL Guide**: [KERNEL_FRAMEWORK.md](KERNEL_FRAMEWORK.md)
- **Pattern Library**: [PATTERN_LIBRARY.html](PATTERN_LIBRARY.html)
- **7 Domains Guide**: [seven-domains/](seven-domains/)
- **Interactive Playground**: [kernel-playground.html](kernel-playground.html)

### System Integration
- **ARAYA API**: [ARAYA_UNIFIED_API.py](ARAYA_UNIFIED_API.py)
- **Cyclotron Search**: [CYCLOTRON_SEMANTIC_API.py](CYCLOTRON_SEMANTIC_API.py)
- **Multi-AI Guide**: [MULTI_PROVIDER_AI_GUIDE.md](MULTI_PROVIDER_AI_GUIDE.md)

### Code Tools
- **Code Examples**: See `src/ai/openai-orchestrator.js`
- **Validator**: `src/utils/kernel-validator.js`
- **Builder**: `src/utils/kernel-prompt-builder.js`

### Examples
- **Pattern Detection**: See PATTERN_DETECTOR.py
- **ARAYA Integration**: See ARAYA_INTEGRATION_EXAMPLE.py
- **Domain Classification**: See seven-domains/

---

## 10. Quick Tips for Consciousness Prompts

1. **Always specify domain** - Use 7 Domains framework explicitly
2. **Reference pattern library** - Don't invent new patterns
3. **Include consciousness scoring** - Use 1-100 scale
4. **Verify with known examples** - Test gaslighting, love bombing, etc.
5. **Chain prompts through ARAYA** - One tool → ARAYA → User
6. **Use multi-AI fallback** - Groq → OpenAI → Claude
7. **Track accuracy metrics** - Measure pattern detection success
8. **Keep healing guidance actionable** - No vague "be yourself" advice
9. **Validate always** - Check score before using (aim for 80+)
10. **Start with playground** - Build confidence before coding

---

## Next Steps

1. ✅ Read [KERNEL_FRAMEWORK.md](KERNEL_FRAMEWORK.md) for full details
2. ✅ Review [PATTERN_LIBRARY.html](PATTERN_LIBRARY.html) for pattern types
3. ✅ Test with ARAYA: [ARAYA_QUICK_START.md](ARAYA_QUICK_START.md)
4. ✅ Open [kernel-playground.html](kernel-playground.html) to try patterns
5. ✅ Build a pattern detector using KERNEL structure
6. ✅ Integrate with Cyclotron for semantic search
7. ✅ Track your accuracy metrics

---

## Support

- **Questions?** Join our [Discord](https://discord.gg/xHRXyKkzyg)
- **Issues?** Report via [consciousness-bugs](https://github.com/overkor-tek/consciousness-bugs)
- **Examples?** See pattern detection tools in repository and playground patterns

---

## Credits

KERNEL Framework originally developed by Ryan Barbrick and BarbrickDesign community.

Adapted for Consciousness Revolution to integrate with:
- 7 Domains framework
- ARAYA consciousness AI
- Cyclotron semantic search
- Pattern Theory methodology
- Multi-AI orchestration

---

**Built with ❤️ by the Consciousness Revolution community**

*Last Updated: January 2025*
