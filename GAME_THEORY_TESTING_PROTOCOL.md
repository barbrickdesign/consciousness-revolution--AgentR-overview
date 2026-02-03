# GAME THEORY TESTING PROTOCOL
## Recursive Multi-Perspective Validation System
## "No more beta testers - the system tests itself"

---

## CORE CONCEPT

Every feature is tested from 3 perspectives simultaneously:
- **C1 MECHANIC**: Does it work RIGHT NOW? (functionality)
- **C2 ARCHITECT**: Does it SCALE? (performance, security)
- **C3 ORACLE**: Does it ALIGN? (consciousness, UX)

Test failures from ANY perspective block deployment.

---

## AUTOMATED TEST MATRIX

### Level 1: EXISTENCE TESTS (Does it exist?)
| Test | Command | Expected |
|------|---------|----------|
| Signup page loads | `curl -I https://conciousnessrevolution.io/signup.html` | 200 |
| Login page loads | `curl -I https://conciousnessrevolution.io/login.html` | 200 |
| Dashboard page loads | `curl -I https://conciousnessrevolution.io/dashboard.html` | 200 |
| Auth signup function | `curl -I https://conciousnessrevolution.io/.netlify/functions/auth-signup` | 204 (OPTIONS) |
| Auth login function | `curl -I https://conciousnessrevolution.io/.netlify/functions/auth-login` | 204 (OPTIONS) |

### Level 2: FUNCTIONALITY TESTS (Does it work?)
| Test | Method | Expected |
|------|--------|----------|
| Signup creates user | POST /auth-signup | `{"success":true}` |
| Login returns token | POST /auth-login | `{"session":{...}}` |
| Invalid email rejected | POST /auth-signup (bad email) | `{"error":"Invalid email"}` |
| Wrong password rejected | POST /auth-login (wrong pw) | `{"error":"Invalid email or password"}` |
| Duplicate email rejected | POST /auth-signup (existing) | `{"error":"already registered"}` |

### Level 3: FLOW TESTS (Does the journey work?)
| Test | Steps | Expected |
|------|-------|----------|
| Full signup flow | 1. Load signup 2. Submit form 3. Check redirect | Redirects to login.html |
| Full login flow | 1. Load login 2. Submit valid creds 3. Check redirect | Redirects to dashboard.html |
| Protected route | 1. Access dashboard without login | Redirects to login.html |

### Level 4: EDGE CASES (What breaks it?)
| Test | Input | Expected |
|------|-------|----------|
| Empty form submission | No email/password | Form validation error |
| Short password | 5 chars | "Password must be at least 8 characters" |
| SQL injection attempt | `'; DROP TABLE users;--` | Sanitized/rejected |
| XSS attempt | `<script>console.warn('xss')</script>` | Escaped/sanitized |

---

## C1 MECHANIC PERSPECTIVE (Implementation)

### Quick Health Check
```bash
# Run from 100X_DEPLOYMENT folder
curl -s -o /dev/null -w "%{http_code}" https://conciousnessrevolution.io/signup.html
curl -s -o /dev/null -w "%{http_code}" https://conciousnessrevolution.io/login.html
curl -s -o /dev/null -w "%{http_code}" https://conciousnessrevolution.io/.netlify/functions/auth-signup -X OPTIONS
```

### Test Signup
```bash
curl -X POST https://conciousnessrevolution.io/.netlify/functions/auth-signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test-$(date +%s)@example.com","password":"TestPass123","full_name":"Test"}'
```

### Test Login
```bash
curl -X POST https://conciousnessrevolution.io/.netlify/functions/auth-login \
  -H "Content-Type: application/json" \
  -d '{"email":"YOUR_TEST_EMAIL","password":"YOUR_PASSWORD"}'
```

---

## C2 ARCHITECT PERSPECTIVE (Scale)

### Performance Checks
| Metric | Target | How to Test |
|--------|--------|-------------|
| Page load time | <2s | Lighthouse or curl timing |
| API response time | <500ms | curl timing |
| Concurrent users | 100+ | Load test |
| Error rate | <1% | Monitor logs |

### Security Checks
| Check | Status | Method |
|-------|--------|--------|
| HTTPS enforced | Required | Check redirect |
| CORS configured | Required | Check headers |
| No secrets in client | Required | View source |
| Rate limiting | Recommended | Check 429 responses |
| Input sanitization | Required | Test SQL/XSS |

