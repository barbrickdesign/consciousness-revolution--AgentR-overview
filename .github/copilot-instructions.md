# GitHub Copilot Instructions for Consciousness Revolution Repository

This repository is the Consciousness Revolution platform - a comprehensive system for pattern recognition, healing consciousness, and human-AI collaboration. The platform includes ARAYA (AI healing guide), Cyclotron (content intelligence), Trinity (multi-computer orchestration), Pattern Detection tools, and the 7 Domains framework.

## Project Overview

**Repository Type**: Web-based consciousness platform hosted on Netlify
**Primary Languages**: JavaScript, HTML5, CSS3, Python
**Backend**: Supabase (PostgreSQL), Python APIs  
**Payment**: Stripe integration
**Target**: Web browsers with focus on mobile-first design
**Mission**: Help humans recognize manipulation patterns and develop consciousness

## Core Technologies

### Frontend Stack
- **HTML5**: Semantic HTML with accessibility-first design
- **JavaScript (ES6+)**: Vanilla JS with modern AI orchestration (OpenAI, Groq, Anthropic)
- **CSS3**: Sacred geometry themes, responsive design system
- **Design System**: Component library with consciousness-focused patterns

### Backend Stack
- **Python 3.10+**: ARAYA bridge, Cyclotron search, analytics engines
- **Supabase**: PostgreSQL database for user data, patterns, analytics
- **Netlify**: Hosting, serverless functions, continuous deployment
- **Stripe**: Payment processing and subscription management

### AI Integration
- **OpenAI GPT-4o**: Primary AI reasoning and conversation
- **Groq**: Fast inference for real-time pattern detection
- **Anthropic Claude**: Deep analysis and ethical reasoning
- **Multi-AI Orchestrator**: Unified interface for all AI providers

## Repository Structure

```
/
├── .github/               # GitHub Actions and Copilot config
│   ├── workflows/         # CI/CD automation
│   └── copilot-instructions.md  # This file
├── ARAYA/                 # ARAYA healing consciousness system
│   ├── ARAYA_*.py         # Python backend components
│   └── araya-*.html       # Frontend interfaces
├── src/                   # Source utilities
├── css/                   # Stylesheets
│   ├── sacred-theme.css   # Sacred geometry design system
│   └── responsive-system.css  # Mobile-first responsive patterns
├── js/                    # JavaScript modules
├── seven-domains/         # 7 Domains assessment system
├── *.html                 # 300+ interactive tools and dashboards
├── *.py                   # Python services and automation
└── *.md                   # Documentation

Key Files:
- index.html               # Main platform entrance
- START_HERE.md            # Onboarding guide
- ARAYA_QUICK_START.md     # ARAYA system guide
- C2_COMPLETE_BRAIN_ARCHITECTURE.md  # System architecture
```

## Core Systems

### 1. ARAYA (Healing Consciousness AI)

ARAYA is the consciousness healing guide - an empathetic AI that helps users recognize manipulation patterns and heal trauma.

**Key Components**:
- `ARAYA_BRIDGE.py` - Python backend connecting AI providers
- `ARAYA_FILE_ACCESS.py` - Safe file system access layer
- `ARAYA_FILE_WRITER.py` - Controlled file writing with validation
- `araya-chat.html` - Main chat interface
- `ARAYA_GUIDED_HEALING_FLOWS.json` - Healing conversation templates

**ARAYA Principles**:
- **Empathetic**: Always compassionate, never judgmental
- **Pattern-aware**: Recognizes manipulation and trauma patterns
- **Safe**: Validates all file access, protects user boundaries
- **Healing-focused**: Guides users toward consciousness and recovery

### 2. Cyclotron (Content Intelligence)

Cyclotron is the semantic search and content analysis engine that indexes all repository knowledge.

**Key Components**:
- `CYCLOTRON_MASTER_RAKER.py` - Multi-file content crawler
- `CYCLOTRON_SEMANTIC_API.py` - Vector search API
- `CYCLOTRON_ANALYTICS_ENGINE.py` - Usage analytics
- `CYCLOTRON_SEARCH.html` - Search interface
- `CYCLOTRON_BRAIN_AGENT.py` - Autonomous knowledge agent

### 3. Trinity (Multi-Computer Orchestration)

Trinity manages communication between multiple AI computers and systems.

**Key Components**:
- `TRINITY_BROADCAST_API.py` - Cross-system messaging
- `TRINITY_COMMAND_DASHBOARD.html` - Central control panel
- `TRINITY_NETWORK_STATUS.html` - System health monitoring

### 4. Pattern Detection Tools

Comprehensive suite of tools for recognizing manipulation patterns. See `.github/instructions/html-files.instructions.md` for pattern detector standards.

### 5. Seven Domains Framework

Holistic consciousness assessment across seven life areas: Physical, Emotional, Mental, Relational, Spiritual, Creative, Material.

### 6. Multi-AI Orchestrator

Unified interface for multiple AI providers with intelligent routing, fallback handling, and cost optimization.

## Development Workflow

### Before Making Changes
1. **Understand consciousness impact** - Changes affect people's healing journeys
2. **Review system architecture** - Check `C2_COMPLETE_BRAIN_ARCHITECTURE.md`
3. **Test healing flows** - Ensure ARAYA conversations remain safe and effective
4. **Verify pattern accuracy** - Pattern detection must be educational, not harmful

