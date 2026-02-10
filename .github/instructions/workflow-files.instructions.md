---
applyTo: ".github/workflows/*.yml"
---

## GitHub Actions Workflow Requirements for Consciousness Revolution

Workflows for CI/CD, testing, deployment, and automation with security and consciousness focus.

### Workflow Structure Standards

```yaml
name: Descriptive Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger

permissions:
  contents: read
  pull-requests: write

env:
  PYTHON_VERSION: '3.10'
  NODE_VERSION: '18'

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: python -m pytest
```

### Critical Workflows

#### 1. ARAYA System Test

Test ARAYA healing conversations and file access:

```yaml
name: Test ARAYA System

on:
  push:
    paths:
      - 'ARAYA_*.py'
      - 'araya-*.html'
  pull_request:
    paths:
      - 'ARAYA_*.py'
      - 'araya-*.html'

permissions:
  contents: read

jobs:
  test-araya:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Test ARAYA Bridge
        run: python TEST_ARAYA_SYSTEM.py
      
      - name: Test File Access
        run: python TEST_ARAYA_FILE_ACCESS.py
      
      - name: Verify Empathy Standards
        run: |
          # Check for non-empathetic language
          if grep -r "diagnose\|disorder\|dysfunction" ARAYA_*.py; then
            echo "::error::Found non-empathetic language in ARAYA files"
            exit 1
          fi
          echo "✅ ARAYA empathy standards verified"
```

#### 2. Pattern Detector Validation

Validate pattern detection tools for educational language:

```yaml
name: Validate Pattern Detectors

on:
  push:
    paths:
      - '*_DETECTOR.html'
      - 'PATTERN_*.html'
  pull_request:
    paths:
      - '*_DETECTOR.html'
      - 'PATTERN_*.html'

jobs:
  validate-patterns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for triggering language
        run: |
          # List of potentially triggering medical/diagnostic terms
          FORBIDDEN_TERMS="diagnose|disorder|dysfunction|mental illness|crazy|insane"
          
          if grep -riE "$FORBIDDEN_TERMS" *_DETECTOR.html; then
            echo "::error::Found potentially triggering language"
            exit 1
          fi
          echo "✅ No triggering language found"
      
      - name: Verify healing resources
        run: |
          # Check that each detector links to healing resources
          for file in *_DETECTOR.html; do
            if ! grep -q "araya-chat.html\|PATTERN_LIBRARY.html" "$file"; then
              echo "::error::$file missing healing resource links"
              exit 1
            fi
          done
          echo "✅ All detectors link to healing resources"
      
      - name: Check accessibility
        run: |
          # Verify ARIA labels present
          for file in *_DETECTOR.html; do
            if ! grep -q "aria-label" "$file"; then
              echo "::warning::$file may be missing ARIA labels"
            fi
          done
```

#### 3. Stripe Integration Test

Test payment integration safely:

```yaml
name: Test Stripe Integration

on:
  push:
    paths:
      - 'STRIPE_*.py'
      - 'pricing*.html'
  pull_request:
    paths:
      - 'STRIPE_*.py'
      - 'pricing*.html'

permissions:
  contents: read

jobs:
  test-stripe:
    runs-on: ubuntu-latest
    environment: test  # Use test environment
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Verify test mode
        run: |
          # Ensure using test keys
          if grep -r "sk_live_\|pk_live_" *.py *.html; then
            echo "::error::Live Stripe keys found in code!"
            exit 1
          fi
          echo "✅ No live keys in code"
      
      - name: Test checkout flow
        env:
          STRIPE_TEST_KEY: ${{ secrets.STRIPE_TEST_KEY }}
        run: |
          python -m pytest test_stripe_integration.py
```

#### 4. Accessibility Check

Verify WCAG compliance:

```yaml
name: Accessibility Check

on:
  push:
    paths:
      - '**.html'
  pull_request:
    paths:
      - '**.html'

jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install pa11y
        run: npm install -g pa11y-ci
      
      - name: Run accessibility tests
        run: |
          # Test key pages
          pa11y-ci \
            --threshold 10 \
            index.html \
            araya-chat.html \
            GASLIGHTING_DETECTOR.html \
            seven-domains.html
      
      - name: Check ARIA labels
        run: |
          for file in *.html; do
            if grep -q "<button\|<input\|<textarea" "$file"; then
              if ! grep -q "aria-label\|aria-labelledby" "$file"; then
                echo "::warning::$file may be missing ARIA labels"
              fi
            fi
          done
```

