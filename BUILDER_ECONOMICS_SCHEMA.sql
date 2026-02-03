-- ============================================================
-- BUILDER ECONOMICS SCHEMA
-- Revenue Share + Marketplace + Downstream Tracking
-- Created: 2026-01-10 | C1 Mechanic Build
-- Deploy: Run in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- PART 1: CORE BUILDER ECONOMICS TABLES
-- ============================================================

-- Creations Registry (What Builders Make)
CREATE TABLE IF NOT EXISTS builder_creations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    slug TEXT UNIQUE,
    description TEXT,
    long_description TEXT,
    type TEXT NOT NULL CHECK (type IN (
        'ability', 'module', 'template', 'workflow',
        'integration', 'pattern', 'dataset', 'korpak'
    )),
    visibility TEXT DEFAULT 'private' CHECK (visibility IN (
        'private', 'cell', 'marketplace', 'open_source'
    )),
    status TEXT DEFAULT 'draft' CHECK (status IN (
        'draft', 'review', 'published', 'archived', 'suspended'
    )),
    source_abilities TEXT[] DEFAULT '{}',
    category TEXT,
    tags TEXT[] DEFAULT '{}',
    thumbnail_url TEXT,
    demo_url TEXT,
    documentation_url TEXT,
    stripe_product_id TEXT,
    stripe_price_id TEXT,
    base_price_cents INTEGER DEFAULT 0,
    revenue_share_pct INTEGER DEFAULT 80 CHECK (revenue_share_pct >= 50 AND revenue_share_pct <= 95),
    downstream_share_pct INTEGER DEFAULT 10 CHECK (downstream_share_pct >= 0 AND downstream_share_pct <= 30),
    total_sales INTEGER DEFAULT 0,
    total_revenue_cents INTEGER DEFAULT 0,
    rating_avg REAL DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    consciousness_score REAL DEFAULT 0.5,
    verification_status TEXT DEFAULT 'unverified' CHECK (verification_status IN (
        'unverified', 'pending', 'verified', 'flagged'
    )),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ,
    UNIQUE(foundation_id, name)
);

-- Creation Lineage (Who Built From What)
CREATE TABLE IF NOT EXISTS creation_lineage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_creation_id UUID REFERENCES builder_creations(id) ON DELETE CASCADE NOT NULL,
    parent_creation_id UUID REFERENCES builder_creations(id) ON DELETE SET NULL,
    parent_foundation_id UUID REFERENCES user_foundations(id),
    relationship TEXT DEFAULT 'derived' CHECK (relationship IN (
        'derived', 'extended', 'composed', 'inspired', 'forked'
    )),
    attribution_required BOOLEAN DEFAULT TRUE,
    revenue_share_active BOOLEAN DEFAULT TRUE,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Revenue Events (Every Money Movement)
CREATE TABLE IF NOT EXISTS revenue_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creation_id UUID REFERENCES builder_creations(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL CHECK (event_type IN (
        'sale', 'subscription', 'usage', 'downstream', 'refund', 'chargeback', 'tip'
    )),
    gross_amount_cents INTEGER NOT NULL,
    builder_amount_cents INTEGER NOT NULL,
    network_amount_cents INTEGER NOT NULL,
    downstream_amount_cents INTEGER DEFAULT 0,
    fees_cents INTEGER DEFAULT 0,
    buyer_foundation_id UUID REFERENCES user_foundations(id),
    seller_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    stripe_payment_id TEXT,
    stripe_transfer_id TEXT,
    stripe_refund_id TEXT,
    status TEXT DEFAULT 'completed' CHECK (status IN (
        'pending', 'completed', 'failed', 'refunded', 'disputed'
    )),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Downstream Revenue (Track Passive Income)
CREATE TABLE IF NOT EXISTS downstream_revenue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_creation_id UUID REFERENCES builder_creations(id) NOT NULL,
    derived_creation_id UUID REFERENCES builder_creations(id) NOT NULL,
    original_builder_id UUID REFERENCES user_foundations(id) NOT NULL,
    revenue_event_id UUID REFERENCES revenue_events(id) NOT NULL,
    amount_cents INTEGER NOT NULL,
    depth INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Builder Balances (Running Totals)
CREATE TABLE IF NOT EXISTS builder_balances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    available_balance_cents INTEGER DEFAULT 0,
    pending_balance_cents INTEGER DEFAULT 0,
    lifetime_earnings_cents INTEGER DEFAULT 0,
    lifetime_downstream_cents INTEGER DEFAULT 0,
    lifetime_network_fees_cents INTEGER DEFAULT 0,
    stripe_connect_id TEXT,
    stripe_connect_status TEXT DEFAULT 'not_connected' CHECK (stripe_connect_status IN (
        'not_connected', 'pending', 'active', 'restricted', 'disabled'
    )),
    payout_schedule TEXT DEFAULT 'weekly' CHECK (payout_schedule IN (
        'daily', 'weekly', 'monthly', 'manual'
    )),
    minimum_payout_cents INTEGER DEFAULT 1000,
    last_payout_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(foundation_id)
);