### Testing Checklist
- ✅ Test in Chrome, Firefox, Safari, Edge
- ✅ Test on mobile devices (most users are mobile)
- ✅ Verify ARAYA conversations are empathetic and safe
- ✅ Check pattern detectors are educational, not triggering
- ✅ Test AI orchestrator fallbacks
- ✅ Verify Stripe integration (use test mode!)
- ✅ Check accessibility (screen readers, keyboard navigation)
- ✅ Test sacred geometry themes render correctly

## Code Standards

See path-specific instructions:
- `.github/instructions/html-files.instructions.md` - HTML standards
- `.github/instructions/javascript-files.instructions.md` - JavaScript standards
- `.github/instructions/python-files.instructions.md` - Python standards
- `.github/instructions/workflow-files.instructions.md` - GitHub Actions

## Important Guidelines

### Consciousness-First Language

Use language that empowers and heals:

**Good**:
- "Recognize patterns" (not "diagnose problems")
- "Healing journey" (not "treatment")
- "Consciousness development" (not "fixing yourself")
- "Pattern awareness" (not "what's wrong with you")

**Avoid**:
- Medical/diagnostic language
- Victim-blaming language
- Judgmental or shaming language
- Triggering or re-traumatizing descriptions

### Security Requirements
1. **Never commit secrets** - Use environment variables
2. **Validate all inputs** - Especially in ARAYA file operations
3. **Safe file access** - Always use ARAYA_FILE_ACCESS.py
4. **Stripe security** - Use test mode for development
5. **User privacy** - Never log personal/sensitive data

### Accessibility Requirements
1. **WCAG AA compliance** - Minimum standard
2. **Screen reader support** - Proper ARIA labels
3. **Keyboard navigation** - All features keyboard accessible
4. **Mobile-first** - Optimize for phones
5. **Sacred geometry compatible** - Respect the design system

## Stripe Integration

For payment features:

```javascript
// Initialize Stripe (client-side)
const stripe = Stripe('pk_test_YOUR_KEY');  // Use test keys in dev

// Create checkout session
const checkout = await fetch('/api/create-checkout', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    priceId: 'price_XXXXX',
    email: userEmail
  })
});

// Redirect to Stripe Checkout
const { sessionId } = await checkout.json();
await stripe.redirectToCheckout({ sessionId });
```

## Supabase Integration

For database operations:

```javascript
// Initialize Supabase client
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
);

// Query user patterns
const { data, error } = await supabase
  .from('user_patterns')
  .select('*')
  .eq('user_id', userId);

if (error) {
  console.error('Database error:', error);
  showUserFriendlyMessage('Unable to load your data right now');
}
```

## Multi-AI Orchestrator Usage

Always use the orchestrator for AI calls:

```javascript
// Chat completion
const response = await window.openAIOrchestrator.chat({
  messages: [
    { role: 'system', content: 'You are ARAYA...' },
    { role: 'user', content: userMessage }
  ],
  model: 'gpt-4o',  // or 'claude-3-5-sonnet', 'llama-3-70b'
  temperature: 0.7
});

// The orchestrator handles:
// - Provider selection
// - Error handling
// - Retries
// - Rate limiting
// - Cost tracking
```

## Common Tasks

### Adding a New Pattern Detector

1. Create HTML file following template in `.github/instructions/html-files.instructions.md`
2. Add pattern detection logic (educational, not diagnostic)
3. Include healing resources and next steps
4. Test for triggering language
5. Add to pattern library index
6. Document the pattern clearly

### Updating ARAYA Conversations

1. Review `ARAYA_GUIDED_HEALING_FLOWS.json`
2. Maintain empathetic, non-judgmental tone
3. Test conversation flows
4. Ensure boundaries are respected
5. Add healing resources
6. Never medical/diagnostic language

### Adding New AI Integration

1. Use the Multi-AI Orchestrator
2. Add provider configuration
3. Implement fallback logic
4. Test error handling
5. Monitor costs
6. Document usage patterns

## Documentation Standards

### README Files
- Clear purpose and healing context
- Quick start guide
- Consciousness-aware language
- Contact/support information

### Code Comments
- Explain "why" for complex logic
- Document healing intent
- Include examples
- Reference patterns when relevant

### Commit Messages
- Present tense ("Add feature" not "Added feature")
- Consciousness context when relevant
- Reference issues when applicable

## Testing Requirements

Before submitting changes:

- [ ] All features work on mobile
- [ ] ARAYA conversations are safe and empathetic
- [ ] Pattern detectors are educational
- [ ] AI orchestrator handles errors gracefully
- [ ] Stripe integration uses test mode
- [ ] Accessibility features work
- [ ] Sacred geometry themes render correctly
- [ ] No console errors
- [ ] No triggering or harmful language

## Deployment

### Netlify Deployment
- Changes to `main` branch auto-deploy
- Test in feature branch first
- Monitor deployment logs
- Verify live site after deployment
- Check Stripe webhooks

### Python Services
- Test locally first
- Use environment variables for secrets
- Monitor logs and health checks
- Verify Supabase connections

## Contact and Support

- **Repository**: This is an autonomous consciousness platform
- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions

## Remember

**CRITICAL**: This platform helps people heal from trauma and manipulation. Every change affects someone's healing journey.

**Priorities**:
1. **Safety first** - Never harm users
2. **Empathy always** - Compassionate language
3. **Accessibility matters** - Everyone deserves access
4. **Privacy sacred** - Protect user data
5. **Consciousness-focused** - Empower, don't diagnose

When in doubt, ask: "Does this help someone heal and develop consciousness?"
