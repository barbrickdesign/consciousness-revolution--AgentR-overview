# SCHEMA DEPLOYMENT GUIDE
## Run in Supabase SQL Editor - IN ORDER
## Created: 2026-01-10

---

## DEPLOYMENT ORDER (CRITICAL)

```
1. FOUNDATION_SCHEMA.sql    (user_foundations - required by all others)
2. BUILDER_ECONOMICS_SCHEMA.sql (marketplace, revenue, payouts)
3. NETWORK_FEATURES_SCHEMA.sql  (tier system, feature gating)
4. NARROW_AGENT_SCHEMA.sql      (verification, governance)
```

---

## QUICK DEPLOYMENT

### Step 1: Open Supabase SQL Editor
1. Go to https://supabase.com/dashboard
2. Select your project
3. Click "SQL Editor" in sidebar
4. Click "New Query"

### Step 2: Deploy Each Schema

Copy/paste each .sql file content and run:

```sql
-- Run these one at a time, wait for each to complete

-- 1. Foundation (FIRST)
-- Paste contents of FOUNDATION_SCHEMA.sql
-- Click "Run"

-- 2. Builder Economics
-- Paste contents of BUILDER_ECONOMICS_SCHEMA.sql
-- Click "Run"

-- 3. Network Features
-- Paste contents of NETWORK_FEATURES_SCHEMA.sql
-- Click "Run"

-- 4. Narrow Agents
-- Paste contents of NARROW_AGENT_SCHEMA.sql
-- Click "Run"
```

### Step 3: Verify Deployment

```sql
-- Check all tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Expected: 23+ tables including:
-- user_foundations, builder_creations, builder_balances,
-- builder_network_status, ability_access_control, etc.
```

### Step 4: Create Auth Trigger (Admin Required)

```sql
-- This auto-creates foundation when user signs up
-- Must be run with admin privileges
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION create_foundation_on_signup();
```

---

## TABLE SUMMARY

| Schema | Tables | Indexes | RLS Policies |
|--------|--------|---------|--------------|
| Foundation | 4 | 15 | 4 |
| Builder Economics | 10 | 20 | 10 |
| Network Features | 4 | 8 | 5 |
| Narrow Agents | 8 | 20 | 12 |
| **TOTAL** | **26** | **63** | **31** |

---

## POST-DEPLOYMENT VERIFICATION

```sql
-- 1. Check foundation creation works
INSERT INTO user_foundations (user_id, email, name)
VALUES (gen_random_uuid(), 'test@test.com', 'Test User')
RETURNING *;

-- 2. Check builder balance auto-created
SELECT * FROM builder_balances WHERE foundation_id = (
    SELECT id FROM user_foundations WHERE email = 'test@test.com'
);

-- 3. Check network status works
SELECT * FROM builder_network_status WHERE foundation_id = (
    SELECT id FROM user_foundations WHERE email = 'test@test.com'
);

-- 4. Cleanup test data
DELETE FROM user_foundations WHERE email = 'test@test.com';
```

---

## ROLLBACK (If Needed)

```sql
-- Drop in reverse order
DROP TABLE IF EXISTS gaming_detection_log CASCADE;
DROP TABLE IF EXISTS builder_pattern_history CASCADE;
DROP TABLE IF EXISTS governance_votes CASCADE;
DROP TABLE IF EXISTS governance_proposals CASCADE;
DROP TABLE IF EXISTS agent_rules CASCADE;
DROP TABLE IF EXISTS love_pod_witnesses CASCADE;
DROP TABLE IF EXISTS love_pod_disputes CASCADE;
DROP TABLE IF EXISTS agent_verifications CASCADE;
DROP TABLE IF EXISTS shared_patterns CASCADE;
DROP TABLE IF EXISTS network_feature_access CASCADE;
DROP TABLE IF EXISTS ability_access_control CASCADE;
DROP TABLE IF EXISTS builder_network_status CASCADE;
DROP TABLE IF EXISTS payout_history CASCADE;
DROP TABLE IF EXISTS creation_reviews CASCADE;
DROP TABLE IF EXISTS creation_usage CASCADE;
DROP TABLE IF EXISTS builder_balances CASCADE;
DROP TABLE IF EXISTS downstream_revenue CASCADE;
DROP TABLE IF EXISTS revenue_events CASCADE;
DROP TABLE IF EXISTS creation_lineage CASCADE;
DROP TABLE IF EXISTS builder_creations CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS user_foundations CASCADE;
```

---

## NEXT STEPS AFTER DEPLOYMENT

1. **Test with real Supabase auth user**
   - Sign up through your app
   - Verify foundation created
   - Check builder_balance created

2. **Add JWT verification to Netlify functions**
   - Start with ability-access.mjs
   - Use as template for others

3. **Wire up Stripe Connect**
   - Test create-connect-account.mjs
   - Verify webhook handling

4. **Set up monitoring**
   - Check Supabase dashboard
   - Enable Netlify analytics

---

*Deploy order matters. Foundation first, everything else depends on it.*