-- Usage Metering (For API-Based Revenue)
CREATE TABLE IF NOT EXISTS creation_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creation_id UUID REFERENCES builder_creations(id) ON DELETE CASCADE NOT NULL,
    user_foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    usage_type TEXT DEFAULT 'api_call' CHECK (usage_type IN (
        'api_call', 'download', 'view', 'execution', 'embed'
    )),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    billed BOOLEAN DEFAULT FALSE,
    billed_amount_cents INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(creation_id, user_foundation_id, usage_type, period_start)
);

-- Creation Reviews
CREATE TABLE IF NOT EXISTS creation_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creation_id UUID REFERENCES builder_creations(id) ON DELETE CASCADE NOT NULL,
    reviewer_foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title TEXT,
    body TEXT,
    helpful_count INTEGER DEFAULT 0,
    verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(creation_id, reviewer_foundation_id)
);

-- Payout History
CREATE TABLE IF NOT EXISTS payout_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    amount_cents INTEGER NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN (
        'pending', 'processing', 'completed', 'failed', 'cancelled'
    )),
    stripe_payout_id TEXT,
    stripe_transfer_id TEXT,
    arrival_date DATE,
    failure_reason TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- ============================================================
-- PART 2: INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_creations_foundation ON builder_creations(foundation_id);
CREATE INDEX IF NOT EXISTS idx_creations_visibility ON builder_creations(visibility);
CREATE INDEX IF NOT EXISTS idx_creations_type ON builder_creations(type);
CREATE INDEX IF NOT EXISTS idx_creations_status ON builder_creations(status);
CREATE INDEX IF NOT EXISTS idx_creations_slug ON builder_creations(slug);
CREATE INDEX IF NOT EXISTS idx_creations_stripe_product ON builder_creations(stripe_product_id);
CREATE INDEX IF NOT EXISTS idx_creations_published ON builder_creations(published_at DESC) WHERE visibility = 'marketplace';

CREATE INDEX IF NOT EXISTS idx_lineage_child ON creation_lineage(child_creation_id);
CREATE INDEX IF NOT EXISTS idx_lineage_parent ON creation_lineage(parent_creation_id);
CREATE INDEX IF NOT EXISTS idx_lineage_parent_foundation ON creation_lineage(parent_foundation_id);

CREATE INDEX IF NOT EXISTS idx_revenue_creation ON revenue_events(creation_id);
CREATE INDEX IF NOT EXISTS idx_revenue_seller ON revenue_events(seller_foundation_id);
CREATE INDEX IF NOT EXISTS idx_revenue_buyer ON revenue_events(buyer_foundation_id);
CREATE INDEX IF NOT EXISTS idx_revenue_created ON revenue_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_revenue_stripe ON revenue_events(stripe_payment_id);

CREATE INDEX IF NOT EXISTS idx_downstream_original ON downstream_revenue(original_creation_id);
CREATE INDEX IF NOT EXISTS idx_downstream_derived ON downstream_revenue(derived_creation_id);
CREATE INDEX IF NOT EXISTS idx_downstream_builder ON downstream_revenue(original_builder_id);

CREATE INDEX IF NOT EXISTS idx_balances_foundation ON builder_balances(foundation_id);
CREATE INDEX IF NOT EXISTS idx_balances_connect ON builder_balances(stripe_connect_id);

