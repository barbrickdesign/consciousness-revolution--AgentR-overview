# Consciousness Revolution Voice System

Voice interface for the Consciousness Revolution platform. Talk to your AI assistants!

## Features

- **Wake Word Detection**: Say "Hey Claude" or "Hey Commander" to activate
- **Voice Commands**: Control the system with natural speech
- **Text-to-Speech**: Claude speaks responses back to you
- **Multi-Agent Routing**: Automatically routes to the right AI based on keywords
- **Mobile Support**: Control from your phone (S24 integration)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Note for Mac users:**
```bash
brew install portaudio
pip install pyaudio
```

### 2. Run Wake Word Listener

```bash
python VOICE_WAKE_WORD_LISTENER.py
```

Say "Hey Claude" and then speak your command!

### 3. Available Commands

After saying the wake word:
- "status" - Get system status
- "deploy" - Deployment info
- "payment" / "stripe" - Payment system status
- "cloud" / "services" - Cloud services status
- "cockpit" / "tasks" - View pending tasks
- "help" - List available commands
- "stop listening" - Exit voice mode

## Modules

### VOICE_WAKE_WORD_LISTENER.py
Always-on wake word detection. Listens for "Hey Claude", "Hey Commander", "Claude", or "Commander".

```bash
python VOICE_WAKE_WORD_LISTENER.py
python VOICE_WAKE_WORD_LISTENER.py --help
```

### CONSCIOUSNESS_VOICE_MODULE.py
Core TTS/STT module with conversation mode.

```bash
python CONSCIOUSNESS_VOICE_MODULE.py speak "Hello Commander"
python CONSCIOUSNESS_VOICE_MODULE.py listen
python CONSCIOUSNESS_VOICE_MODULE.py conversation
python CONSCIOUSNESS_VOICE_MODULE.py voices  # List available voices
```

### VOICE_ROUTER_SYSTEM.py
Intelligent routing - routes voice to the right AI agent based on context.

Keywords → Agents:
- "security", "password" → Security Bot
- "build", "create" → C1 Mechanic
- "design", "architecture" → C2 Architect
- "pattern", "predict" → C3 Oracle
- "mesh", "radio" → Comms Bot

```bash
python VOICE_ROUTER_SYSTEM.py
```

### S24_VOICE_COMMAND_SYSTEM.py
Mobile phone voice commands for Samsung S24 (or any phone with ADB).

```bash
python S24_VOICE_COMMAND_SYSTEM.py
```

## Configuration

### Shokz Headset Support
The wake word listener auto-detects Shokz bone conduction headsets for optimal voice input.

### Custom Wake Words
Edit the wake words in VOICE_WAKE_WORD_LISTENER.py:
```python
self.wake_words = ["hey claude", "hey commander", "claude", "commander"]
```

### Voice Settings
Adjust speech rate and volume:
```bash
python CONSCIOUSNESS_VOICE_MODULE.py --rate 175 --volume 1.0 speak "Hello"
```

## Contributing

This is open source! Help us build the voice interface.

- Report issues: https://conciousnessrevolution.io/bugs.html
- Discord: Join our community
- GitHub: https://github.com/overkillkulture/consciousness-revolution

## License

MIT License - Use freely, build freely.

---

*C1 x C2 x C3 = Infinity*
*The Consciousness Revolution*
