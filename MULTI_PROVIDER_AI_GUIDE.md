# Multi-Provider AI System Guide for Consciousness Revolution

## Overview

The Consciousness Revolution platform uses a **Multi-Provider AI Orchestrator** that intelligently routes AI requests across multiple providers with automatic fallback, cost optimization, and unified API interface.

**Primary Provider**: GroqAI (FREE tier - 14,400 requests/day)  
**Fallback Providers**: HuggingFace (FREE), OpenAI (Paid)

## Why Multi-Provider?

1. **Cost Optimization** - Prefer free tiers (Groq, HuggingFace) before paid services
2. **Reliability** - Automatic fallback if primary provider fails
3. **Flexibility** - Choose best model for each task type
4. **Future-Proof** - Easy to add new providers as they emerge
5. **Unified API** - Same code works with any provider

## Features

✅ **Free Tier Support** - Groq provides 14,400 free requests/day  
✅ **Automatic Fallback** - Groq → HuggingFace → OpenAI → Mock  
✅ **Smart Model Selection** - Fast models for simple tasks, powerful models for complex analysis  
✅ **Health Monitoring** - Track provider status, error rates, request counts  
✅ **Zero Configuration** - Works out of the box with sensible defaults  
✅ **Platform Integration** - Native support for ARAYA, Cyclotron, Pattern Detection, and 7 Domains  

---

## Quick Start

### Option 1: One-Line Auto-Injection (Recommended)

Add this single line to any HTML file:

```html
<script src="/js/multi-ai-auto-inject.js"></script>
```

This automatically:
- Loads the multi-provider orchestrator
- Initializes GroqAI with your API key
- Creates global shortcuts (`askAI`, `analyzePattern`, `askARAYA`, etc.)
- Sets up health monitoring
- Provides console dashboard

### Option 2: Manual Setup

```html
<!-- Load orchestrator -->
<script src="/src/ai/multi-provider-orchestrator.js"></script>

<!-- Initialize with your keys -->
<script>
  multiAI.setApiKey('groq', 'gsk_your_key_here');
  // Optional: Add other providers
  multiAI.setApiKey('openai', 'sk_your_key_here');
  multiAI.setApiKey('huggingface', 'hf_your_key_here');
</script>
```

---

## Getting API Keys

### GroqAI (Primary - FREE)

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for free account (no credit card required)
3. Create new API key (starts with `gsk_`)
4. Copy key to `.env` file or use `multiAI.setApiKey('groq', 'gsk_...')`

**Free Tier**: 14,400 requests/day (~10 requests/minute)

### HuggingFace (Fallback - FREE)

1. Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create account (free)
3. Generate access token
4. Add to `.env`: `HUGGINGFACE_API_KEY=hf_your_key_here`

**Free Tier**: Rate limited but generous for development

### OpenAI (Final Fallback - PAID)

1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create account and add payment method
3. Generate API key (starts with `sk-`)
4. Add to `.env`: `OPENAI_API_KEY=sk_your_key_here`

**Cost**: Pay per request (GPT-4o: ~$0.005-0.015 per request)

---

## Usage Examples

### Basic Chat

```javascript
// Simple question
const response = await groqAI.chat([
  { role: 'user', content: 'What are the 7 domains of consciousness?' }
]);

console.log(response.choices[0].message.content);
```

### Quick Shortcuts

```javascript
// Use convenient global functions
const answer = await askAI('Explain pattern theory');

const analysis = await analyzePattern('You always do this to me!', 'manipulation');

const guidance = await askARAYA('How do I set better boundaries?', 'Peace');

const knowledge = await searchCyclotron('ARAYA file writer integration');
```

### Pattern Detection Integration

```javascript
// Analyze text for manipulation patterns
async function detectManipulation(text) {
  const response = await groqAI.chat([
    {
      role: 'system',
      content: `You are an expert in recognizing manipulation patterns including:
