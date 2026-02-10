---
applyTo: "*.html"
---

## HTML File Requirements for Consciousness Revolution

All HTML files must follow these standards for accessibility, consciousness-focused design, and healing impact.

### Standard HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Specific consciousness-focused description">
    <title>Tool Name - Consciousness Revolution</title>
    <link rel="stylesheet" href="css/sacred-theme.css">
    <link rel="stylesheet" href="css/responsive-system.css">
</head>
<body>
    <header>
        <nav role="navigation" aria-label="Main navigation">
            <a href="index.html" class="home-link">🏠 Home</a>
            <a href="araya-chat.html">Talk to ARAYA</a>
        </nav>
    </header>
    
    <main role="main">
        <h1>Primary Heading</h1>
        <section aria-labelledby="section-heading">
            <h2 id="section-heading">Section Title</h2>
            <!-- Content -->
        </section>
    </main>
    
    <footer role="contentinfo">
        <p>Consciousness Revolution | Healing through Awareness</p>
    </footer>
    
    <script src="js/your-script.js"></script>
</body>
</html>
```

### Consciousness-Focused Language

**Use empowering, healing language:**
- "Recognize patterns" (not "diagnose problems")
- "Healing journey" (not "treatment")
- "Develop consciousness" (not "fix yourself")
- "Pattern awareness" (not "what's wrong with you")

**Avoid:**
- Medical/diagnostic language
- Victim-blaming language
- Judgmental or shaming language
- Triggering descriptions

### Accessibility Requirements

1. **ARIA labels** - All interactive elements
```html
<button aria-label="Analyze conversation for patterns">Analyze</button>
<input type="text" id="input" aria-label="Enter conversation text" aria-describedby="help-text">
<p id="help-text">Your data stays private</p>
```

2. **Semantic HTML** - Proper structure
```html
<header>, <nav>, <main>, <section>, <article>, <aside>, <footer>
```

3. **Heading hierarchy** - No skipped levels
```html
<h1> → <h2> → <h3> (never skip from h1 to h3)
```

4. **Alt text** - All images
```html
<img src="pattern-diagram.png" alt="Diagram showing gaslighting pattern cycle">
```

### Mobile-First Design

1. **Viewport meta tag** - Required
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

2. **Touch-friendly** - Minimum 44x44px targets
```css
button, a { min-width: 44px; min-height: 44px; }
```

3. **Responsive images**
```html
<img src="image.jpg" alt="Description" loading="lazy" style="max-width: 100%; height: auto;">
```

### Sacred Geometry Theme

Always use the design system:
```html
<link rel="stylesheet" href="css/sacred-theme.css">
<link rel="stylesheet" href="css/responsive-system.css">
```

### Pattern Detector Template

For manipulation pattern detection tools:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern Name Detector - Consciousness Revolution</title>
    <link rel="stylesheet" href="css/sacred-theme.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.html">🏠 Home</a>
            <a href="PATTERN_LIBRARY.html">Pattern Library</a>
            <a href="araya-chat.html">Talk to ARAYA</a>
        </nav>
    </header>
    
    <main>
        <h1>[Pattern Name] Recognition Tool</h1>
        
        <section aria-labelledby="pattern-intro">
            <h2 id="pattern-intro">Understanding [Pattern]</h2>
            <p>Educational, non-judgmental explanation of the pattern.</p>
            
            <h3>Common Signs</h3>
            <ul>
                <li>Sign 1 with compassionate explanation</li>
                <li>Sign 2 with educational context</li>
                <li>Sign 3 with empowering language</li>
            </ul>
        </section>
        
        <section aria-labelledby="detector-section">
            <h2 id="detector-section">Analyze a Situation</h2>
            <form id="pattern-form" aria-label="Pattern analysis form">
                <label for="situation">
                    Describe the situation (your data stays private):
                </label>
                <textarea 
                    id="situation" 
                    aria-describedby="privacy-note"
                    rows="8"
                    required
                ></textarea>
                <p id="privacy-note" class="help-text">
                    This analysis happens privately and securely.
                </p>
                
                <button type="submit" aria-label="Analyze with compassion">
                    Analyze with Compassion
                </button>
            </form>
        </section>
        
        <section id="results" aria-live="polite" hidden>
            <h2>Insights</h2>
            <div id="results-content"></div>
            
            <h3>Healing Resources</h3>
            <ul>
                <li><a href="araya-chat.html">Talk to ARAYA about this pattern</a></li>
                <li><a href="PATTERN_LIBRARY.html">Learn about related patterns</a></li>
                <li><a href="seven-domains.html">Assess your 7 Domains</a></li>
            </ul>
        </section>
    </main>
    
    <footer>
        <p>Consciousness Revolution | You're not alone on this journey</p>
    </footer>
    
    <script src="js/pattern-detector.js"></script>
</body>
</html>
```

