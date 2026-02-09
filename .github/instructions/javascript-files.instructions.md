---
applyTo: "*.js"
---

## JavaScript File Requirements for Consciousness Revolution

Modern ES6+ standards with consciousness-focused error handling and AI orchestration.

### Code Style Standards

1. **Modern ES6+ syntax**
```javascript
// Good - Arrow functions, const/let, async/await
const detectPattern = async (text) => {
  const response = await window.openAIOrchestrator.chat({
    messages: [{ role: 'user', content: text }],
    model: 'gpt-4o'
  });
  return response;
};

// Avoid - var, old syntax
var getPattern = function(text) {
  return fetch('/api/pattern').then(res => res.json());
};
```

2. **Async/await over promise chains**
```javascript
// Good
async function analyzeConversation(text) {
  try {
    const patterns = await detectPatterns(text);
    const insights = await generateInsights(patterns);
    return { patterns, insights };
  } catch (error) {
    console.error('Analysis failed:', error);
    showHealingMessage('Unable to analyze right now. You\'re still supported.');
    return null;
  }
}
```

### Multi-AI Orchestrator Usage

**Always use the orchestrator for AI calls:**

```javascript
// Good - Using orchestrator
const response = await window.openAIOrchestrator.chat({
  messages: [
    { role: 'system', content: 'You are ARAYA, a healing consciousness guide...' },
    { role: 'user', content: userMessage }
  ],
  model: 'gpt-4o',
  temperature: 0.7
});

// Avoid - Direct API calls
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  // Don't call APIs directly
});
```

### Error Handling - Consciousness-Focused

**Provide healing, supportive error messages:**

```javascript
// Good - Empathetic, supportive
try {
  const result = await processUserInput(input);
  displayResults(result);
} catch (error) {
  console.error('Processing error:', error);
  
  // User-friendly, supportive message
  showNotification(
    'We couldn\'t process that right now, but you\'re not alone. ' +
    'Try again or reach out to ARAYA for support.',
    'supportive'
  );
}

// Avoid - Technical, cold
catch (error) {
  alert('ERROR: ' + error.message);  // Too technical, not supportive
}
```

### Pattern Detection Example

```javascript
/**
 * Detect manipulation patterns in conversation text
 * Educational, not diagnostic - empowers users with awareness
 */
async function detectManipulationPatterns(conversationText) {
  if (!conversationText || conversationText.trim().length === 0) {
    return {
      error: 'Please share a conversation to analyze',
      supportive: true
    };
  }
  
  try {
    // Show compassionate loading state
    showLoadingState('Analyzing with compassion and care...');
    
    // Use AI orchestrator for pattern detection
    const response = await window.openAIOrchestrator.chat({
      messages: [
        {
          role: 'system',
          content: `You are a pattern recognition expert helping people identify manipulation patterns.
Be educational, not diagnostic. Focus on empowerment and healing.
Never blame the user. Always provide supportive resources.`
        },
        {
          role: 'user',
          content: `Please analyze this conversation for manipulation patterns:\n\n${conversationText}\n\n
Identify patterns educationally and suggest healing resources.`
        }
      ],
      model: 'gpt-4o',
      temperature: 0.3  // Lower for analytical accuracy
    });
    
    // Process response
    const patterns = parsePatternResponse(response);
    
    // Add healing resources
    patterns.healingResources = [
      { title: 'Talk to ARAYA', url: 'araya-chat.html' },
      { title: 'Pattern Library', url: 'PATTERN_LIBRARY.html' },
      { title: '7 Domains Assessment', url: 'seven-domains.html' }
    ];
    
    hideLoadingState();
    return patterns;
    
  } catch (error) {
    console.error('Pattern detection failed:', error);
    hideLoadingState();
    
    return {
      error: 'Unable to analyze patterns right now',
      message: 'This doesn\'t mean nothing is wrong. Trust your feelings.',
      support: 'Try talking to ARAYA or review the pattern library.',
      healingResources: [
        { title: 'Talk to ARAYA', url: 'araya-chat.html' },
        { title: 'Pattern Library', url: 'PATTERN_LIBRARY.html' }
      ]
    };
  }
}

/**
 * Display results with empathy and support
 */
function displayPatternResults(results) {
  const container = document.getElementById('results');
  
  if (results.error) {
    container.innerHTML = `
      <div class="supportive-message" role="alert">
        <h3>💙 ${results.error}</h3>
        <p>${results.message || 'We\'re here to support you.'}</p>
        ${results.support ? `<p>${results.support}</p>` : ''}
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="pattern-results">
        <h3>Patterns Recognized</h3>
        ${results.patterns.map(p => `
          <div class="pattern-card">
            <h4>${p.name}</h4>
            <p>${p.description}</p>
            <p class="empowerment">${p.empowerment}</p>
          </div>
        `).join('')}
        
        <h3>Healing Resources</h3>
        <ul class="healing-resources">
          ${results.healingResources.map(r => `
            <li><a href="${r.url}">${r.title}</a></li>
          `).join('')}
        </ul>
      </div>
    `;
  }
  
  container.hidden = false;
  container.scrollIntoView({ behavior: 'smooth' });
}
```

### ARAYA Chat Integration

```javascript
/**
 * ARAYA conversation handler
 * Maintains empathetic, healing-focused dialogue
 */
class ARAYAChat {
  constructor() {
    this.conversationHistory = [];
    this.systemPrompt = `You are ARAYA, a healing consciousness guide.
