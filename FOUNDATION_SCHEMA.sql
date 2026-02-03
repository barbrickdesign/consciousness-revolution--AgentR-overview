-- ============================================================
-- FOUNDATION SCHEMA
-- Core user identity tables - DEPLOY FIRST
-- Created: 2026-01-10 | C1 Mechanic Build
-- Deploy: Run in Supabase SQL Editor BEFORE any other schemas
-- ============================================================

-- ============================================================
-- PART 1: CORE USER TABLES
-- ============================================================

-- User Foundations (Core Identity)
-- Every user has exactly one foundation
CREATE TABLE IF NOT EXISTS user_foundations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

    -- Identity
    email TEXT NOT NULL,
    name TEXT,
    display_name TEXT,
    avatar_url TEXT,
    bio TEXT,

    -- Subscription Tier
    tier TEXT DEFAULT 'free' CHECK (tier IN (
        'free', 'builder', 'pro', 'enterprise'
    )),
    tier_expires_at TIMESTAMPTZ,

    -- Stripe Integration
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,

    -- Status
    status TEXT DEFAULT 'active' CHECK (status IN (
        'active', 'suspended', 'deleted'
    )),
    suspended_reason TEXT,

    -- Preferences
    preferences JSONB DEFAULT '{}',
    notification_settings JSONB DEFAULT '{
        "email_marketing": false,
        "email_product": true,
        "email_security": true
    }',

    -- Metadata
    referral_code TEXT UNIQUE,
    referred_by UUID REFERENCES user_foundations(id),
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_step INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ DEFAULT NOW(),

    -- Constraints
    UNIQUE(user_id),
    UNIQUE(email)
);

-- User Sessions (Activity Tracking)
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,

    -- Session Info
    session_token TEXT NOT NULL,
    device_type TEXT,
    ip_address INET,
    user_agent TEXT,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    -- Timestamps
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);

-- Audit Log (Security Compliance)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE SET NULL,

    -- Event Details
    event_type TEXT NOT NULL,
    event_category TEXT NOT NULL CHECK (event_category IN (
        'auth', 'data', 'billing', 'admin', 'system'
    )),
    resource_type TEXT,
    resource_id UUID,

    -- Context
    action TEXT NOT NULL,
    ip_address INET,
    user_agent TEXT,
    request_id TEXT,

    -- Data (Privacy-Safe)
    old_values JSONB,
    new_values JSONB,
    metadata JSONB DEFAULT '{}',

    -- Timestamp
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys (For Programmatic Access)
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,

    -- Key Details
    name TEXT NOT NULL,
    key_hash TEXT NOT NULL,  -- Store hash, not plaintext
    key_prefix TEXT NOT NULL,  -- First 8 chars for identification

    -- Permissions
    scopes TEXT[] DEFAULT '{}',

    -- Limits
    rate_limit_per_minute INTEGER DEFAULT 60,
    rate_limit_per_day INTEGER DEFAULT 10000,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMPTZ,
    use_count INTEGER DEFAULT 0,

    -- Expiration
    expires_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);

-- ============================================================
-- PART 2: INDEXES
-- ============================================================

-- User Foundations
CREATE INDEX IF NOT EXISTS idx_foundations_user ON user_foundations(user_id);
CREATE INDEX IF NOT EXISTS idx_foundations_email ON user_foundations(email);
CREATE INDEX IF NOT EXISTS idx_foundations_tier ON user_foundations(tier);
CREATE INDEX IF NOT EXISTS idx_foundations_status ON user_foundations(status);
CREATE INDEX IF NOT EXISTS idx_foundations_stripe ON user_foundations(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_foundations_referral ON user_foundations(referral_code);
CREATE INDEX IF NOT EXISTS idx_foundations_active ON user_foundations(last_active_at DESC);

-- User Sessions
CREATE INDEX IF NOT EXISTS idx_sessions_foundation ON user_sessions(foundation_id);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);