### ARAYA Integration Pages

For pages with ARAYA chat:

```html
<div id="araya-chat-container">
    <div id="messages" role="log" aria-live="polite" aria-label="Conversation history"></div>
    
    <form id="chat-form" aria-label="Chat with ARAYA">
        <label for="message-input" class="sr-only">Your message to ARAYA</label>
        <textarea 
            id="message-input" 
            aria-label="Type your message"
            placeholder="Share what's on your mind..."
            rows="3"
        ></textarea>
        
        <button type="submit" aria-label="Send message to ARAYA">
            Send
        </button>
    </form>
    
    <p class="help-text">
        ARAYA is here to listen with compassion and help you recognize patterns.
    </p>
</div>
```

### Stripe Integration

For payment/subscription pages:

```html
<!-- Load Stripe.js -->
<script src="https://js.stripe.com/v3/"></script>

<section id="pricing" aria-labelledby="pricing-heading">
    <h2 id="pricing-heading">Choose Your Path</h2>
    
    <div class="pricing-cards">
        <article class="pricing-card" aria-labelledby="seeker-title">
            <h3 id="seeker-title">Seeker</h3>
            <p class="price" aria-label="$10 per month">$10<span>/month</span></p>
            <ul>
                <li>Access to pattern library</li>
                <li>ARAYA conversations</li>
                <li>7 Domains assessment</li>
            </ul>
            <button 
                data-price-id="price_seeker"
                aria-label="Subscribe to Seeker plan"
            >
                Start Healing Journey
            </button>
        </article>
    </div>
</section>

<script>
// Initialize Stripe (use test keys in development)
const stripe = Stripe('pk_test_YOUR_KEY');

// Handle subscription
document.querySelectorAll('[data-price-id]').forEach(button => {
    button.addEventListener('click', async (e) => {
        const priceId = e.target.dataset.priceId;
        // Create checkout session...
    });
});
</script>
```

### Testing Checklist

Before submitting HTML changes:

- [ ] Validate HTML (W3C validator)
- [ ] Test in Chrome, Firefox, Safari, Edge
- [ ] Test on mobile (iOS Safari, Android Chrome)
- [ ] Verify all links work
- [ ] Check console for errors
- [ ] Test with screen reader if possible
- [ ] Verify keyboard navigation
- [ ] Check color contrast (WCAG AA)
- [ ] Test forms submit correctly
- [ ] Verify consciousness-focused language
- [ ] Ensure no triggering content
- [ ] Check sacred geometry theme applies

### Common Mistakes to Avoid

1. ❌ Missing viewport meta tag
2. ❌ Using diagnostic/medical language
3. ❌ Missing ARIA labels
4. ❌ Poor heading hierarchy
5. ❌ Broken links
6. ❌ Missing alt text
7. ❌ Judgmental or triggering language
8. ❌ Not mobile-friendly
9. ❌ Hard-coded API keys
10. ❌ Poor color contrast

### Remember

- **Every tool helps someone heal** - Language matters
- **Mobile-first always** - Most users on phones
- **Accessibility is love** - Everyone deserves access
- **Empathy in every word** - We're guiding healing journeys
- **Sacred geometry themes** - Respect the design system
