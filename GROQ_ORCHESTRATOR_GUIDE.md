# GroqAI Orchestrator Guide for Consciousness Revolution

## Overview

The Consciousness Revolution platform uses **GroqAI** as the primary AI orchestrator, providing **FREE** AI capabilities with automatic fallback to other providers.

## Features

- ✅ **Free Tier**: 14,400 requests per day (no credit card required!)
- ✅ **Fast Inference**: Optimized for speed with Llama 3.3, Mixtral models
- ✅ **Automatic Fallback**: Falls back to HuggingFace or OpenAI if needed
- ✅ **Unified Interface**: Consistent API across all projects
- ✅ **Health Monitoring**: Automatic health checks and error tracking
- ✅ **Zero Configuration**: Works out of the box for all projects

## API Key Setup

### Get Your Free Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for a free account (no credit card needed)
3. Create a new API key (starts with `gsk_`)
4. Copy your key

### Configure API Key

Add your key to `.env` file:

```bash
GROQ_API_KEY=gsk_your_key_here
```

This key is configured in:
- **Configuration File**: `groq-orchestrator-config.json`
- **Environment File**: `.env` (not committed to git)
- **Initialization Script**: `groq-orchestrator-init.js`

Or set it directly in your HTML:

```html
<script src="/groq-orchestrator-init.js"></script>
<script>
  // Set key programmatically
  multiAI.setApiKey('groq', 'gsk_your_key_here');
</script>
```

## Quick Start

### Option 1: Auto-initialization (Recommended)

Add this to your HTML file:

```html
<!-- Load GroqAI orchestrator (auto-initializes) -->
<script src="/groq-orchestrator-init.js"></script>

<script>
  // Wait for initialization, then use
  async function myAIFunction() {
    const response = await groqAI.chat([
      {
        role: 'user',
        content: 'Explain pattern recognition'
      }
    ]);
    
    console.log(response.choices[0].message.content);
  }
</script>
```

### Option 2: Manual initialization

```html
<!-- Load multi-provider orchestrator -->
<script src="/src/ai/multi-provider-orchestrator.js"></script>

<script>
  // Set GroqAI key
  multiAI.setApiKey('groq', 'gsk_your_key_here');
  
  // Use the API
  async function myAIFunction() {
    const response = await multiAI.chatCompletion([
      {
        role: 'user',
        content: 'Hello!'
      }
    ]);
    
    console.log(response.choices[0].message.content);
  }
</script>
```

## Usage Examples

### Basic Chat

```javascript
const response = await groqAI.chat([
  { role: 'user', content: 'What are the 7 domains of consciousness?' }
]);

console.log(response.choices[0].message.content);
```

### Chat with System Message

```javascript
const response = await groqAI.chat([
  {
    role: 'system',
    content: 'You are a consciousness coach helping people recognize patterns.'
  },
  {
    role: 'user',
    content: 'How do I identify gaslighting?'
  }
]);

console.log(response.choices[0].message.content);
```

### Chat with Options

```javascript
const response = await groqAI.chat([
  {
    role: 'user',
    content: 'Generate a creative healing story.'
  }
], {
  model: 'llama-3.3-70b-versatile',  // Specify model
  temperature: 0.9,                   // Increase creativity
  max_tokens: 500                     // Limit response length
});

console.log(response.choices[0].message.content);
```

### Audio Transcription

```javascript
// Get audio file from input
const audioFile = document.getElementById('audioInput').files[0];

// Transcribe with Whisper
const transcription = await groqAI.transcribe(audioFile);

console.log(transcription.text);
```

### Check Status

```javascript
// Get current AI system status
const status = groqAI.getStatus();

console.log('Health:', status.healthStatus);
console.log('Requests:', status.requestCount);
console.log('Errors:', status.errorCount);
console.log('Error Rate:', status.errorRate);

// Show detailed dashboard
groqAI.showDashboard();
```

## Available Models

### Chat Models

| Model | Description | Speed | Best For |
|-------|-------------|-------|----------|
| `llama-3.3-70b-versatile` | Primary model (default) | Fast | General purpose, high quality, consciousness analysis |
| `llama-3.1-8b-instant` | Fastest model | Fastest | Quick responses, simple tasks, pattern detection |
| `mixtral-8x7b-32768` | Large context window | Fast | Long conversations, documents, deep analysis |
| `gemma2-9b-it` | Lightweight | Very Fast | Simple queries, basic pattern recognition |