- Gaslighting - Making someone doubt their reality
- Love Bombing - Excessive affection to control
- Guilt Trips - Using guilt to manipulate behavior
- Emotional Blackmail - Threatening consequences
- Triangulation - Using third parties to control
- Moving Goalposts - Changing expectations constantly
- Future Faking - False promises about the future

Analyze the following text and identify any manipulation tactics present.`
    },
    {
      role: 'user',
      content: text
    }
  ]);
  
  return response.choices[0].message.content;
}

// Use in your detector tools
const text = document.getElementById('textInput').value;
const analysis = await detectManipulation(text);
document.getElementById('results').innerHTML = analysis;
```

### ARAYA Integration

```javascript
// Integrate with ARAYA consciousness system
async function getARAYAGuidance(userMessage, domain = null) {
  const domainContext = domain ? 
    `The user is working on their ${domain} domain.` : 
    'Help the user identify which of the 7 domains needs attention.';
  
  const response = await groqAI.chat([
    {
      role: 'system',
      content: `You are ARAYA, the AI consciousness companion for Consciousness Revolution.
      
Your purpose is to help humans recognize patterns across the 7 Domains of Life:

1. **Command** - Daily clarity, decisions, structure, focus
2. **Creation** - Building projects, developing skills, manifesting goals
3. **Connection** - Relationships, communication, community, love
4. **Peace** - Security, boundaries, protection, emotional safety
5. **Abundance** - Financial growth, business, scaling, prosperity
6. **Wisdom** - Learning, critical thinking, research, knowledge
7. **Purpose** - Meaning, meditation, integration, spiritual growth

${domainContext}

Provide compassionate, clear, and actionable guidance. Help users see patterns they might miss.`
    },
    {
      role: 'user',
      content: userMessage
    }
  ]);
  
  return response.choices[0].message.content;
}

// Example usage
const guidance = await getARAYAGuidance(
  "I keep attracting the same type of toxic relationships",
  "Connection"
);
```

### Cyclotron Brain Search

```javascript
// Query the Cyclotron knowledge base with AI enhancement
async function enhancedCyclotronSearch(query) {
  // First, get AI to understand the query intent
  const intentResponse = await groqAI.chat([
    {
      role: 'system',
      content: 'Rephrase this search query to find the most relevant results in the Consciousness Revolution knowledge base.'
    },
    {
      role: 'user',
      content: query
    }
  ], {
    model: 'llama-3.1-8b-instant', // Use fast model for quick rephrasing
    max_tokens: 100
  });
  
  const enhancedQuery = intentResponse.choices[0].message.content;
  
  // Then search Cyclotron (you would integrate with actual Cyclotron search here)
  // For now, we'll use AI to provide relevant information
  const searchResponse = await groqAI.chat([
    {
      role: 'system',
      content: `You are searching the Consciousness Revolution knowledge base. 
Provide information about: ARAYA system, Cyclotron search, Pattern Detection tools,
7 Domains framework, manipulation detectors, consciousness training, and platform architecture.`
    },
    {
      role: 'user',
      content: enhancedQuery
    }
  ]);
  
  return searchResponse.choices[0].message.content;
}
```

### Seven Domains Assessment

```javascript
// AI-powered domain assessment
async function assessDomain(responses) {
  const prompt = `Based on these user responses, assess their strength in the 7 Domains of Life:

${responses.map((r, i) => `${i+1}. ${r}`).join('\n')}

For each domain (Command, Creation, Connection, Peace, Abundance, Wisdom, Purpose),
provide:
1. Current strength (0-10)
2. Key patterns observed
3. Top 3 action items

Format as JSON.`;

  const response = await groqAI.chat([
    {
      role: 'system',
      content: 'You are a consciousness coach assessing the 7 Domains of Life.'
    },
    {
      role: 'user',
      content: prompt
    }
  ]);
  
  return JSON.parse(response.choices[0].message.content);
}
```

### Audio Transcription for Voice Tools