-- Audit Log
CREATE INDEX IF NOT EXISTS idx_audit_foundation ON audit_log(foundation_id);
CREATE INDEX IF NOT EXISTS idx_audit_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_category ON audit_log(event_category);
CREATE INDEX IF NOT EXISTS idx_audit_resource ON audit_log(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_request ON audit_log(request_id);

-- API Keys
CREATE INDEX IF NOT EXISTS idx_apikeys_foundation ON api_keys(foundation_id);
CREATE INDEX IF NOT EXISTS idx_apikeys_prefix ON api_keys(key_prefix);
CREATE INDEX IF NOT EXISTS idx_apikeys_active ON api_keys(is_active) WHERE is_active = true;

-- ============================================================
-- PART 3: ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE user_foundations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Users own their foundation
CREATE POLICY "Users own their foundation"
    ON user_foundations FOR ALL
    USING (user_id = auth.uid());

-- Users can see their sessions
CREATE POLICY "Users see own sessions"
    ON user_sessions FOR SELECT
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Users can see their audit log
CREATE POLICY "Users see own audit log"
    ON audit_log FOR SELECT
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Users manage their API keys
CREATE POLICY "Users manage own API keys"
    ON api_keys FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- ============================================================
-- PART 4: FUNCTIONS
-- ============================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_foundation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER foundation_updated_at
    BEFORE UPDATE ON user_foundations
    FOR EACH ROW EXECUTE FUNCTION update_foundation_timestamp();

-- Generate unique referral code
CREATE OR REPLACE FUNCTION generate_referral_code()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.referral_code IS NULL THEN
        NEW.referral_code = upper(substr(md5(random()::text), 1, 8));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER foundation_generate_referral
    BEFORE INSERT ON user_foundations
    FOR EACH ROW EXECUTE FUNCTION generate_referral_code();

-- Create foundation when user signs up
CREATE OR REPLACE FUNCTION create_foundation_on_signup()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_foundations (user_id, email)
    VALUES (NEW.id, NEW.email)
    ON CONFLICT (user_id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users (requires admin)
-- Run this separately with admin privileges:
-- CREATE TRIGGER on_auth_user_created
--     AFTER INSERT ON auth.users
--     FOR EACH ROW EXECUTE FUNCTION create_foundation_on_signup();

-- Log audit event
CREATE OR REPLACE FUNCTION log_audit_event(
    p_foundation_id UUID,
    p_event_type TEXT,
    p_event_category TEXT,
    p_action TEXT,
    p_resource_type TEXT DEFAULT NULL,
    p_resource_id UUID DEFAULT NULL,
    p_old_values JSONB DEFAULT NULL,
    p_new_values JSONB DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
    v_audit_id UUID;
BEGIN
    INSERT INTO audit_log (
        foundation_id, event_type, event_category, action,
        resource_type, resource_id, old_values, new_values, metadata
    ) VALUES (
        p_foundation_id, p_event_type, p_event_category, p_action,
        p_resource_type, p_resource_id, p_old_values, p_new_values, p_metadata
    )
    RETURNING id INTO v_audit_id;

    RETURN v_audit_id;
END;
$$ LANGUAGE plpgsql;

-- Get foundation by user
CREATE OR REPLACE FUNCTION get_foundation_by_user(p_user_id UUID)
RETURNS user_foundations AS $$
DECLARE
    v_foundation user_foundations;
BEGIN
    SELECT * INTO v_foundation
    FROM user_foundations
    WHERE user_id = p_user_id;

    RETURN v_foundation;
END;
$$ LANGUAGE plpgsql;

-- Update last active timestamp
CREATE OR REPLACE FUNCTION update_last_active(p_foundation_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE user_foundations
    SET last_active_at = NOW()
    WHERE id = p_foundation_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- PART 5: VIEWS
-- ============================================================

-- Foundation Summary (for dashboards)
CREATE OR REPLACE VIEW foundation_summary AS
SELECT
    f.id,
    f.email,
    f.name,
    f.display_name,
    f.tier,
    f.status,
    f.onboarding_completed,
    f.created_at,
    f.last_active_at,
    CASE
        WHEN f.last_active_at > NOW() - INTERVAL '1 day' THEN 'active'
        WHEN f.last_active_at > NOW() - INTERVAL '7 days' THEN 'recent'
        WHEN f.last_active_at > NOW() - INTERVAL '30 days' THEN 'inactive'
        ELSE 'dormant'
    END as activity_status,
    (SELECT COUNT(*) FROM user_sessions WHERE foundation_id = f.id AND is_active = true) as active_sessions,
    (SELECT COUNT(*) FROM api_keys WHERE foundation_id = f.id AND is_active = true) as active_api_keys
FROM user_foundations f;

-- ============================================================
-- VERIFICATION
-- ============================================================

DO $$
BEGIN
    RAISE NOTICE 'Foundation Schema created successfully!';
    RAISE NOTICE 'Tables: user_foundations, user_sessions, audit_log, api_keys';
    RAISE NOTICE 'Functions: log_audit_event, get_foundation_by_user, update_last_active';
    RAISE NOTICE 'Views: foundation_summary';
    RAISE NOTICE '';
    RAISE NOTICE 'IMPORTANT: Run this trigger separately with admin privileges:';
    RAISE NOTICE 'CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION create_foundation_on_signup();';
    RAISE NOTICE '';
    RAISE NOTICE 'Deploy order: FOUNDATION_SCHEMA.sql -> BUILDER_ECONOMICS_SCHEMA.sql -> NETWORK_FEATURES_SCHEMA.sql -> NARROW_AGENT_SCHEMA.sql';
END $$;