**Note:** `llama-3.1-70b-versatile` has been decommissioned by Groq. Use `llama-3.3-70b-versatile` as the primary alternative.

### Audio Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `whisper-large-v3` | Audio transcription | Speech-to-text, voice notes, conversation analysis |

## Configuration

### Configuration File: `groq-orchestrator-config.json`

```json
{
  "name": "Consciousness Revolution GroqAI Orchestrator",
  "provider": "groq",
  "apiKey": "gsk_your_key_here",
  "enabled": true,
  "priority": 1,
  "models": {
    "chat": {
      "primary": "llama-3.3-70b-versatile",
      "fast": "llama-3.1-8b-instant"
    }
  },
  "features": {
    "autoRetry": true,
    "autoFallback": true,
    "rateLimiting": true
  }
}
```

### Environment Variables: `.env`

```bash
# Primary AI Orchestrator
GROQ_API_KEY=gsk_your_key_here

# Fallback providers (optional)
OPENAI_API_KEY=sk-your-openai-key-here
HUGGINGFACE_API_KEY=hf_your_key_here
```

## Integration Points

The GroqAI orchestrator is integrated across:

### 1. Consciousness Systems
- **ARAYA**: Healing consciousness conversations and pattern analysis
- **Cyclotron Brain**: Knowledge queries and semantic search
- **Pattern Detectors**: Real-time manipulation pattern recognition
- **7 Domains**: Consciousness assessment and guidance

### 2. Agent Systems
- **Merlin Hive**: Central AI coordination
- **Agent R**: System architecture decisions
- **Management Dashboard**: Monitoring and control

### 3. User-Facing Features
- **Government Grants Portal**: Grant matching and application generation
- **Contributor Dashboard**: AI-assisted guidance
- **Megan AI Dashboard**: Multi-provider interface

### 4. Backend Services
- **API Connection Manager**: Automatic retry and fallback
- **Autonomous API Key Manager**: Smart key sourcing
- **Enhancement Loop**: Code improvement suggestions

### 5. Content Generation
- **GemBot Universe**: AI character interactions
- **Voice NFT**: Audio processing
- **Content Sharing**: Automated content generation

## Integration with Consciousness Systems

### ARAYA Consciousness System

```javascript
// Integrate with ARAYA for consciousness analysis
const analysis = await groqAI.chat([
  {
    role: 'system',
    content: 'You are ARAYA, analyzing consciousness patterns with empathy and wisdom.'
  },
  {
    role: 'user',
    content: `Analyze this message for manipulation patterns: "${userMessage}"`
  }
]);
```

### Pattern Detection Tools

```javascript
// Enhance pattern detectors with AI
async function detectGaslighting(message) {
  const response = await groqAI.chat([
    {
      role: 'system',
      content: 'You are a pattern recognition expert. Identify gaslighting tactics educationally, not diagnostically.'
    },
    {
      role: 'user',
      content: message
    }
  ]);
  
  return response.choices[0].message.content;
}
```

### Cyclotron Brain Integration

```javascript
// Use for Cyclotron knowledge queries
async function queryBrain(question) {
  const response = await groqAI.chat([
    {
      role: 'system',
      content: 'You have access to the Cyclotron knowledge base. Answer based on consciousness principles and pattern theory.'
    },
    {
      role: 'user',
      content: question
    }
  ]);
  
  return response.choices[0].message.content;
}
```

## API Reference

### `groqAI.chat(messages, options)`

Make a chat completion request.

**Parameters:**
- `messages` (Array): Array of message objects with `role` and `content`
- `options` (Object, optional):
  - `model` (string): Model to use (default: `llama-3.3-70b-versatile`)
  - `temperature` (number): 0.0-2.0, controls randomness (default: 0.7)
  - `max_tokens` (number): Maximum response length (default: 1000)

**Returns:** Promise resolving to response object with `choices` array

### `groqAI.transcribe(audioFile, options)`

Transcribe audio file to text.

