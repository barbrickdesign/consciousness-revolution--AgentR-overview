# GroqAI Orchestrator Guide for Consciousness Revolution

## Overview

The Consciousness Revolution platform now uses **GroqAI** as the primary AI orchestrator, providing **FREE** AI capabilities with automatic fallback to other providers.

## Features

- ✅ **Free Tier**: 14,400 requests per day (no credit card required!)
- ✅ **Fast Inference**: Optimized for speed with Llama 3.3, Mixtral models
- ✅ **Automatic Fallback**: Falls back to HuggingFace or OpenAI if needed
- ✅ **Unified Interface**: Consistent API across all projects
- ✅ **Health Monitoring**: Automatic health checks and error tracking
- ✅ **Zero Configuration**: Works out of the box

## Quick Start

### 1. Get Your Free Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for a free account (no credit card needed)
3. Create a new API key (starts with `gsk_`)
4. Copy your key

### 2. Configure API Key

Add your key to `.env` file:

```bash
GROQ_API_KEY=gsk_your_key_here
```

Or set it directly in your HTML:

```html
<script src="/groq-orchestrator-init.js"></script>
<script>
  // Set key programmatically
  multiAI.setApiKey('groq', 'gsk_your_key_here');
</script>
```

### 3. Use in Your Pages

Add this single line to any HTML file:

```html
<script src="/groq-orchestrator-init.js"></script>
```

Then use the AI anywhere:

```javascript
// Chat with AI
const response = await groqAI.chat([
  { role: 'user', content: 'Explain pattern recognition' }
]);

console.log(response.choices[0].message.content);
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

// Show detailed dashboard
groqAI.showDashboard();
```

## Available Models

### Chat Models

| Model | Description | Speed | Best For |
|-------|-------------|-------|----------|
| `llama-3.3-70b-versatile` | Primary model (default) | Fast | General purpose, high quality |
| `llama-3.1-8b-instant` | Fastest model | Fastest | Quick responses, simple tasks |
| `mixtral-8x7b-32768` | Large context window | Fast | Long conversations, documents |
| `gemma2-9b-it` | Lightweight | Very Fast | Simple queries |

### Audio Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `whisper-large-v3` | Audio transcription | Speech-to-text, voice notes |

## Integration with Existing Systems

### ARAYA Consciousness System

```javascript
// Integrate with ARAYA for consciousness analysis
const analysis = await groqAI.chat([
  {
    role: 'system',
    content: 'You are ARAYA, analyzing consciousness patterns.'
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
      content: 'You are a pattern recognition expert. Identify gaslighting tactics.'
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
      content: 'You have access to the Cyclotron knowledge base. Answer based on consciousness principles.'
    },
    {
      role: 'user',
      content: question
    }
  ]);
  
  return response.choices[0].message.content;
}
```

## Testing

Check the status dashboard:

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

## Rate Limits & Best Practices

### Free Tier Limits
- **Daily**: 14,400 requests per day
- **Rate**: ~10 requests per minute average
- **Burst**: Higher rates allowed for short periods

### Best Practices

1. **Use Fast Models for Simple Tasks**
   ```javascript
   const response = await groqAI.chat(messages, {
     model: 'llama-3.1-8b-instant'  // Faster for simple queries
   });
   ```

2. **Keep Prompts Concise**
   ```javascript
   // Good
   const response = await groqAI.chat([
     { role: 'user', content: 'Summarize pattern theory in 2 sentences' }
   ]);
   ```

3. **Handle Errors Gracefully**
   ```javascript
   try {
     const response = await groqAI.chat(messages);
     return response.choices[0].message.content;
   } catch (error) {
     console.error('AI request failed:', error);
     return 'Sorry, AI is temporarily unavailable. Please try again.';
   }
   ```

4. **Monitor Usage**
   ```javascript
   // Check periodically
   const status = groqAI.getStatus();
   if (status.requestCount > 10000) {
     console.warn('Approaching daily limit');
   }
   ```

## Fallback Providers

If Groq fails, the system automatically falls back to:

1. **HuggingFace** (free, rate limited)
2. **OpenAI** (paid, highest quality)
3. **Mock responses** (for testing)

Configure fallback providers in `.env`:

```bash
HUGGINGFACE_API_KEY=hf_your_key_here
OPENAI_API_KEY=sk-your_key_here
```

## Troubleshooting

### "GroqAI orchestrator not initialized"

**Solution**: Wait for page load or check console for errors
```javascript
window.addEventListener('load', () => {
  // Use groqAI after page loads
  groqAI.showDashboard();
});
```

### "API key not set"

**Solution**: Set key in `.env` or programmatically
```javascript
multiAI.setApiKey('groq', 'gsk_your_key_here');
```

### Rate limit errors

**Solution**: Wait or implement request queuing
```javascript
// Add delay between requests
await new Promise(resolve => setTimeout(resolve, 1000));
const response = await groqAI.chat(messages);
```

## Support

- **Get API Key**: [https://console.groq.com/keys](https://console.groq.com/keys)
- **Documentation**: This file
- **Issues**: Open issue on GitHub
- **Email**: Contact team for help

## Security Notes

- ✅ API keys should be in `.env` file (not committed to git)
- ✅ `.env` is already in `.gitignore`
- ✅ Never hardcode API keys in source code
- ✅ Use environment variables for production

---

**Built for Consciousness Revolution** - Pattern recognition powered by AI 🧠✨