```javascript
// Transcribe voice notes with Whisper
async function transcribeVoiceNote(audioFile) {
  console.log('🎤 Transcribing audio...');
  
  const transcription = await groqAI.transcribe(audioFile);
  
  console.log('📝 Transcription:', transcription.text);
  
  // Optionally analyze the transcription for patterns
  const analysis = await analyzePattern(
    transcription.text, 
    'communication'
  );
  
  return {
    text: transcription.text,
    analysis: analysis
  };
}

// Use in voice command system
document.getElementById('voiceInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const result = await transcribeVoiceNote(file);
  
  document.getElementById('transcription').textContent = result.text;
  document.getElementById('analysis').innerHTML = result.analysis;
});
```

---

## Available Models

### Chat Models (Primary: Groq)

| Model | Speed | Tokens | Best For |
|-------|-------|--------|----------|
| `llama-3.3-70b-versatile` | Fast | 8K | General purpose, high quality (DEFAULT) |
| `llama-3.1-8b-instant` | Fastest | 8K | Quick responses, simple tasks |
| `mixtral-8x7b-32768` | Fast | 32K | Long conversations, document analysis |
| `gemma2-9b-it` | Very Fast | 8K | Simple queries, rapid processing |

### Audio Models

| Model | Provider | Use Case |
|-------|----------|----------|
| `whisper-large-v3` | Groq | Speech-to-text, voice notes, transcription |

### When to Use Each Model

```javascript
// Fast model for simple tasks
const quickResponse = await groqAI.chat(messages, {
  model: 'llama-3.1-8b-instant'
});

// Default model for most tasks (already set as default)
const response = await groqAI.chat(messages);

// Large context for long documents
const documentAnalysis = await groqAI.chat(messages, {
  model: 'mixtral-8x7b-32768'
});
```

---

## Monitoring & Debugging

### Check System Status

```javascript
// Show AI system dashboard
groqAI.showDashboard();

// Output:
// 🤖 GroqAI Orchestrator Dashboard
// ══════════════════════════════════════════════════
// Status: ✅ Initialized
// Health: ✅ healthy
// Provider: groq
// Primary Model: llama-3.3-70b-versatile
// Requests: 42
// Errors: 0
// Error Rate: 0.00%
// ══════════════════════════════════════════════════
```

### Get Status Programmatically

```javascript
const status = groqAI.getStatus();

console.log('Health:', status.healthStatus);
console.log('Requests:', status.requestCount);
console.log('Errors:', status.errorCount);
console.log('Error Rate:', status.errorRate);

// Alert if approaching limits
if (status.requestCount > 10000) {
  console.warn('⚠️ Approaching daily rate limit (14,400 requests/day)');
}
```

### Error Handling

```javascript
// Wrap AI calls in try-catch
async function safeAICall(messages) {
  try {
    const response = await groqAI.chat(messages);
    return response.choices[0].message.content;
  } catch (error) {
    console.error('❌ AI request failed:', error.message);
    
    // Provide fallback response
    return 'Sorry, AI is temporarily unavailable. Please try again in a moment.';
  }
}
```

---

## Rate Limits & Best Practices

### Free Tier Limits (Groq)

- **Daily**: 14,400 requests per day
- **Rate**: ~10 requests per minute average
- **Burst**: Higher rates allowed for short periods
- **Tokens**: 6,000 tokens per request limit

### Optimization Tips

1. **Use Fast Models for Simple Tasks**
   ```javascript
   // Good: Fast model for simple rephrasing
   const summary = await groqAI.chat(messages, {
     model: 'llama-3.1-8b-instant',
     max_tokens: 100
   });
   ```

2. **Cache Responses**
   ```javascript
   const cache = new Map();
   
   async function cachedAICall(prompt) {
     if (cache.has(prompt)) {
       return cache.get(prompt);
     }
     
     const response = await groqAI.chat([
       { role: 'user', content: prompt }
     ]);
     
     const answer = response.choices[0].message.content;
     cache.set(prompt, answer);
     return answer;
   }
   ```