**Parameters:**
- `audioFile` (File): Audio file to transcribe
- `options` (Object, optional):
  - `model` (string): Model to use (default: `whisper-large-v3`)
  - `language` (string): Expected language code (optional)

**Returns:** Promise resolving to transcription object with `text` property

### `groqAI.getStatus()`

Get current orchestrator status.

**Returns:** Object with:
- `initialized` (boolean): Whether orchestrator is ready
- `healthStatus` (string): 'healthy', 'unhealthy', or 'unknown'
- `requestCount` (number): Total requests made
- `errorCount` (number): Total errors encountered
- `errorRate` (string): Error percentage
- `provider` (string): Current provider ('groq')
- `model` (string): Primary model being used

### `groqAI.showDashboard()`

Display status dashboard in console.

**Returns:** void (outputs to console)

## Testing

A comprehensive test suite is available at:

**URL**: [test-groq-orchestrator.html](./test-groq-orchestrator.html)

### Tests Included:
1. **Configuration Load**: Verifies config file is accessible
2. **API Key Validation**: Confirms key is valid and accepted
3. **Simple Chat**: Tests basic chat functionality
4. **Advanced Chat**: Tests chat with system messages
5. **Error Handling**: Verifies graceful error handling
6. **Performance**: Measures response times across multiple requests

### Running Tests

1. Open `test-groq-orchestrator.html` in your browser
2. Click "Run All Tests" or run individual tests
3. Check results for each test
4. View system status in real-time

Or check the status dashboard in browser console:

```javascript
// In browser console
groqAI.showDashboard();
```

Output:
```
🤖 GroqAI Orchestrator Dashboard
══════════════════════════════════════════════════
Status: ✅ Initialized
Health: ✅ healthy
Provider: groq
Primary Model: llama-3.3-70b-versatile
Requests: 42
Errors: 0
Error Rate: 0.00%
══════════════════════════════════════════════════
```

## Monitoring

### Health Checks

The orchestrator automatically performs health checks every 5 minutes:

```javascript
// Manual health check
const isHealthy = await performHealthCheck();

if (!isHealthy) {
  console.warn('Orchestrator is unhealthy!');
}
```

### Request Tracking

All requests are tracked and can be monitored:

```javascript
const status = groqAI.getStatus();

console.log(`Requests: ${status.requestCount}`);
console.log(`Errors: ${status.errorCount}`);
console.log(`Error Rate: ${status.errorRate}`);
```

## Error Handling

The orchestrator includes robust error handling:

### Automatic Retry

Failed requests are automatically retried with exponential backoff:

```javascript
try {
  const response = await groqAI.chat([...]);
} catch (error) {
  // After automatic retry attempts
  console.error('Request failed:', error.message);
}
```

### Fallback Providers

If GroqAI fails, the system automatically falls back to:
1. **HuggingFace** (free, rate limited)
2. **OpenAI** (paid, highest quality)
3. **Mock responses** (for testing)

Configure fallback providers in `.env`:

```bash
HUGGINGFACE_API_KEY=hf_your_key_here
OPENAI_API_KEY=sk-your_key_here
```

### Error Types

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `API key not set` | Key not loaded | Check config file and .env |
| `Rate limit exceeded` | Too many requests | Wait 1 minute, implement queuing |
| `Invalid model` | Model name typo | Check available models list |
| `Network error` | Connection issue | Check internet connection |

## Rate Limits & Best Practices

### Free Tier Limits
- **Daily**: 14,400 requests per day
- **Rate**: ~10 requests per minute average
- **Burst**: Higher rates allowed for short periods

### Best Practices

#### 1. Keep Requests Concise

```javascript
// Good
const response = await groqAI.chat([
  { role: 'user', content: 'Summarize pattern theory in 2 sentences' }
]);

// Avoid
const response = await groqAI.chat([
  { role: 'user', content: 'Please tell me everything you know about...' }
]);
```

#### 2. Use Appropriate Models

```javascript
// For quick tasks, use fast model
const quick = await groqAI.chat([...], {
  model: 'llama-3.1-8b-instant'
});

// For complex consciousness analysis, use primary model
const complex = await groqAI.chat([...], {
  model: 'llama-3.3-70b-versatile'
});
```

