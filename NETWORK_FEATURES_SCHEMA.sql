-- ============================================================
-- NETWORK FEATURES SCHEMA
-- Add to Supabase alongside BUILDER_ECONOMICS_IMPLEMENTATION.md schema
-- Created: 2026-01-10
-- ============================================================

-- Builder Network Status
-- Tracks contribution score and tier for each builder
CREATE TABLE IF NOT EXISTS builder_network_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,

    -- Score and Tier
    contribution_score INTEGER DEFAULT 0,
    contribution_tier TEXT DEFAULT 'GHOST' CHECK (contribution_tier IN (
        'GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'
    )),

    -- Contribution Counters
    creations_published INTEGER DEFAULT 0,
    marketplace_sales INTEGER DEFAULT 0,
    downstream_derivatives INTEGER DEFAULT 0,
    bugs_reported INTEGER DEFAULT 0,
    patterns_shared INTEGER DEFAULT 0,
    community_help_given INTEGER DEFAULT 0,

    -- Activity Tracking
    last_network_activity TIMESTAMPTZ,
    network_features_enabled JSONB DEFAULT '[]',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(foundation_id)
);

-- Ability Access Control
-- Defines which abilities require network connection
CREATE TABLE IF NOT EXISTS ability_access_control (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ability_name TEXT NOT NULL UNIQUE,
    ability_category TEXT NOT NULL,

    -- Access Type: standalone (offline), network_enhanced (better online), network_required (online only)
    access_type TEXT NOT NULL CHECK (access_type IN (
        'standalone', 'network_enhanced', 'network_required'
    )),

    -- Minimum tier required (for network_required abilities)
    min_tier_required TEXT DEFAULT 'GHOST' CHECK (min_tier_required IN (
        'GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'
    )),

    -- For network_enhanced: percentage of power available offline
    offline_power_pct INTEGER DEFAULT 100 CHECK (offline_power_pct >= 0 AND offline_power_pct <= 100),

    -- Network features this ability uses
    network_features TEXT[] DEFAULT '{}',

    -- Description of degraded behavior when offline/low tier
    degraded_behavior TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Network Feature Access Log
-- Audit log of feature access attempts
CREATE TABLE IF NOT EXISTS network_feature_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id),
    feature_name TEXT NOT NULL,
    access_granted BOOLEAN NOT NULL,
    denial_reason TEXT,
    contribution_tier TEXT,
    contribution_score INTEGER,
    accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Shared Pattern Library
-- Community patterns (network-only feature)
CREATE TABLE IF NOT EXISTS shared_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contributor_id UUID REFERENCES user_foundations(id),
    pattern_name TEXT NOT NULL,
    pattern_type TEXT NOT NULL,
    pattern_data JSONB NOT NULL,
    description TEXT,
    tags TEXT[] DEFAULT '{}',
    usage_count INTEGER DEFAULT 0,
    quality_score FLOAT DEFAULT 0.5 CHECK (quality_score >= 0 AND quality_score <= 1),

    -- Visibility: local (contributor only), cell (cell members), network (all SAPLING+)
    visibility TEXT DEFAULT 'network' CHECK (visibility IN ('local', 'cell', 'network')),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_network_status_foundation ON builder_network_status(foundation_id);
CREATE INDEX IF NOT EXISTS idx_network_status_tier ON builder_network_status(contribution_tier);
CREATE INDEX IF NOT EXISTS idx_network_status_score ON builder_network_status(contribution_score DESC);

CREATE INDEX IF NOT EXISTS idx_ability_access_type ON ability_access_control(access_type);
CREATE INDEX IF NOT EXISTS idx_ability_access_tier ON ability_access_control(min_tier_required);

CREATE INDEX IF NOT EXISTS idx_feature_access_foundation ON network_feature_access(foundation_id);
CREATE INDEX IF NOT EXISTS idx_feature_access_time ON network_feature_access(accessed_at DESC);

CREATE INDEX IF NOT EXISTS idx_shared_patterns_type ON shared_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_shared_patterns_contributor ON shared_patterns(contributor_id);
CREATE INDEX IF NOT EXISTS idx_shared_patterns_visibility ON shared_patterns(visibility);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE builder_network_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE ability_access_control ENABLE ROW LEVEL SECURITY;
ALTER TABLE network_feature_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_patterns ENABLE ROW LEVEL SECURITY;

-- Builders see their own network status
CREATE POLICY "Builders see own network status"
    ON builder_network_status FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Anyone can read ability access rules
CREATE POLICY "Public reads ability access rules"
    ON ability_access_control FOR SELECT
    USING (TRUE);

