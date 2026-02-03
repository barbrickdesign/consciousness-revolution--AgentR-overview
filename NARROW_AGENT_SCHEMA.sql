-- ============================================================
-- NARROW AGENT SCHEMA
-- Verification System for Builder Economics
-- Created: 2026-01-10 | C2 Architect Design
-- Deploy: Run in Supabase SQL Editor AFTER BUILDER_ECONOMICS_SCHEMA.sql
-- ============================================================

-- ============================================================
-- PART 1: AGENT VERIFICATION TABLES
-- ============================================================

-- Agent Verification Events (All agent decisions)
CREATE TABLE IF NOT EXISTS agent_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type TEXT NOT NULL CHECK (agent_type IN (
        'quality', 'lineage', 'contribution', 'pattern'
    )),
    entity_type TEXT NOT NULL CHECK (entity_type IN (
        'creation', 'builder', 'contribution', 'transaction'
    )),
    entity_id UUID NOT NULL,
    entity_hash TEXT NOT NULL,  -- SHA256(entity_id + salt) for privacy
    result BOOLEAN NOT NULL,
    confidence REAL DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
    score REAL CHECK (score >= 0 AND score <= 100),
    evidence_hash TEXT NOT NULL,  -- SHA256 of evidence for auditability
    rule_version TEXT DEFAULT '1.0.0',
    flags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- PART 2: LOVE POD TABLES (Dispute Resolution)
-- ============================================================

-- Love Pod Disputes
CREATE TABLE IF NOT EXISTS love_pod_disputes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dispute_type TEXT NOT NULL CHECK (dispute_type IN (
        'quality', 'lineage', 'contribution', 'revenue', 'other'
    )),
    status TEXT DEFAULT 'open' CHECK (status IN (
        'open', 'evidence_gathering', 'witness_selection',
        'deliberation', 'resolved', 'appealed', 'expired'
    )),
    party_a_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    party_b_foundation_id UUID REFERENCES user_foundations(id),
    related_creation_id UUID REFERENCES builder_creations(id),
    related_transaction_id UUID REFERENCES revenue_events(id),
    party_a_claim TEXT NOT NULL,
    party_b_claim TEXT,
    party_a_evidence JSONB DEFAULT '{}',
    party_b_evidence JSONB DEFAULT '{}',
    agent_analysis JSONB DEFAULT '{}',
    outcome TEXT CHECK (outcome IN (
        'party_a_wins', 'party_b_wins', 'compromise', 'dismissed', 'expired'
    )),
    outcome_reason TEXT,
    outcome_evidence_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    evidence_deadline TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),
    resolution_deadline TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '14 days'),
    resolved_at TIMESTAMPTZ
);

-- Love Pod Witnesses
CREATE TABLE IF NOT EXISTS love_pod_witnesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dispute_id UUID REFERENCES love_pod_disputes(id) ON DELETE CASCADE NOT NULL,
    witness_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    selection_weight REAL,  -- Based on consciousness_score at selection time
    vote TEXT DEFAULT 'pending' CHECK (vote IN (
        'party_a', 'party_b', 'compromise', 'abstain', 'pending'
    )),
    vote_reason TEXT,
    vote_evidence_hash TEXT,
    voted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(dispute_id, witness_foundation_id)
);

-- ============================================================
-- PART 3: GOVERNANCE TABLES
-- ============================================================

-- Agent Rules (Versioned, Evolvable)
CREATE TABLE IF NOT EXISTS agent_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type TEXT NOT NULL CHECK (agent_type IN (
        'quality', 'lineage', 'contribution', 'pattern'
    )),
    rule_name TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    rule_definition JSONB NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    activation_date TIMESTAMPTZ,
    deactivation_date TIMESTAMPTZ,
    proposal_id UUID,  -- Link to governance proposal if rule was voted on
    created_by UUID REFERENCES user_foundations(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_type, rule_name, rule_version)
);