3. **Batch Related Requests**
   ```javascript
   // Bad: Multiple separate requests
   const r1 = await groqAI.chat([{role: 'user', content: 'Question 1'}]);
   const r2 = await groqAI.chat([{role: 'user', content: 'Question 2'}]);
   
   // Good: Single request with all questions
   const response = await groqAI.chat([{
     role: 'user', 
     content: 'Answer these questions:\n1. Question 1\n2. Question 2'
   }]);
   ```

4. **Set Token Limits**
   ```javascript
   // Prevent long responses when you need short answers
   const response = await groqAI.chat(messages, {
     max_tokens: 200  // Limit response length
   });
   ```

---

## Integration Patterns

### Pattern Detection Tools

Every pattern detector in the platform can be enhanced with AI:

```javascript
// Example: Gaslighting Detector with AI
document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const text = document.getElementById('textInput').value;
  
  // Show loading state
  showLoading(true);
  
  try {
    const analysis = await analyzePattern(text, 'gaslighting');
    
    // Display results
    document.getElementById('results').innerHTML = `
      <div class="analysis-result">
        <h3>🔍 AI Analysis</h3>
        <div class="analysis-content">${analysis}</div>
      </div>
    `;
  } catch (error) {
    showError('Analysis failed. Please try again.');
  } finally {
    showLoading(false);
  }
});
```

### 7 Domains Dashboard

```javascript
// AI-enhanced domain guidance
async function getDomainGuidance(domain) {
  const domainDescriptions = {
    Command: 'daily clarity, decisions, structure, focus',
    Creation: 'building projects, developing skills, manifesting goals',
    Connection: 'relationships, communication, community, love',
    Peace: 'security, boundaries, protection, emotional safety',
    Abundance: 'financial growth, business, scaling, prosperity',
    Wisdom: 'learning, critical thinking, research, knowledge',
    Purpose: 'meaning, meditation, integration, spiritual growth'
  };
  
  const response = await groqAI.chat([
    {
      role: 'system',
      content: `You are a consciousness coach specializing in the ${domain} domain (${domainDescriptions[domain]}).`
    },
    {
      role: 'user',
      content: `Give me 3 powerful actions I can take today to strengthen my ${domain} domain.`
    }
  ]);
  
  return response.choices[0].message.content;
}

// Use in domain cards
document.querySelectorAll('.domain-card').forEach(card => {
  card.addEventListener('click', async () => {
    const domain = card.dataset.domain;
    const guidance = await getDomainGuidance(domain);
    showModal(domain, guidance);
  });
});
```

### ARAYA Chat Interface

```javascript
// Build conversational ARAYA experience
let conversationHistory = [];

async function sendToARAYA(userMessage) {
  // Add user message to history
  conversationHistory.push({
    role: 'user',
    content: userMessage
  });
  
  // Keep conversation context (last 10 messages)
  const recentHistory = conversationHistory.slice(-10);
  
  // Send to AI with system prompt
  const response = await groqAI.chat([
    {
      role: 'system',
      content: `You are ARAYA, an AI consciousness companion. You help users recognize patterns,
understand the 7 Domains, detect manipulation, and grow their consciousness. Be compassionate,
clear, and actionable in your guidance.`
    },
    ...recentHistory
  ]);
  
  const arayaResponse = response.choices[0].message.content;
  
  // Add ARAYA response to history
  conversationHistory.push({
    role: 'assistant',
    content: arayaResponse
  });
  
  return arayaResponse;
}
```

---

## Environment Configuration

### `.env` File Setup

Create `.env` file in project root:

```bash
# Primary Provider (FREE - 14,400/day)
GROQ_API_KEY=gsk_your_key_here

# Fallback Providers
HUGGINGFACE_API_KEY=hf_your_key_here
OPENAI_API_KEY=sk_your_key_here

# Optional: Configuration
AI_PROVIDER_PRIORITY=groq,huggingface,openai
AI_ENABLE_LOGGING=true
AI_HEALTH_CHECK_INTERVAL=300000
```