#### 3. Handle Errors Gracefully

```javascript
async function safeAIRequest(prompt) {
  try {
    const response = await groqAI.chat([
      { role: 'user', content: prompt }
    ]);
    return response.choices[0].message.content;
  } catch (error) {
    console.error('AI request failed:', error);
    return 'Sorry, AI is temporarily unavailable. Please try again.';
  }
}
```

#### 4. Monitor Usage

```javascript
// Check status periodically
const status = groqAI.getStatus();
if (status.requestCount > 10000) {
  console.warn('Approaching daily limit');
}

// Check periodically
setInterval(() => {
  const status = groqAI.getStatus();
  if (status.errorRate > 10) {
    console.warn('High error rate detected!');
  }
}, 60000); // Check every minute
```

### Avoiding Rate Limits

```javascript
// Implement request queue
const requestQueue = [];
let processing = false;

async function queuedRequest(messages) {
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
    setTimeout(processQueue, 1000); // 1 second delay between requests
  }
}
```

## Troubleshooting

### "GroqAI orchestrator not initialized"

**Solution:**
1. Check that `groq-orchestrator-init.js` is loaded
2. Wait for initialization: `window.addEventListener('load', () => { /* use groqAI */ })`
3. Check browser console for initialization errors

```javascript
window.addEventListener('load', () => {
  // Use groqAI after page loads
  groqAI.showDashboard();
});
```

### "API key not set" or "API key validation failed"

**Solution:**
1. Verify key in `groq-orchestrator-config.json`
2. Check that key starts with `gsk_`
3. Ensure config file is accessible (not blocked by CORS)
4. Set key programmatically if needed:

```javascript
multiAI.setApiKey('groq', 'gsk_your_key_here');
```

### Rate limit errors

**Solution:**
1. Check request count: `groqAI.getStatus().requestCount`
2. Implement request queuing (see Rate Limits section)
3. Consider using fast model for simple requests
4. Wait for rate limit to reset (resets daily)
5. Add delay between requests:

```javascript
// Add delay between requests
await new Promise(resolve => setTimeout(resolve, 1000));
const response = await groqAI.chat(messages);
```

### Slow responses

**Solution:**
1. Use faster model: `llama-3.1-8b-instant`
2. Reduce `max_tokens` in request
3. Simplify prompts
4. Check network connection

## Migration from Other Providers

### From OpenAI

```javascript
// Before (OpenAI)
const response = await openAIOrchestrator.chatCompletion('gpt-4o', [
  { role: 'user', content: 'Hello' }
]);

// After (GroqAI)
const response = await groqAI.chat([
  { role: 'user', content: 'Hello' }
], {
  model: 'llama-3.3-70b-versatile'
});
```

### From Multi-Provider

```javascript
// Before
const response = await multiAI.chatCompletion([...], {
  provider: 'openai'
});

// After (uses GroqAI by default)
const response = await multiAI.chatCompletion([...]);

// Or use groqAI directly
const response = await groqAI.chat([...]);
```

## Support

For issues or questions:

1. **Check Test Suite**: Run `test-groq-orchestrator.html` to diagnose
2. **View Console**: Check browser console for detailed error messages
3. **Check Status**: Run `groqAI.showDashboard()` to see health status
4. **Get API Key**: [https://console.groq.com/keys](https://console.groq.com/keys)
5. **Documentation**: This file
6. **Issues**: Open issue on GitHub repository

## Security Notes

- ✅ API keys should be in `.env` file (not committed to git)
- ✅ `.env` is already in `.gitignore`
- ✅ Never hardcode API keys in source code
- ✅ Use environment variables for production

## Changelog

### Version 1.0.0 (2026-02-08)
- Initial GroqAI orchestrator integration
- Repo-wide API key configuration
- Auto-initialization script
- Comprehensive test suite
- Multi-provider fallback support
- Health monitoring and tracking
- Full documentation
- Integration with ARAYA, Cyclotron, and pattern detectors

## License

This integration is part of the Consciousness Revolution platform. See main repository LICENSE for details.

---

**Built for Consciousness Revolution** - Pattern recognition powered by AI 🧠✨

**Last Updated**: 2026-02-08  
**Contact**: Open issue on GitHub for support