-- Governance Proposals
CREATE TABLE IF NOT EXISTS governance_proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proposer_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    proposal_type TEXT NOT NULL CHECK (proposal_type IN (
        'rule_change', 'threshold_change', 'new_agent', 'process_change'
    )),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    proposed_changes JSONB NOT NULL,
    affected_agent TEXT,  -- Which agent this affects
    status TEXT DEFAULT 'draft' CHECK (status IN (
        'draft', 'discussion', 'voting', 'passed', 'failed',
        'implemented', 'rolled_back'
    )),
    discussion_start TIMESTAMPTZ,
    discussion_end TIMESTAMPTZ,
    voting_start TIMESTAMPTZ,
    voting_end TIMESTAMPTZ,
    votes_for INTEGER DEFAULT 0,
    votes_against INTEGER DEFAULT 0,
    votes_abstain INTEGER DEFAULT 0,
    vote_weight_for REAL DEFAULT 0,
    vote_weight_against REAL DEFAULT 0,
    min_participation_pct REAL DEFAULT 0.1,  -- 10% minimum participation
    approval_threshold_pct REAL DEFAULT 0.66,  -- 66% approval needed
    implementation_date TIMESTAMPTZ,
    rollback_date TIMESTAMPTZ,
    rollback_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Governance Votes
CREATE TABLE IF NOT EXISTS governance_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proposal_id UUID REFERENCES governance_proposals(id) ON DELETE CASCADE NOT NULL,
    voter_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    vote TEXT NOT NULL CHECK (vote IN ('for', 'against', 'abstain')),
    vote_weight REAL NOT NULL,  -- Based on voter's consciousness_score
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(proposal_id, voter_foundation_id)
);

-- ============================================================
-- PART 4: PATTERN TRACKING TABLES
-- ============================================================

-- Builder Pattern History (Daily Snapshots)
CREATE TABLE IF NOT EXISTS builder_pattern_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    snapshot_date DATE NOT NULL DEFAULT CURRENT_DATE,
    consciousness_score REAL NOT NULL CHECK (consciousness_score >= 0 AND consciousness_score <= 1),
    pattern_classification TEXT CHECK (pattern_classification IN (
        'exemplary', 'builder', 'neutral', 'warning', 'destroyer'
    )),

    -- Builder Indicators
    value_created_cents INTEGER DEFAULT 0,
    collaborations_count INTEGER DEFAULT 0,
    quality_avg REAL DEFAULT 0,
    rating_avg REAL DEFAULT 0,
    downstream_creations INTEGER DEFAULT 0,

    -- Destroyer Indicators
    value_taken_cents INTEGER DEFAULT 0,
    disputes_initiated INTEGER DEFAULT 0,
    contributions_flagged INTEGER DEFAULT 0,
    rating_trend REAL DEFAULT 0,  -- Negative = declining

    -- Computed
    extraction_ratio REAL DEFAULT 0,  -- take / (take + create)

    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(foundation_id, snapshot_date)
);

-- Gaming Detection Log
CREATE TABLE IF NOT EXISTS gaming_detection_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    detection_type TEXT NOT NULL CHECK (detection_type IN (
        'rapid_fire', 'self_plagiarism', 'artificial_bug', 'sybil',
        'timing_anomaly', 'similarity_match', 'bot_behavior'
    )),
    severity TEXT DEFAULT 'warning' CHECK (severity IN (
        'info', 'warning', 'flag', 'block'
    )),
    evidence_hash TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by UUID REFERENCES user_foundations(id),
    reviewed_at TIMESTAMPTZ,
    review_outcome TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- PART 5: INDEXES
-- ============================================================