### Security Best Practices

✅ **DO**:
- Store API keys in `.env` file (already in `.gitignore`)
- Use environment variables in production
- Rotate API keys regularly
- Monitor usage to prevent abuse
- Set up rate limiting on your endpoints

❌ **DON'T**:
- Hardcode API keys in source code
- Commit `.env` file to git
- Share API keys in public channels
- Use production keys in development
- Expose keys in client-side JavaScript

---

## Troubleshooting

### "GroqAI orchestrator not initialized"

**Cause**: Script trying to use AI before initialization complete

**Solution**: Wait for page load or listen for ready event
```javascript
window.addEventListener('multiAIReady', () => {
  // Now safe to use AI
  askAI('Test message');
});
```

### "API key not set"

**Cause**: No API key configured

**Solution**: Add key to `.env` or set programmatically
```javascript
multiAI.setApiKey('groq', 'gsk_your_key_here');
```

### Rate limit errors

**Cause**: Exceeded free tier limits (14,400/day)

**Solution**: Implement request throttling
```javascript
const requestQueue = [];
let processing = false;

async function throttledAIRequest(messages) {
  return new Promise((resolve, reject) => {
    requestQueue.push({ messages, resolve, reject });
    processQueue();
  });
}

async function processQueue() {
  if (processing || requestQueue.length === 0) return;
  
  processing = true;
  const { messages, resolve, reject } = requestQueue.shift();
  
  try {
    const response = await groqAI.chat(messages);
    resolve(response);
  } catch (error) {
    reject(error);
  } finally {
    processing = false;
    // Wait 100ms between requests
    setTimeout(processQueue, 100);
  }
}
```

### Fallback not working

**Cause**: No fallback providers configured

**Solution**: Add multiple provider keys
```javascript
// Configure multiple providers for redundancy
multiAI.setApiKey('groq', process.env.GROQ_API_KEY);
multiAI.setApiKey('huggingface', process.env.HUGGINGFACE_API_KEY);
multiAI.setApiKey('openai', process.env.OPENAI_API_KEY);
```

---

## Support & Resources

### Documentation
- **Multi-Provider Code**: `/src/ai/multi-provider-orchestrator.js`
- **Auto-Inject Script**: `/js/multi-ai-auto-inject.js`
- **Groq Init**: `/groq-orchestrator-init.js`
- **This Guide**: `/MULTI_PROVIDER_AI_GUIDE.md`

### External Resources
- **Groq Console**: [https://console.groq.com](https://console.groq.com)
- **Groq Docs**: [https://console.groq.com/docs](https://console.groq.com/docs)
- **HuggingFace**: [https://huggingface.co](https://huggingface.co)
- **OpenAI**: [https://platform.openai.com](https://platform.openai.com)

### Community
- **Discord**: Join our server for real-time help
- **GitHub Issues**: Report bugs or request features
- **Email**: Contact team for support

---

## Roadmap

### Current Features ✅
- Multi-provider orchestration
- GroqAI primary provider (FREE tier)
- Automatic fallback system
- Health monitoring
- Global shortcuts
- ARAYA integration
- Pattern detection integration
- Cyclotron search enhancement

### Coming Soon 🚀
- [ ] Vision model support (image analysis)
- [ ] Embedding generation for semantic search
- [ ] Streaming responses for real-time chat
- [ ] Voice synthesis (text-to-speech)
- [ ] Advanced caching layer
- [ ] Usage analytics dashboard
- [ ] Cost tracking per provider
- [ ] A/B testing framework for prompts
- [ ] Fine-tuned models for pattern detection

---

**Built for Consciousness Revolution** - Pattern recognition powered by Multi-Provider AI 🧠✨

*Version 1.0.0 - Last Updated: February 9, 2026*