#### 5. Security Scan

Comprehensive security scanning:

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

permissions:
  contents: read
  security-events: write

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for secrets
        run: |
          # Check for common secret patterns
          if grep -rE "sk_live_|pk_live_|api[_-]?key.*=.*['\"][A-Za-z0-9]+" . --exclude-dir=node_modules; then
            echo "::error::Potential secret found in code"
            exit 1
          fi
      
      - name: Python security audit
        run: |
          pip install safety
          safety check --json
      
      - name: Dependency review
        uses: actions/dependency-review-action@v3
        if: github.event_name == 'pull_request'
```

#### 6. Deploy to Netlify

Deployment workflow:

```yaml
name: Deploy to Netlify

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run pre-deployment checks
        run: |
          # Verify no test keys in production
          if grep -r "test_\|sandbox" *.html *.py; then
            echo "::warning::Test/sandbox references found"
          fi
      
      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        with:
          args: deploy --prod
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
      
      - name: Verify deployment
        run: |
          # Check site is accessible
          response=$(curl -s -o /dev/null -w "%{http_code}" https://consciousness-revolution.netlify.app)
          if [ "$response" != "200" ]; then
            echo "::error::Deployment verification failed"
            exit 1
          fi
          echo "✅ Deployment verified"
```

### Best Practices

1. **Use secrets for sensitive data**
```yaml
env:
  STRIPE_KEY: ${{ secrets.STRIPE_TEST_KEY }}
  SUPABASE_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
```

2. **Pin action versions**
```yaml
# Good
- uses: actions/checkout@v4

# Avoid
- uses: actions/checkout@latest
```

3. **Add proper error handling**
```yaml
- name: Deploy with fallback
  run: |
    npm run deploy || {
      echo "::error::Deployment failed"
      npm run rollback
      exit 1
    }
```

4. **Use caching**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### Consciousness-Specific Checks

**Verify healing language:**
```yaml
- name: Check consciousness language
  run: |
    # Ensure empowering language used
    EMPOWERING_TERMS="recognize|awareness|healing|consciousness|empowerment"
    HARMFUL_TERMS="diagnose|disorder|dysfunction|broken|fix yourself"
    
    if grep -riE "$HARMFUL_TERMS" *.html *.py; then
      echo "::error::Found potentially harmful language"
      exit 1
    fi
```

**Test ARAYA empathy:**
```yaml
- name: Validate ARAYA empathy
  run: |
    python -c "
    import json
    with open('ARAYA_GUIDED_HEALING_FLOWS.json') as f:
        flows = json.load(f)
        for flow in flows:
            if 'empathy' not in flow or flow['empathy'] != 'high':
                print(f'::error::Flow {flow[\"id\"]} missing high empathy')
                exit(1)
    "
```

### Testing Requirements

Before deploying workflow:

- [ ] Test in feature branch first
- [ ] Verify secrets configured
- [ ] Check permissions are minimal
- [ ] Test failure scenarios
- [ ] Verify notifications work
- [ ] Check resource usage

### Security Checklist

- [ ] Use secrets for credentials
- [ ] Set minimal permissions
- [ ] Pin action versions
- [ ] No secrets in logs
- [ ] Validate external inputs
- [ ] Use trusted actions only

### Common Mistakes to Avoid

1. ❌ Using `@latest` for actions
2. ❌ Exposing secrets in logs
3. ❌ Too broad permissions
4. ❌ Not handling failures
5. ❌ Missing timeout settings
6. ❌ Hard-coding values
7. ❌ No rollback mechanism
8. ❌ Not testing before merge

### Remember

- **Test workflows in branches** - Don't break main
- **Consciousness language matters** - Verify empathy
- **Security first** - Never expose secrets
- **Healing-critical systems** - Extra validation
- **Monitor costs** - GitHub Actions has limits
- **Document everything** - Help future maintainers
