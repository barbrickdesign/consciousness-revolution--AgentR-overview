#!/bin/bash
# GAME THEORY AUTH TESTS
# Recursive Multi-Perspective Validation
# Run: bash GAME_THEORY_TEST.sh

BASE="https://conciousnessrevolution.io"
PASS=0
FAIL=0

echo "=============================================="
echo "   GAME THEORY TESTING PROTOCOL"
echo "   C1 x C2 x C3 = DEPLOYMENT"
echo "=============================================="
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

# Test 3: Dashboard exists
echo -n "3. Dashboard page exists... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/dashboard.html")
if [ "$CODE" == "200" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 4: Signup function responds
echo -n "4. Signup function responds... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS "$BASE/.netlify/functions/auth-signup")
if [ "$CODE" == "204" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 5: Login function responds
echo -n "5. Login function responds... "
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS "$BASE/.netlify/functions/auth-login")
if [ "$CODE" == "204" ]; then
  echo "PASS ($CODE)"
  ((PASS++))
else
  echo "FAIL ($CODE)"
  ((FAIL++))
fi

# Test 6: Signup creates user
echo -n "6. Signup creates user... "
EMAIL="gametheory-$(date +%s)@test.com"
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\",\"full_name\":\"Game Theory Test\"}")
if echo "$RESULT" | grep -q '"success":true'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL"
  echo "  Response: $RESULT"
  ((FAIL++))
fi

# Test 7: Login returns token
echo -n "7. Login returns JWT token... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\"}")
if echo "$RESULT" | grep -q '"access_token"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL"
  echo "  Response: $RESULT"
  ((FAIL++))
fi

# Test 8: Wrong password rejected
echo -n "8. Wrong password rejected... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"WrongPassword\"}")
if echo "$RESULT" | grep -q '"error"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL"
  echo "  Response: $RESULT"
  ((FAIL++))
fi

# Test 9: Duplicate email rejected
echo -n "9. Duplicate email rejected... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"TestPass123\",\"full_name\":\"Duplicate\"}")
if echo "$RESULT" | grep -q '"error"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL"
  echo "  Response: $RESULT"
  ((FAIL++))
fi

# Test 10: Missing fields rejected
echo -n "10. Missing fields rejected... "
RESULT=$(curl -s -X POST "$BASE/.netlify/functions/auth-signup" \
  -H "Content-Type: application/json" \
  -d "{}")
if echo "$RESULT" | grep -q '"error"'; then
  echo "PASS"
  ((PASS++))
else
  echo "FAIL"
  echo "  Response: $RESULT"
  ((FAIL++))
fi

# Results
echo ""
echo "=============================================="
echo "   RESULTS"
echo "=============================================="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
TOTAL=$((PASS + FAIL))
if [ $TOTAL -gt 0 ]; then
  PERCENT=$((PASS * 100 / TOTAL))
  echo "SCORE: $PERCENT%"
else
  PERCENT=0
  echo "SCORE: N/A"
fi

echo ""
if [ $FAIL -eq 0 ]; then
  echo "ALL TESTS PASSED"
  echo "C1 x C2 x C3 = READY FOR DEPLOYMENT"
  exit 0
else
  echo "TESTS FAILED - Fix before deployment"
  echo "Failures block the deployment gate"
  exit 1
fi