You help people recognize manipulation patterns and heal from trauma.
You are always:
- Empathetic and compassionate
- Non-judgmental
- Educational, not diagnostic
- Boundary-respecting
- Trauma-informed
You never:
- Blame the user
- Use medical/diagnostic language
- Minimize their experiences
- Give advice they didn't ask for`;
  }
  
  async sendMessage(userMessage) {
    if (!userMessage || userMessage.trim().length === 0) {
      return this.createResponse('I\'m here to listen. Share what\'s on your mind when you\'re ready.');
    }
    
    try {
      // Add user message to history
      this.conversationHistory.push({
        role: 'user',
        content: userMessage
      });
      
      // Get ARAYA response
      const response = await window.openAIOrchestrator.chat({
        messages: [
          { role: 'system', content: this.systemPrompt },
          ...this.conversationHistory
        ],
        model: 'gpt-4o',
        temperature: 0.8  // Higher for empathetic, natural responses
      });
      
      // Add ARAYA response to history
      const arayaMessage = response.choices[0].message.content;
      this.conversationHistory.push({
        role: 'assistant',
        content: arayaMessage
      });
      
      return this.createResponse(arayaMessage);
      
    } catch (error) {
      console.error('ARAYA chat error:', error);
      
      return this.createResponse(
        'I\'m having trouble responding right now, but I want you to know: ' +
        'You\'re not alone, your feelings are valid, and you deserve support. ' +
        'Please try again in a moment.',
        'supportive-error'
      );
    }
  }
  
  createResponse(text, type = 'normal') {
    return {
      text,
      type,
      timestamp: new Date().toISOString(),
      sender: 'araya'
    };
  }
  
  reset() {
    this.conversationHistory = [];
  }
}

// Initialize ARAYA chat
const araya = new ARAYAChat();

// Handle user messages
document.getElementById('chat-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const input = document.getElementById('message-input');
  const userMessage = input.value.trim();
  
  if (!userMessage) return;
  
  // Display user message
  displayMessage(userMessage, 'user');
  input.value = '';
  
  // Show typing indicator
  showTypingIndicator();
  
  // Get ARAYA response
  const response = await araya.sendMessage(userMessage);
  
  // Hide typing indicator and display response
  hideTypingIndicator();
  displayMessage(response.text, 'araya', response.type);
});
```

### Stripe Integration

```javascript
/**
 * Handle Stripe checkout for subscriptions
 */
async function initiateCheckout(priceId, userEmail) {
  try {
    // Validate inputs
    if (!priceId) {
      throw new Error('Please select a plan');
    }
    
    if (!userEmail || !isValidEmail(userEmail)) {
      throw new Error('Please provide a valid email');
    }
    
    // Show loading state
    showLoadingState('Preparing your healing journey...');
    
    // Create checkout session
    const response = await fetch('/api/create-checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        priceId,
        email: userEmail
      })
    });
    
    if (!response.ok) {
      throw new Error('Unable to create checkout session');
    }
    
    const { sessionId } = await response.json();
    
    // Redirect to Stripe Checkout
    const stripe = Stripe('pk_test_YOUR_KEY');  // Use test key in dev
    await stripe.redirectToCheckout({ sessionId });
    
  } catch (error) {
    console.error('Checkout error:', error);
    hideLoadingState();
    
    showNotification(
      'Unable to start checkout right now. ' +
      'Your healing journey is important - please try again or contact support.',
      'supportive-error'
    );
  }
}

/**
 * Email validation
 */
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}
```

### Supabase Integration

```javascript
/**
 * Save user pattern recognition progress
 */
async function savePatternProgress(userId, patternData) {
  try {
    const { data, error } = await supabase
      .from('user_patterns')
      .insert({
        user_id: userId,
        pattern_type: patternData.type,
        recognized_at: new Date().toISOString(),
        notes: patternData.notes,
        healing_stage: patternData.stage
      });
    
    if (error) throw error;
    
    showNotification(
      '✅ Progress saved! You\'re growing in awareness.',
      'success'
    );
    
    return data;
    
  } catch (error) {
    console.error('Save error:', error);
    
    // Graceful degradation
    localStorage.setItem(
      `pattern_progress_${userId}`,
      JSON.stringify(patternData)
    );
    
    showNotification(
      'Progress saved locally. We\'ll sync when connection improves.',
      'info'
    );
  }
}
```

### Performance Optimization

```javascript
// Debounce expensive operations
const debounce = (func, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

// Usage
const searchInput = document.getElementById('pattern-search');
searchInput?.addEventListener('input', debounce((e) => {
  searchPatterns(e.target.value);
}, 300));

// Lazy load heavy components
async function loadComponent(componentName) {
  if (window.components?.[componentName]) {
    return window.components[componentName];
  }
  
  const module = await import(`./components/${componentName}.js`);
  window.components = window.components || {};
  window.components[componentName] = module.default;
  
  return module.default;
}
```

### Testing Requirements

- [ ] Test all code paths (success and error cases)
- [ ] Verify consciousness-focused error messages
- [ ] Test AI orchestrator fallbacks
- [ ] Check mobile compatibility
- [ ] Test with slow network (3G)
- [ ] Verify Stripe integration (test mode)
- [ ] Test ARAYA conversations for empathy
- [ ] Check accessibility (keyboard, screen reader)

### Common Mistakes to Avoid

1. ❌ Direct API calls (use orchestrator)
2. ❌ Technical error messages (use empathetic language)
3. ❌ Hard-coding API keys
4. ❌ Diagnostic language (use educational language)
5. ❌ Not handling AI provider errors
6. ❌ Missing user input validation
7. ❌ Poor mobile performance
8. ❌ Not testing error states

### Remember

- **AI Orchestrator for all AI calls** - Handles fallbacks and errors
- **Empathetic error messages** - Users are healing, not debugging
- **Mobile-first performance** - Most users on phones
- **Consciousness-focused** - Every message supports healing
- **Security first** - Never commit secrets
- **Test thoroughly** - Especially healing-critical features