-- Builders see their own access logs
CREATE POLICY "Builders see own access logs"
    ON network_feature_access FOR SELECT
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Pattern visibility based on tier and visibility setting
CREATE POLICY "Patterns visible to appropriate tiers"
    ON shared_patterns FOR SELECT
    USING (
        visibility = 'network' AND EXISTS (
            SELECT 1 FROM builder_network_status bns
            JOIN user_foundations uf ON bns.foundation_id = uf.id
            WHERE uf.user_id = auth.uid()
            AND bns.contribution_tier IN ('SAPLING', 'TREE', 'FOREST')
        )
        OR
        contributor_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Contributors can manage their patterns
CREATE POLICY "Contributors manage own patterns"
    ON shared_patterns FOR ALL
    USING (
        contributor_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- ============================================================
-- SEED DATA: Ability Access Rules
-- ============================================================

-- Type A: Standalone (100% offline)
INSERT INTO ability_access_control (ability_name, ability_category, access_type, min_tier_required, offline_power_pct, degraded_behavior) VALUES
('file_read', 'filesystem', 'standalone', 'GHOST', 100, NULL),
('file_write', 'filesystem', 'standalone', 'GHOST', 100, NULL),
('file_list', 'filesystem', 'standalone', 'GHOST', 100, NULL),
('file_search', 'filesystem', 'standalone', 'GHOST', 100, NULL),
('sqlite_query', 'database', 'standalone', 'GHOST', 100, NULL),
('sqlite_insert', 'database', 'standalone', 'GHOST', 100, NULL),
('sqlite_update', 'database', 'standalone', 'GHOST', 100, NULL),
('code_generate', 'generation', 'standalone', 'GHOST', 100, NULL),
('code_format', 'generation', 'standalone', 'GHOST', 100, NULL),
('text_transform', 'processing', 'standalone', 'GHOST', 100, NULL),
('json_parse', 'processing', 'standalone', 'GHOST', 100, NULL),
('template_render', 'generation', 'standalone', 'GHOST', 100, NULL),
('local_script', 'automation', 'standalone', 'GHOST', 100, NULL),
('batch_job', 'automation', 'standalone', 'GHOST', 100, NULL)
ON CONFLICT (ability_name) DO UPDATE SET
    access_type = EXCLUDED.access_type,
    offline_power_pct = EXCLUDED.offline_power_pct;

-- Type B: Network Enhanced (works offline, better connected)
INSERT INTO ability_access_control (ability_name, ability_category, access_type, min_tier_required, offline_power_pct, network_features, degraded_behavior) VALUES
('pattern_recognition', 'intelligence', 'network_enhanced', 'GHOST', 60, '{"pattern_library_read"}', 'Limited to 50 local patterns. Connect for 10,000+ community patterns.'),
('bug_detection', 'quality', 'network_enhanced', 'GHOST', 70, '{"bug_fixes_instant"}', 'Local lint rules only. Connect for 500K+ known issues database.'),
('code_analysis', 'quality', 'network_enhanced', 'GHOST', 80, '{"best_practices_db"}', 'Static analysis only. Connect for AI-powered analysis + best practices.'),
('documentation', 'generation', 'network_enhanced', 'GHOST', 70, '{"examples_library"}', 'Template-based generation. Connect for AI docs + 100K examples.'),
('testing', 'quality', 'network_enhanced', 'GHOST', 80, '{"test_case_sharing"}', 'Unit tests only. Connect for shared test cases + fuzzing.'),
('ai_assistance', 'intelligence', 'network_enhanced', 'SEEDLING', 50, '{"ai_model_access"}', 'Local LLM or rule-based. Connect for GPT-4/Claude.'),
('code_completion', 'intelligence', 'network_enhanced', 'SEEDLING', 60, '{"ai_model_access"}', 'Basic completion. Connect for advanced AI suggestions.'),
('search_codebase', 'intelligence', 'network_enhanced', 'GHOST', 70, '{"community_examples"}', 'Local search only. Connect for cross-project examples.')
ON CONFLICT (ability_name) DO UPDATE SET
    access_type = EXCLUDED.access_type,
    offline_power_pct = EXCLUDED.offline_power_pct,
    network_features = EXCLUDED.network_features,
    degraded_behavior = EXCLUDED.degraded_behavior;

-- Type C: Network Required (only works connected)
INSERT INTO ability_access_control (ability_name, ability_category, access_type, min_tier_required, offline_power_pct, network_features, degraded_behavior) VALUES
('marketplace_browse', 'marketplace', 'network_required', 'SEEDLING', 0, '{"marketplace_browse"}', NULL),
('marketplace_buy', 'marketplace', 'network_required', 'SAPLING', 0, '{"marketplace_buy"}', NULL),
('marketplace_sell', 'marketplace', 'network_required', 'SAPLING', 0, '{"marketplace_sell"}', NULL),
('marketplace_featured', 'marketplace', 'network_required', 'TREE', 0, '{"marketplace_featured"}', NULL),
('downstream_revenue', 'revenue', 'network_required', 'TREE', 0, '{"downstream_revenue"}', NULL),
('custom_revenue_terms', 'revenue', 'network_required', 'FOREST', 0, '{"custom_revenue_terms"}', NULL),
('pattern_library_read', 'community', 'network_required', 'SAPLING', 0, '{"pattern_library_read"}', NULL),
('pattern_library_write', 'community', 'network_required', 'TREE', 0, '{"pattern_library_write"}', NULL),
('community_help', 'support', 'network_required', 'SEEDLING', 0, '{"community_help"}', NULL),
('priority_support', 'support', 'network_required', 'TREE', 0, '{"priority_support"}', NULL),
('cell_creation', 'collaboration', 'network_required', 'TREE', 0, '{"cell_creation"}', NULL),
('cell_leadership', 'collaboration', 'network_required', 'FOREST', 0, '{"cell_leadership"}', NULL),
('full_api_access', 'enterprise', 'network_required', 'FOREST', 0, '{"full_api_access"}', NULL),
('white_label', 'enterprise', 'network_required', 'FOREST', 0, '{"white_label"}', NULL),
('beta_features', 'enterprise', 'network_required', 'TREE', 0, '{"beta_features"}', NULL),
('bug_fixes_instant', 'updates', 'network_required', 'SAPLING', 0, '{"bug_fixes_instant"}', NULL),
('version_updates', 'updates', 'network_required', 'SEEDLING', 0, '{"version_updates"}', NULL),
('cloud_ai_models', 'intelligence', 'network_required', 'SAPLING', 0, '{"ai_model_access"}', NULL),
('reputation_view', 'trust', 'network_required', 'SEEDLING', 0, '{"reputation_system"}', NULL),
('reputation_give', 'trust', 'network_required', 'SAPLING', 0, '{"reputation_system"}', NULL)
ON CONFLICT (ability_name) DO UPDATE SET
    access_type = EXCLUDED.access_type,
    min_tier_required = EXCLUDED.min_tier_required,
    network_features = EXCLUDED.network_features;

-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Function to calculate contribution tier from score
CREATE OR REPLACE FUNCTION calculate_contribution_tier(score INTEGER)
RETURNS TEXT AS $$
BEGIN
    IF score >= 500 THEN RETURN 'FOREST';
    ELSIF score >= 200 THEN RETURN 'TREE';
    ELSIF score >= 50 THEN RETURN 'SAPLING';
    ELSIF score >= 1 THEN RETURN 'SEEDLING';
    ELSE RETURN 'GHOST';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to update builder network status
CREATE OR REPLACE FUNCTION update_contribution_score(
    p_foundation_id UUID,
    p_points INTEGER,
    p_contribution_type TEXT DEFAULT 'general'
)
RETURNS JSONB AS $$
DECLARE
    v_current_score INTEGER;
    v_new_score INTEGER;
    v_current_tier TEXT;
    v_new_tier TEXT;
    v_result JSONB;
BEGIN
    -- Get or create status
    INSERT INTO builder_network_status (foundation_id, contribution_score, contribution_tier)
    VALUES (p_foundation_id, 0, 'GHOST')
    ON CONFLICT (foundation_id) DO NOTHING;

    -- Get current values
    SELECT contribution_score, contribution_tier
    INTO v_current_score, v_current_tier
    FROM builder_network_status
    WHERE foundation_id = p_foundation_id;

    -- Calculate new values
    v_new_score := v_current_score + p_points;
    v_new_tier := calculate_contribution_tier(v_new_score);

    -- Update status
    UPDATE builder_network_status
    SET
        contribution_score = v_new_score,
        contribution_tier = v_new_tier,
        last_network_activity = NOW(),
        updated_at = NOW()
    WHERE foundation_id = p_foundation_id;

    -- Build result
    v_result := jsonb_build_object(
        'previous_score', v_current_score,
        'new_score', v_new_score,
        'previous_tier', v_current_tier,
        'new_tier', v_new_tier,
        'tier_changed', v_current_tier != v_new_tier,
        'points_added', p_points
    );

    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- TRIGGERS
-- ============================================================

-- Auto-update tier when score changes
CREATE OR REPLACE FUNCTION auto_update_tier()
RETURNS TRIGGER AS $$
BEGIN
    NEW.contribution_tier := calculate_contribution_tier(NEW.contribution_score);
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_update_tier
    BEFORE UPDATE ON builder_network_status
    FOR EACH ROW
    WHEN (OLD.contribution_score IS DISTINCT FROM NEW.contribution_score)
    EXECUTE FUNCTION auto_update_tier();

-- ============================================================
-- VIEWS
-- ============================================================

-- View: Builder Network Dashboard
CREATE OR REPLACE VIEW builder_network_dashboard AS
SELECT
    bns.foundation_id,
    uf.email,
    bns.contribution_score,
    bns.contribution_tier,
    bns.creations_published,
    bns.marketplace_sales,
    bns.downstream_derivatives,
    bns.bugs_reported,
    bns.patterns_shared,
    bns.community_help_given,
    bns.last_network_activity,
    CASE bns.contribution_tier
        WHEN 'GHOST' THEN 1
        WHEN 'SEEDLING' THEN 50
        WHEN 'SAPLING' THEN 200
        WHEN 'TREE' THEN 500
        ELSE 0
    END - bns.contribution_score AS points_to_next_tier,
    jsonb_array_length(bns.network_features_enabled) AS features_unlocked
FROM builder_network_status bns
JOIN user_foundations uf ON bns.foundation_id = uf.id;

-- View: Ability Access Summary
CREATE OR REPLACE VIEW ability_access_summary AS
SELECT
    access_type,
    COUNT(*) as ability_count,
    array_agg(ability_name ORDER BY ability_name) as abilities
FROM ability_access_control
GROUP BY access_type;