---

## C3 ORACLE PERSPECTIVE (Consciousness)

### UX Consciousness Checks
| Check | Question | Target |
|-------|----------|--------|
| Error clarity | Does user understand what went wrong? | 100% |
| Loading feedback | Does user know something is happening? | 100% |
| Success confirmation | Does user know it worked? | 100% |
| Next step clarity | Does user know what to do next? | 100% |

### Pattern Theory Alignment
| Element | Builder Pattern | Destroyer Pattern |
|---------|-----------------|-------------------|
| Error messages | Helpful, specific | Vague, blaming |
| Form validation | Real-time, friendly | After submit, harsh |
| Loading states | Visual progress | Frozen/unknown |
| Success states | Celebratory | Dismissive |

---

## AUTOMATED TEST SCRIPT

Save as `test-auth.sh`:

```bash
#!/bin/bash
# GAME THEORY AUTH TESTS
# Run: bash test-auth.sh

BASE="https://conciousnessrevolution.io"
PASS=0
FAIL=0

echo "=== GAME THEORY AUTH TESTS ==="
echo ""

# Test 1: Signup page exists
echo -n "1. Signup page exists... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/signup.html")
if [ "$CODE" == "200" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 2: Login page exists
echo -n "2. Login page exists... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/login.html")
if [ "$CODE" == "200" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 3: Signup function responds
echo -n "3. Signup function responds... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS "$BASE/.netlify/functions/auth-signup")
if [ "$CODE" == "204" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 4: Login function responds
echo -n "4. Login function responds... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS "$BASE/.netlify/functions/auth-login")
if [ "$CODE" == "204" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 5: Signup creates user
echo -n "5. Signup creates user... "
EMAIL="gametheory-$(date +%s)@test.com"
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\",\"full_name\":\"Game Theory\"}")
if echo "$RESULT" | grep -q '"success":true'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL ($RESULT)"
  ((FAIL++))
fi

# Test 6: Login returns token
echo -n "6. Login returns token... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\"}")
if echo "$RESULT" | grep -q '"access_token"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL ($RESULT)"
  ((FAIL++))
fi

# Test 7: Wrong password rejected
echo -n "7. Wrong password rejected... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"WrongPassword\"}")
if echo "$RESULT" | grep -q '"error"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL ($RESULT)"
  ((FAIL++))
fi

# Test 8: Duplicate email rejected
echo -n "8. Duplicate email rejected... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\",\"full_name\":\"Duplicate\"}")
if echo "$RESULT" | grep -q '"error"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL ($RESULT)"
  ((FAIL++))
fi

# Results
echo ""
echo "=== RESULTS ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
TOTAL=$((PASS + FAIL))
PERCENT=$((PASS * 100 / TOTAL))
echo "SCORE: $PERCENT%"

if [ $FAIL -eq 0 ]; then
  echo ""
  echo "ALL TESTS PASSED - Ready for deployment"
  exit 0
else
  echo ""
  echo "TESTS FAILED - Fix before deployment"
  exit 1
fi
```

---

## RECURSIVE IMPROVEMENT LOOP

When tests fail:
1. **Identify** - Which perspective caught it?
2. **Diagnose** - Root cause analysis
3. **Fix** - Minimal targeted fix
4. **Verify** - Run tests again
5. **Prevent** - Add regression test

The loop continues until ALL THREE PERSPECTIVES pass.

---

## DEPLOYMENT GATE

**Deployment is BLOCKED unless:**
- [ ] All Level 1 tests pass (existence)
- [ ] All Level 2 tests pass (functionality)
- [ ] All Level 3 tests pass (flows)
- [ ] C1 Mechanic approves (it works)
- [ ] C2 Architect approves (it scales)
- [ ] C3 Oracle approves (it aligns)

**Formula: C1 x C2 x C3 = DEPLOY**

If ANY perspective = 0, deployment = 0.

---

## RUN THE TESTS

```bash
# Quick version (copy-paste)
cd C:/Users/dwrek/100X_DEPLOYMENT
bash GAME_THEORY_TEST.sh

# Or manual verification
curl https://conciousnessrevolution.io/signup.html -I
curl https://conciousnessrevolution.io/login.html -I
```

---

Created: 2026-01-10
Purpose: Replace human beta testers with systematic multi-perspective testing
Pattern: C1 x C2 x C3 = Deployment