-- Agent Verifications
CREATE INDEX IF NOT EXISTS idx_verifications_agent ON agent_verifications(agent_type);
CREATE INDEX IF NOT EXISTS idx_verifications_entity ON agent_verifications(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_verifications_created ON agent_verifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_verifications_result ON agent_verifications(result);

-- Love Pod Disputes
CREATE INDEX IF NOT EXISTS idx_disputes_status ON love_pod_disputes(status);
CREATE INDEX IF NOT EXISTS idx_disputes_party_a ON love_pod_disputes(party_a_foundation_id);
CREATE INDEX IF NOT EXISTS idx_disputes_party_b ON love_pod_disputes(party_b_foundation_id);
CREATE INDEX IF NOT EXISTS idx_disputes_creation ON love_pod_disputes(related_creation_id);
CREATE INDEX IF NOT EXISTS idx_disputes_deadline ON love_pod_disputes(resolution_deadline) WHERE status NOT IN ('resolved', 'expired');

-- Love Pod Witnesses
CREATE INDEX IF NOT EXISTS idx_witnesses_dispute ON love_pod_witnesses(dispute_id);
CREATE INDEX IF NOT EXISTS idx_witnesses_foundation ON love_pod_witnesses(witness_foundation_id);
CREATE INDEX IF NOT EXISTS idx_witnesses_pending ON love_pod_witnesses(vote) WHERE vote = 'pending';

-- Agent Rules
CREATE INDEX IF NOT EXISTS idx_rules_agent ON agent_rules(agent_type);
CREATE INDEX IF NOT EXISTS idx_rules_active ON agent_rules(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_rules_name ON agent_rules(rule_name);

-- Governance
CREATE INDEX IF NOT EXISTS idx_proposals_status ON governance_proposals(status);
CREATE INDEX IF NOT EXISTS idx_proposals_voting ON governance_proposals(voting_end) WHERE status = 'voting';
CREATE INDEX IF NOT EXISTS idx_proposals_proposer ON governance_proposals(proposer_foundation_id);

CREATE INDEX IF NOT EXISTS idx_votes_proposal ON governance_votes(proposal_id);
CREATE INDEX IF NOT EXISTS idx_votes_voter ON governance_votes(voter_foundation_id);

-- Pattern History
CREATE INDEX IF NOT EXISTS idx_pattern_foundation ON builder_pattern_history(foundation_id);
CREATE INDEX IF NOT EXISTS idx_pattern_date ON builder_pattern_history(snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_pattern_score ON builder_pattern_history(consciousness_score);
CREATE INDEX IF NOT EXISTS idx_pattern_class ON builder_pattern_history(pattern_classification);

-- Gaming Detection
CREATE INDEX IF NOT EXISTS idx_gaming_foundation ON gaming_detection_log(foundation_id);
CREATE INDEX IF NOT EXISTS idx_gaming_type ON gaming_detection_log(detection_type);
CREATE INDEX IF NOT EXISTS idx_gaming_severity ON gaming_detection_log(severity);
CREATE INDEX IF NOT EXISTS idx_gaming_unreviewed ON gaming_detection_log(reviewed) WHERE reviewed = false;

-- ============================================================
-- PART 6: ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE agent_verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE love_pod_disputes ENABLE ROW LEVEL SECURITY;
ALTER TABLE love_pod_witnesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE governance_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE governance_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE builder_pattern_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE gaming_detection_log ENABLE ROW LEVEL SECURITY;

-- Verifications: Visible to entity owner
CREATE POLICY "verification_owner_select"
    ON agent_verifications FOR SELECT
    USING (
        entity_id IN (
            SELECT id FROM builder_creations WHERE foundation_id IN (
                SELECT id FROM user_foundations WHERE user_id = auth.uid()
            )
        )
        OR entity_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Disputes: Visible to parties and witnesses
CREATE POLICY "dispute_party_select"
    ON love_pod_disputes FOR SELECT
    USING (
        party_a_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR party_b_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR id IN (
            SELECT dispute_id FROM love_pod_witnesses
            WHERE witness_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        )
    );

-- Disputes: Parties can update their evidence
CREATE POLICY "dispute_party_update"
    ON love_pod_disputes FOR UPDATE
    USING (
        party_a_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR party_b_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    )
    WITH CHECK (
        party_a_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR party_b_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- Witnesses: Own votes visible
CREATE POLICY "witness_self_select"
    ON love_pod_witnesses FOR SELECT
    USING (
        witness_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR dispute_id IN (
            SELECT id FROM love_pod_disputes
            WHERE party_a_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
            OR party_b_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        )
    );

-- Witnesses: Can update own vote
CREATE POLICY "witness_self_update"
    ON love_pod_witnesses FOR UPDATE
    USING (
        witness_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    )
    WITH CHECK (
        witness_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- Rules: Active rules publicly visible
CREATE POLICY "rules_public_select"
    ON agent_rules FOR SELECT
    USING (is_active = true);

-- Proposals: Non-draft proposals publicly visible
CREATE POLICY "proposals_public_select"
    ON governance_proposals FOR SELECT
    USING (status != 'draft');

-- Proposals: Proposer can update drafts
CREATE POLICY "proposals_proposer_update"
    ON governance_proposals FOR UPDATE
    USING (
        proposer_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        AND status = 'draft'
    );

-- Votes: Own votes visible
CREATE POLICY "votes_self_select"
    ON governance_votes FOR SELECT
    USING (
        voter_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- Votes: Can cast own vote
CREATE POLICY "votes_self_insert"
    ON governance_votes FOR INSERT
    WITH CHECK (
        voter_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- Pattern History: Own history visible
CREATE POLICY "pattern_self_select"
    ON builder_pattern_history FOR SELECT
    USING (
        foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- Gaming Log: Own logs visible
CREATE POLICY "gaming_self_select"
    ON gaming_detection_log FOR SELECT
    USING (
        foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
    );

-- ============================================================
-- PART 7: FUNCTIONS
-- ============================================================

-- Calculate consciousness score from indicators
CREATE OR REPLACE FUNCTION calculate_consciousness_score(
    p_value_created INTEGER,
    p_value_taken INTEGER,
    p_collaborations INTEGER,
    p_quality_avg REAL,
    p_rating_avg REAL,
    p_downstream INTEGER,
    p_disputes INTEGER,
    p_flagged INTEGER
)
RETURNS REAL AS $$
DECLARE
    builder_score REAL := 0;
    destroyer_score REAL := 0;
    total_value INTEGER;
    extraction_ratio REAL;
BEGIN
    total_value := p_value_created + p_value_taken;

    -- Calculate extraction ratio
    IF total_value > 0 THEN
        extraction_ratio := p_value_taken::REAL / total_value;
    ELSE
        extraction_ratio := 0;
    END IF;

    -- Builder indicators (positive)
    builder_score := builder_score + LEAST(p_collaborations * 0.05, 0.2);  -- Max 0.2 from collaborations
    builder_score := builder_score + (p_quality_avg / 100) * 0.2;  -- Quality contributes up to 0.2
    builder_score := builder_score + (p_rating_avg / 5) * 0.15;  -- Rating contributes up to 0.15
    builder_score := builder_score + LEAST(p_downstream * 0.02, 0.15);  -- Downstream up to 0.15

    -- Destroyer indicators (negative)
    destroyer_score := destroyer_score + LEAST(extraction_ratio * 0.3, 0.3);  -- Extraction up to -0.3
    destroyer_score := destroyer_score + LEAST(p_disputes * 0.08, 0.25);  -- Disputes up to -0.25
    destroyer_score := destroyer_score + LEAST(p_flagged * 0.1, 0.25);  -- Flags up to -0.25

    -- Calculate final score (0.5 base + builder - destroyer)
    RETURN GREATEST(0, LEAST(1, 0.5 + builder_score - destroyer_score));
END;
$$ LANGUAGE plpgsql;

-- Classify pattern from consciousness score
CREATE OR REPLACE FUNCTION classify_pattern(p_score REAL)
RETURNS TEXT AS $$
BEGIN
    CASE
        WHEN p_score >= 0.9 THEN RETURN 'exemplary';
        WHEN p_score >= 0.7 THEN RETURN 'builder';
        WHEN p_score >= 0.5 THEN RETURN 'neutral';
        WHEN p_score >= 0.3 THEN RETURN 'warning';
        ELSE RETURN 'destroyer';
    END CASE;
END;
$$ LANGUAGE plpgsql;

-- Record daily pattern snapshot
CREATE OR REPLACE FUNCTION record_pattern_snapshot(p_foundation_id UUID)
RETURNS builder_pattern_history AS $$
DECLARE
    v_result builder_pattern_history;
    v_value_created INTEGER;
    v_value_taken INTEGER;
    v_collaborations INTEGER;
    v_quality_avg REAL;
    v_rating_avg REAL;
    v_downstream INTEGER;
    v_disputes INTEGER;
    v_flagged INTEGER;
    v_score REAL;
BEGIN
    -- Aggregate 30-day metrics
    SELECT COALESCE(SUM(builder_amount_cents), 0) INTO v_value_created
    FROM revenue_events
    WHERE seller_foundation_id = p_foundation_id
    AND created_at > NOW() - INTERVAL '30 days';

    SELECT COALESCE(SUM(gross_amount_cents), 0) INTO v_value_taken
    FROM revenue_events
    WHERE buyer_foundation_id = p_foundation_id
    AND created_at > NOW() - INTERVAL '30 days';

    SELECT COUNT(DISTINCT cl.parent_foundation_id) INTO v_collaborations
    FROM creation_lineage cl
    JOIN builder_creations bc ON cl.child_creation_id = bc.id
    WHERE bc.foundation_id = p_foundation_id
    AND cl.created_at > NOW() - INTERVAL '30 days';

    SELECT COALESCE(AVG(av.score), 50) INTO v_quality_avg
    FROM agent_verifications av
    WHERE av.entity_id IN (SELECT id FROM builder_creations WHERE foundation_id = p_foundation_id)
    AND av.agent_type = 'quality'
    AND av.created_at > NOW() - INTERVAL '30 days';

    SELECT COALESCE(AVG(rating_avg), 3) INTO v_rating_avg
    FROM builder_creations
    WHERE foundation_id = p_foundation_id
    AND rating_count > 0;

    SELECT COUNT(*) INTO v_downstream
    FROM creation_lineage cl
    WHERE cl.parent_foundation_id = p_foundation_id
    AND cl.created_at > NOW() - INTERVAL '30 days';

    SELECT COUNT(*) INTO v_disputes
    FROM love_pod_disputes
    WHERE party_a_foundation_id = p_foundation_id
    AND created_at > NOW() - INTERVAL '30 days';

    SELECT COUNT(*) INTO v_flagged
    FROM gaming_detection_log
    WHERE foundation_id = p_foundation_id
    AND severity IN ('flag', 'block')
    AND created_at > NOW() - INTERVAL '30 days';

    -- Calculate score
    v_score := calculate_consciousness_score(
        v_value_created, v_value_taken, v_collaborations,
        v_quality_avg, v_rating_avg, v_downstream,
        v_disputes, v_flagged
    );

    -- Insert or update snapshot
    INSERT INTO builder_pattern_history (
        foundation_id, snapshot_date, consciousness_score, pattern_classification,
        value_created_cents, collaborations_count, quality_avg, rating_avg, downstream_creations,
        value_taken_cents, disputes_initiated, contributions_flagged, extraction_ratio
    ) VALUES (
        p_foundation_id, CURRENT_DATE, v_score, classify_pattern(v_score),
        v_value_created, v_collaborations, v_quality_avg, v_rating_avg, v_downstream,
        v_value_taken, v_disputes, v_flagged,
        CASE WHEN (v_value_created + v_value_taken) > 0
            THEN v_value_taken::REAL / (v_value_created + v_value_taken)
            ELSE 0
        END
    )
    ON CONFLICT (foundation_id, snapshot_date)
    DO UPDATE SET
        consciousness_score = EXCLUDED.consciousness_score,
        pattern_classification = EXCLUDED.pattern_classification,
        value_created_cents = EXCLUDED.value_created_cents,
        collaborations_count = EXCLUDED.collaborations_count,
        quality_avg = EXCLUDED.quality_avg,
        rating_avg = EXCLUDED.rating_avg,
        downstream_creations = EXCLUDED.downstream_creations,
        value_taken_cents = EXCLUDED.value_taken_cents,
        disputes_initiated = EXCLUDED.disputes_initiated,
        contributions_flagged = EXCLUDED.contributions_flagged,
        extraction_ratio = EXCLUDED.extraction_ratio
    RETURNING * INTO v_result;

    -- Update consciousness_score on builder_creations
    UPDATE builder_creations
    SET consciousness_score = v_score
    WHERE foundation_id = p_foundation_id;

    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Select witnesses for a dispute
CREATE OR REPLACE FUNCTION select_dispute_witnesses(
    p_dispute_id UUID,
    p_count INTEGER DEFAULT 3
)
RETURNS SETOF love_pod_witnesses AS $$
DECLARE
    v_dispute love_pod_disputes;
    v_witness RECORD;
BEGIN
    -- Get dispute details
    SELECT * INTO v_dispute FROM love_pod_disputes WHERE id = p_dispute_id;

    -- Select eligible witnesses
    FOR v_witness IN
        SELECT uf.id, bph.consciousness_score
        FROM user_foundations uf
        JOIN builder_pattern_history bph ON uf.id = bph.foundation_id
        WHERE bph.snapshot_date = (
            SELECT MAX(snapshot_date) FROM builder_pattern_history WHERE foundation_id = uf.id
        )
        -- Eligibility criteria
        AND uf.created_at < NOW() - INTERVAL '90 days'  -- Account age > 90 days
        AND bph.consciousness_score > 0.6  -- Good standing
        AND uf.id != v_dispute.party_a_foundation_id
        AND uf.id != v_dispute.party_b_foundation_id
        -- Not already a witness
        AND uf.id NOT IN (SELECT witness_foundation_id FROM love_pod_witnesses WHERE dispute_id = p_dispute_id)
        -- Weighted random selection
        ORDER BY RANDOM() * bph.consciousness_score DESC
        LIMIT p_count
    LOOP
        INSERT INTO love_pod_witnesses (dispute_id, witness_foundation_id, selection_weight)
        VALUES (p_dispute_id, v_witness.id, v_witness.consciousness_score)
        RETURNING * INTO v_witness;

        RETURN NEXT v_witness;
    END LOOP;

    -- Update dispute status
    UPDATE love_pod_disputes
    SET status = 'witness_selection'
    WHERE id = p_dispute_id;

    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Resolve dispute based on votes
CREATE OR REPLACE FUNCTION resolve_dispute(p_dispute_id UUID)
RETURNS love_pod_disputes AS $$
DECLARE
    v_dispute love_pod_disputes;
    v_votes_a INTEGER;
    v_votes_b INTEGER;
    v_votes_compromise INTEGER;
    v_outcome TEXT;
BEGIN
    -- Count votes
    SELECT
        COUNT(*) FILTER (WHERE vote = 'party_a'),
        COUNT(*) FILTER (WHERE vote = 'party_b'),
        COUNT(*) FILTER (WHERE vote = 'compromise')
    INTO v_votes_a, v_votes_b, v_votes_compromise
    FROM love_pod_witnesses
    WHERE dispute_id = p_dispute_id
    AND vote != 'pending';

    -- Determine outcome
    IF v_votes_a > v_votes_b AND v_votes_a > v_votes_compromise THEN
        v_outcome := 'party_a_wins';
    ELSIF v_votes_b > v_votes_a AND v_votes_b > v_votes_compromise THEN
        v_outcome := 'party_b_wins';
    ELSIF v_votes_compromise >= v_votes_a AND v_votes_compromise >= v_votes_b THEN
        v_outcome := 'compromise';
    ELSE
        v_outcome := 'dismissed';  -- No clear majority
    END IF;

    -- Update dispute
    UPDATE love_pod_disputes
    SET
        status = 'resolved',
        outcome = v_outcome,
        outcome_reason = FORMAT('Votes: A=%s, B=%s, Compromise=%s', v_votes_a, v_votes_b, v_votes_compromise),
        resolved_at = NOW()
    WHERE id = p_dispute_id
    RETURNING * INTO v_dispute;

    RETURN v_dispute;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- PART 8: DEFAULT RULES
-- ============================================================

-- Insert default Quality Agent rules
INSERT INTO agent_rules (agent_type, rule_name, rule_version, rule_definition, description, is_active, activation_date)
VALUES
    ('quality', 'tests_pass', '1.0.0',
     '{"required": true, "threshold": 0.95, "evidence": "test_results.json"}'::JSONB,
     '95% of declared tests must pass', true, NOW()),
    ('quality', 'documentation_exists', '1.0.0',
     '{"required": true, "threshold": 0.7, "evidence": "docs_audit.json"}'::JSONB,
     '70% documentation coverage required', true, NOW()),
    ('quality', 'no_critical_errors', '1.0.0',
     '{"required": true, "threshold": 0, "evidence": "error_log.json"}'::JSONB,
     'Zero critical errors allowed', true, NOW()),
    ('quality', 'dependencies_declared', '1.0.0',
     '{"required": true, "threshold": 1.0, "evidence": "dependency_scan.json"}'::JSONB,
     'All dependencies must be declared', true, NOW())
ON CONFLICT (agent_type, rule_name, rule_version) DO NOTHING;

-- Insert default Lineage Agent rules
INSERT INTO agent_rules (agent_type, rule_name, rule_version, rule_definition, description, is_active, activation_date)
VALUES
    ('lineage', 'ability_usage_detection', '1.0.0',
     '{"method": "import_scan", "threshold": 1, "triggers": "auto_attribute"}'::JSONB,
     'Detect platform ability usage in creations', true, NOW()),
    ('lineage', 'parent_creation_detection', '1.0.0',
     '{"method": "dependency_analysis", "threshold": 0.1, "triggers": "lineage_link"}'::JSONB,
     'Detect when 10%+ functionality from parent', true, NOW())
ON CONFLICT (agent_type, rule_name, rule_version) DO NOTHING;

-- Insert default Contribution Agent rules
INSERT INTO agent_rules (agent_type, rule_name, rule_version, rule_definition, description, is_active, activation_date)
VALUES
    ('contribution', 'meaningful_change', '1.0.0',
     '{"min_lines": 5, "max_lines": 10000, "complexity_score": 0.3}'::JSONB,
     'Changes must be meaningful, not just formatting', true, NOW()),
    ('contribution', 'timing_check', '1.0.0',
     '{"min_hours": 0.1, "max_hours": 168, "anomaly_detection": true}'::JSONB,
     'Contribution timing must be reasonable', true, NOW()),
    ('contribution', 'uniqueness_check', '1.0.0',
     '{"duplicate_threshold": 0.8, "self_plagiarism_check": true}'::JSONB,
     'Contributions must be unique', true, NOW())
ON CONFLICT (agent_type, rule_name, rule_version) DO NOTHING;

-- Insert default Pattern Agent rules
INSERT INTO agent_rules (agent_type, rule_name, rule_version, rule_definition, description, is_active, activation_date)
VALUES
    ('pattern', 'extraction_threshold', '1.0.0',
     '{"threshold": 0.7, "action": "flag", "indicator_weight": -0.3}'::JSONB,
     'Flag when taking 70%+ of value', true, NOW()),
    ('pattern', 'dispute_threshold', '1.0.0',
     '{"threshold": 3, "window_days": 30, "action": "warning", "indicator_weight": -0.25}'::JSONB,
     'Warning at 3+ disputes in 30 days', true, NOW()),
    ('pattern', 'exemplary_threshold', '1.0.0',
     '{"min_score": 0.9, "action": "badge", "benefits": ["showcase", "priority_placement"]}'::JSONB,
     'Exemplary status at 0.9+ score', true, NOW())
ON CONFLICT (agent_type, rule_name, rule_version) DO NOTHING;

-- ============================================================
-- VERIFICATION
-- ============================================================

DO $$
BEGIN
    RAISE NOTICE 'Narrow Agent Schema created successfully!';
    RAISE NOTICE 'Tables: agent_verifications, love_pod_disputes, love_pod_witnesses';
    RAISE NOTICE 'Tables: agent_rules, governance_proposals, governance_votes';
    RAISE NOTICE 'Tables: builder_pattern_history, gaming_detection_log';
    RAISE NOTICE 'Functions: calculate_consciousness_score, classify_pattern';
    RAISE NOTICE 'Functions: record_pattern_snapshot, select_dispute_witnesses, resolve_dispute';
    RAISE NOTICE 'Default rules inserted for all 4 agent types';
    RAISE NOTICE 'Ready for deployment!';
END $$;