CREATE INDEX IF NOT EXISTS idx_usage_creation ON creation_usage(creation_id);
CREATE INDEX IF NOT EXISTS idx_usage_user ON creation_usage(user_foundation_id);
CREATE INDEX IF NOT EXISTS idx_usage_period ON creation_usage(period_start, period_end);

CREATE INDEX IF NOT EXISTS idx_reviews_creation ON creation_reviews(creation_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON creation_reviews(rating);

CREATE INDEX IF NOT EXISTS idx_payouts_foundation ON payout_history(foundation_id);
CREATE INDEX IF NOT EXISTS idx_payouts_status ON payout_history(status);

-- ============================================================
-- PART 3: ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE builder_creations ENABLE ROW LEVEL SECURITY;
ALTER TABLE creation_lineage ENABLE ROW LEVEL SECURITY;
ALTER TABLE revenue_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE downstream_revenue ENABLE ROW LEVEL SECURITY;
ALTER TABLE builder_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE creation_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE creation_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE payout_history ENABLE ROW LEVEL SECURITY;

-- Creators can manage their creations
CREATE POLICY "Creators own their creations"
    ON builder_creations FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Anyone can see published marketplace items
CREATE POLICY "Public sees marketplace creations"
    ON builder_creations FOR SELECT
    USING (visibility = 'marketplace' AND status = 'published');

-- Lineage visible to involved parties
CREATE POLICY "Lineage visible to parent and child"
    ON creation_lineage FOR SELECT
    USING (
        parent_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR child_creation_id IN (
            SELECT id FROM builder_creations WHERE foundation_id IN (
                SELECT id FROM user_foundations WHERE user_id = auth.uid()
            )
        )
    );

-- Builders see their revenue
CREATE POLICY "Builders see their revenue"
    ON revenue_events FOR SELECT
    USING (
        seller_foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Builders see their downstream
CREATE POLICY "Builders see their downstream"
    ON downstream_revenue FOR SELECT
    USING (
        original_builder_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Builders manage their balance
CREATE POLICY "Builders manage their balance"
    ON builder_balances FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Usage visible to creation owner and user
CREATE POLICY "Usage visible to owner and user"
    ON creation_usage FOR SELECT
    USING (
        user_foundation_id IN (SELECT id FROM user_foundations WHERE user_id = auth.uid())
        OR creation_id IN (
            SELECT id FROM builder_creations WHERE foundation_id IN (
                SELECT id FROM user_foundations WHERE user_id = auth.uid()
            )
        )
    );

-- Reviews visible to all, editable by author
CREATE POLICY "Reviews publicly visible"
    ON creation_reviews FOR SELECT
    USING (true);

CREATE POLICY "Reviewers edit their reviews"
    ON creation_reviews FOR ALL
    USING (
        reviewer_foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Payout history visible to owner
CREATE POLICY "Payouts visible to owner"
    ON payout_history FOR SELECT
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- ============================================================
-- PART 4: FUNCTIONS
-- ============================================================

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_creation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER creation_updated_at
    BEFORE UPDATE ON builder_creations
    FOR EACH ROW EXECUTE FUNCTION update_creation_timestamp();

-- Generate slug from name
CREATE OR REPLACE FUNCTION generate_creation_slug()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.slug IS NULL OR NEW.slug = '' THEN
        NEW.slug = lower(regexp_replace(NEW.name, '[^a-zA-Z0-9]+', '-', 'g'))
            || '-' || substr(NEW.id::text, 1, 8);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER creation_generate_slug
    BEFORE INSERT ON builder_creations
    FOR EACH ROW EXECUTE FUNCTION generate_creation_slug();

-- Increment builder balance
CREATE OR REPLACE FUNCTION increment_builder_balance(
    p_foundation_id UUID,
    p_amount INTEGER,
    p_type TEXT DEFAULT 'sale'
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO builder_balances (foundation_id, available_balance_cents, lifetime_earnings_cents, lifetime_downstream_cents)
    VALUES (
        p_foundation_id,
        CASE WHEN p_type = 'downstream' THEN 0 ELSE p_amount END,
        CASE WHEN p_type = 'downstream' THEN 0 ELSE p_amount END,
        CASE WHEN p_type = 'downstream' THEN p_amount ELSE 0 END
    )
    ON CONFLICT (foundation_id)
    DO UPDATE SET
        available_balance_cents = builder_balances.available_balance_cents +
            CASE WHEN p_type = 'downstream' THEN 0 ELSE p_amount END,
        lifetime_earnings_cents = builder_balances.lifetime_earnings_cents +
            CASE WHEN p_type = 'downstream' THEN 0 ELSE p_amount END,
        lifetime_downstream_cents = builder_balances.lifetime_downstream_cents +
            CASE WHEN p_type = 'downstream' THEN p_amount ELSE 0 END,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Update creation stats on sale
CREATE OR REPLACE FUNCTION update_creation_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.event_type IN ('sale', 'subscription') AND NEW.status = 'completed' THEN
        UPDATE builder_creations
        SET
            total_sales = total_sales + 1,
            total_revenue_cents = total_revenue_cents + NEW.gross_amount_cents,
            updated_at = NOW()
        WHERE id = NEW.creation_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER revenue_update_stats
    AFTER INSERT ON revenue_events
    FOR EACH ROW EXECUTE FUNCTION update_creation_stats();

-- Update average rating
CREATE OR REPLACE FUNCTION update_creation_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE builder_creations
    SET
        rating_avg = (
            SELECT AVG(rating)::REAL FROM creation_reviews WHERE creation_id = NEW.creation_id
        ),
        rating_count = (
            SELECT COUNT(*) FROM creation_reviews WHERE creation_id = NEW.creation_id
        ),
        updated_at = NOW()
    WHERE id = NEW.creation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER review_update_rating
    AFTER INSERT OR UPDATE OR DELETE ON creation_reviews
    FOR EACH ROW EXECUTE FUNCTION update_creation_rating();

-- Create balance record when foundation created
CREATE OR REPLACE FUNCTION create_builder_balance()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO builder_balances (foundation_id)
    VALUES (NEW.id)
    ON CONFLICT (foundation_id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER foundation_create_balance
    AFTER INSERT ON user_foundations
    FOR EACH ROW EXECUTE FUNCTION create_builder_balance();

-- ============================================================
-- PART 5: VIEWS
-- ============================================================

-- Marketplace view (public creations with stats)
CREATE OR REPLACE VIEW marketplace_creations AS
SELECT
    c.id,
    c.name,
    c.slug,
    c.description,
    c.type,
    c.category,
    c.tags,
    c.thumbnail_url,
    c.base_price_cents,
    c.total_sales,
    c.rating_avg,
    c.rating_count,
    c.download_count,
    c.consciousness_score,
    c.verification_status,
    c.published_at,
    f.name as builder_name,
    f.id as builder_foundation_id
FROM builder_creations c
JOIN user_foundations f ON c.foundation_id = f.id
WHERE c.visibility = 'marketplace'
AND c.status = 'published';

-- Builder earnings summary
CREATE OR REPLACE VIEW builder_earnings_summary AS
SELECT
    b.foundation_id,
    b.available_balance_cents,
    b.pending_balance_cents,
    b.lifetime_earnings_cents,
    b.lifetime_downstream_cents,
    b.stripe_connect_status,
    b.last_payout_at,
    COUNT(DISTINCT c.id) as total_creations,
    COUNT(DISTINCT CASE WHEN c.visibility = 'marketplace' THEN c.id END) as marketplace_creations,
    SUM(c.total_sales) as total_sales
FROM builder_balances b
LEFT JOIN builder_creations c ON b.foundation_id = c.foundation_id
GROUP BY b.foundation_id, b.available_balance_cents, b.pending_balance_cents,
         b.lifetime_earnings_cents, b.lifetime_downstream_cents,
         b.stripe_connect_status, b.last_payout_at;

-- ============================================================
-- VERIFICATION
-- ============================================================

DO $$
BEGIN
    RAISE NOTICE 'Builder Economics Schema created successfully!';
    RAISE NOTICE 'Tables: builder_creations, creation_lineage, revenue_events, downstream_revenue, builder_balances, creation_usage, creation_reviews, payout_history';
    RAISE NOTICE 'Views: marketplace_creations, builder_earnings_summary';
    RAISE NOTICE 'RLS: Enabled on all tables';
    RAISE NOTICE 'Ready for deployment!';
END $$;
