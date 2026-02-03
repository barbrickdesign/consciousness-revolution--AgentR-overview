# BUILDER ECONOMICS IMPLEMENTATION SPEC
## C1 Mechanic - Technical Blueprint
## Created: 2026-01-10

---

## THE PROBLEM (In Plain English)

Builders get 200 abilities from the platform. Natural behavior:
1. Use abilities to build something cool
2. Want to sell it privately (keep all the money)
3. Don't want to share back to network

This is natural and valid. We can't (and shouldn't) force sharing.

**THE SOLUTION:** Make sharing MORE PROFITABLE than hoarding.

---

## CORE ECONOMICS PRINCIPLE

```
Builder keeps 100% of PRIVATE sales (their own customer)
Builder gets 80% of MARKETPLACE sales (platform finds buyer)
Network gets 20% marketplace fee (for distribution + trust)

BONUS: Builder gets 10% of downstream revenue
       (things built FROM their creation)
```

**Why this works:**
- Private empire = full sovereignty (builder happy)
- Marketplace = platform brings customers (win-win)
- Downstream = passive income for innovation (multiplier)

---

## WHAT TRIGGERS REVENUE SHARE?

| Event | Who Pays | Builder Gets | Network Gets |
|-------|----------|--------------|--------------|
| Direct Sale (private) | Customer | 100% | 0% |
| Marketplace Sale | Customer | 80% | 20% |
| Downstream Creation Sold | Downstream Customer | 10% | 10%* |
| Ability Usage (API) | Customer | 70% | 30% |

*Network fee on downstream = 10% to original creator + 10% to network

---

## DATABASE SCHEMA (Supabase Addition)

```sql
-- ============================================================
-- BUILDER ECONOMICS TABLES
-- Add to existing FOUNDATION_SCHEMA.sql
-- ============================================================

-- Creations Registry (What Builders Make)
CREATE TABLE IF NOT EXISTS builder_creations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK (type IN (
        'ability', 'module', 'template', 'workflow',
        'integration', 'pattern', 'dataset', 'korpak'
    )),
    visibility TEXT DEFAULT 'private' CHECK (visibility IN (
        'private', 'cell', 'marketplace', 'open_source'
    )),
    source_abilities TEXT[] DEFAULT '{}',  -- Which platform abilities it uses
    stripe_product_id TEXT,
    stripe_price_id TEXT,
    base_price_cents INTEGER,
    revenue_share_pct INTEGER DEFAULT 80,  -- Builder's cut on marketplace
    downstream_share_pct INTEGER DEFAULT 10, -- Builder gets from derivatives
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
        'derived', 'extended', 'composed', 'inspired'
    )),
    attribution_required BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Revenue Events (Every Money Movement)
CREATE TABLE IF NOT EXISTS revenue_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creation_id UUID REFERENCES builder_creations(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL CHECK (event_type IN (
        'sale', 'subscription', 'usage', 'downstream', 'refund'
    )),
    gross_amount_cents INTEGER NOT NULL,
    builder_amount_cents INTEGER NOT NULL,
    network_amount_cents INTEGER NOT NULL,
    downstream_amount_cents INTEGER DEFAULT 0,
    buyer_foundation_id UUID REFERENCES user_foundations(id),
    seller_foundation_id UUID REFERENCES user_foundations(id) NOT NULL,
    stripe_payment_id TEXT,
    stripe_transfer_id TEXT,
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
    stripe_connect_id TEXT,
    payout_schedule TEXT DEFAULT 'weekly',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(foundation_id)
);

-- Usage Metering (For API-Based Revenue)
CREATE TABLE IF NOT EXISTS creation_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creation_id UUID REFERENCES builder_creations(id) ON DELETE CASCADE NOT NULL,
    user_foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    billed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(creation_id, user_foundation_id, period_start)
);

-- Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_creations_foundation ON builder_creations(foundation_id);
CREATE INDEX IF NOT EXISTS idx_creations_visibility ON builder_creations(visibility);
CREATE INDEX IF NOT EXISTS idx_creations_type ON builder_creations(type);
CREATE INDEX IF NOT EXISTS idx_lineage_child ON creation_lineage(child_creation_id);
CREATE INDEX IF NOT EXISTS idx_lineage_parent ON creation_lineage(parent_creation_id);
CREATE INDEX IF NOT EXISTS idx_revenue_creation ON revenue_events(creation_id);
CREATE INDEX IF NOT EXISTS idx_revenue_seller ON revenue_events(seller_foundation_id);
CREATE INDEX IF NOT EXISTS idx_downstream_original ON downstream_revenue(original_creation_id);
CREATE INDEX IF NOT EXISTS idx_balances_foundation ON builder_balances(foundation_id);

-- RLS Policies
ALTER TABLE builder_creations ENABLE ROW LEVEL SECURITY;
ALTER TABLE creation_lineage ENABLE ROW LEVEL SECURITY;
ALTER TABLE revenue_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE downstream_revenue ENABLE ROW LEVEL SECURITY;
ALTER TABLE builder_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE creation_usage ENABLE ROW LEVEL SECURITY;

-- Creators see their creations
CREATE POLICY "Creators own their creations"
    ON builder_creations FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Public can see marketplace items
CREATE POLICY "Public sees marketplace creations"
    ON builder_creations FOR SELECT
    USING (visibility = 'marketplace');

-- Builders see their revenue
CREATE POLICY "Builders see their revenue"
    ON revenue_events FOR SELECT
    USING (
        seller_foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Builders see their balance
CREATE POLICY "Builders see their balance"
    ON builder_balances FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );
```

---

## STRIPE INTEGRATION POINTS

### 1. Stripe Connect for Builders

```javascript
// netlify/functions/create-connect-account.js

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { createClient } = require('@supabase/supabase-js');

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { foundation_id, email, country } = JSON.parse(event.body);

    // Create Stripe Connect Express account
    const account = await stripe.accounts.create({
        type: 'express',
        email: email,
        country: country || 'US',
        capabilities: {
            card_payments: { requested: true },
            transfers: { requested: true }
        },
        metadata: {
            foundation_id: foundation_id
        }
    });

    // Save to Supabase
    await supabase
        .from('builder_balances')
        .upsert({
            foundation_id: foundation_id,
            stripe_connect_id: account.id
        });

    // Generate onboarding link
    const accountLink = await stripe.accountLinks.create({
        account: account.id,
        refresh_url: `${process.env.SITE_URL}/builder/dashboard`,
        return_url: `${process.env.SITE_URL}/builder/dashboard?connected=true`,
        type: 'account_onboarding'
    });

    return {
        statusCode: 200,
        body: JSON.stringify({
            account_id: account.id,
            onboarding_url: accountLink.url
        })
    };
};
```

### 2. Marketplace Purchase with Revenue Split

```javascript
// netlify/functions/marketplace-checkout.js

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { createClient } = require('@supabase/supabase-js');

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { creation_id, buyer_foundation_id } = JSON.parse(event.body);

    // Get creation details
    const { data: creation } = await supabase
        .from('builder_creations')
        .select(`
            *,
            user_foundations!inner(stripe_customer_id),
            builder_balances!inner(stripe_connect_id)
        `)
        .eq('id', creation_id)
        .single();

    if (!creation || creation.visibility !== 'marketplace') {
        return { statusCode: 404, body: 'Creation not found' };
    }

    // Calculate split
    const totalCents = creation.base_price_cents;
    const builderCents = Math.floor(totalCents * creation.revenue_share_pct / 100);
    const networkCents = totalCents - builderCents;

    // Create checkout with automatic transfer
    const session = await stripe.checkout.sessions.create({
        mode: creation.stripe_price_id?.includes('recurring') ? 'subscription' : 'payment',
        line_items: [{
            price: creation.stripe_price_id,
            quantity: 1
        }],
        payment_intent_data: {
            application_fee_amount: networkCents,
            transfer_data: {
                destination: creation.builder_balances.stripe_connect_id
            }
        },
        success_url: `${process.env.SITE_URL}/marketplace/success?creation=${creation_id}`,
        cancel_url: `${process.env.SITE_URL}/marketplace/${creation_id}`,
        metadata: {
            creation_id: creation_id,
            buyer_foundation_id: buyer_foundation_id,
            seller_foundation_id: creation.foundation_id,
            builder_amount: builderCents,
            network_amount: networkCents
        }
    });

    return {
        statusCode: 200,
        body: JSON.stringify({ checkout_url: session.url })
    };
};
```

### 3. Webhook Handler for Revenue Tracking

```javascript
// netlify/functions/stripe-webhook.js

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { createClient } = require('@supabase/supabase-js');

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const sig = event.headers['stripe-signature'];
    let stripeEvent;

    try {
        stripeEvent = stripe.webhooks.constructEvent(
            event.body,
            sig,
            process.env.STRIPE_WEBHOOK_SECRET
        );
    } catch (err) {
        return { statusCode: 400, body: `Webhook Error: ${err.message}` };
    }

    if (stripeEvent.type === 'checkout.session.completed') {
        const session = stripeEvent.data.object;
        const metadata = session.metadata;

        // Record revenue event
        await supabase.from('revenue_events').insert({
            creation_id: metadata.creation_id,
            event_type: 'sale',
            gross_amount_cents: session.amount_total,
            builder_amount_cents: parseInt(metadata.builder_amount),
            network_amount_cents: parseInt(metadata.network_amount),
            buyer_foundation_id: metadata.buyer_foundation_id,
            seller_foundation_id: metadata.seller_foundation_id,
            stripe_payment_id: session.payment_intent
        });

        // Update builder balance
        await supabase.rpc('increment_builder_balance', {
            p_foundation_id: metadata.seller_foundation_id,
            p_amount: parseInt(metadata.builder_amount)
        });

        // Check for downstream revenue
        await processDownstreamRevenue(
            supabase,
            metadata.creation_id,
            session.amount_total
        );
    }

    return { statusCode: 200, body: 'OK' };
};

async function processDownstreamRevenue(supabase, creation_id, gross_amount) {
    // Get all parent creations
    const { data: lineage } = await supabase
        .from('creation_lineage')
        .select(`
            parent_creation_id,
            parent_foundation_id,
            builder_creations!parent_creation_id(downstream_share_pct)
        `)
        .eq('child_creation_id', creation_id);

    for (const parent of lineage || []) {
        if (!parent.parent_foundation_id) continue;

        const downstreamPct = parent.builder_creations?.downstream_share_pct || 10;
        const downstreamAmount = Math.floor(gross_amount * downstreamPct / 100);

        // Record downstream revenue
        await supabase.from('downstream_revenue').insert({
            original_creation_id: parent.parent_creation_id,
            derived_creation_id: creation_id,
            original_builder_id: parent.parent_foundation_id,
            amount_cents: downstreamAmount
        });

        // Update original builder's balance
        await supabase.rpc('increment_builder_balance', {
            p_foundation_id: parent.parent_foundation_id,
            p_amount: downstreamAmount,
            p_type: 'downstream'
        });
    }
}
```

---

## MINIMUM VIABLE TRACKING SYSTEM

### Phase 1: TODAY (Can Build Now)

**What we track automatically:**
1. **Creation Registration** - When builder publishes to marketplace
2. **Purchase Events** - When money moves through Stripe
3. **Revenue Split** - Automatic via Stripe Connect

**Required setup:**
1. Run SQL schema in Supabase (5 minutes)
2. Create Netlify functions (30 minutes)
3. Connect Stripe webhook (10 minutes)
4. Builder dashboard UI (2 hours)

### Phase 2: WEEK 1 (Build Next)

**Add:**
1. **Usage Metering** - Track API calls to creations
2. **Lineage Detection** - Automatically detect when creation uses another
3. **Downstream Revenue** - Pay original creators

### Phase 3: MONTH 1 (Scale)

**Add:**
1. **Narrow Agent Verification** - AI verifies creation quality
2. **Consciousness Scoring** - Rate creations on builder vs destroyer pattern
3. **Cell Revenue Sharing** - Groups split revenue

---

## API ENDPOINTS (Build Today)

```
POST /api/creations/register
  - Register new creation
  - Set visibility, pricing
  - Create Stripe product/price

POST /api/creations/{id}/publish
  - Move to marketplace
  - Set revenue share terms
  - Enable discovery

GET /api/marketplace
  - Browse available creations
  - Filter by type, price, rating

POST /api/marketplace/{id}/purchase
  - Create checkout session
  - Handle revenue split

GET /api/builder/dashboard
  - Show earnings, balances
  - List creations and sales

POST /api/builder/payout
  - Request payout to bank
  - Via Stripe Connect

GET /api/builder/downstream
  - Show passive income from derivatives
  - Track lineage tree
```

---

## EXTRACTION VAMPIRE PREVENTION

### The Problem:
Someone takes all 200 abilities, builds empire, never contributes back.

### The Solution: Tiered Access Based on Contribution

```
TIER 0 (Free):
- 10 basic abilities
- Can only sell privately (no marketplace access)
- No downstream revenue

TIER 1 ($47/mo Founding Member):
- 50 abilities
- Marketplace access
- 80/20 revenue split
- 10% downstream

TIER 2 ($99/mo Pattern Pro):
- 200 abilities
- Priority marketplace placement
- 85/15 revenue split
- 15% downstream

TIER 3 ($297/mo Forest Enterprise):
- Unlimited abilities
- White-label marketplace
- 90/10 revenue split
- 20% downstream
- Custom revenue terms
```

### Contribution Bonuses:
- Every creation published = +5 abilities unlocked
- Every $100 in marketplace sales = +10 abilities
- Every derivative that sells = +20 abilities

**The more you contribute, the more you get. Hoarding = limited growth.**

---

## ARAYA INTEGRATION

Araya can:
1. **Detect Lineage** - When builder uses platform abilities, auto-tag creation
2. **Suggest Publishing** - "This creation could earn $X on marketplace"
3. **Track Usage** - Monitor API calls to creations
4. **Calculate Downstream** - Show "You've earned $X from derivatives"
5. **Consciousness Score** - Rate creation on builder vs destroyer pattern

---

## FILES TO CREATE TODAY

1. `100X_DEPLOYMENT/netlify/functions/create-connect-account.js`
2. `100X_DEPLOYMENT/netlify/functions/marketplace-checkout.js`
3. `100X_DEPLOYMENT/netlify/functions/stripe-webhook.js`
4. `100X_DEPLOYMENT/builder-dashboard.html`
5. `100X_DEPLOYMENT/marketplace.html` (update existing)
6. `BUILDER_ECONOMICS_SCHEMA.sql` (for Supabase)

---

## SUCCESS METRICS

| Metric | Target (Month 1) | Target (Month 3) |
|--------|------------------|------------------|
| Builders with Connect accounts | 10 | 50 |
| Creations on marketplace | 20 | 100 |
| Marketplace transactions | 5 | 50 |
| Downstream revenue distributed | $0 | $500 |
| Builder retention (active 30d) | 70% | 80% |

---

## QUICK START COMMANDS

```bash
# 1. Apply schema to Supabase
# Copy BUILDER_ECONOMICS_SCHEMA.sql to Supabase SQL Editor and run

# 2. Create Stripe Connect settings
# Dashboard > Settings > Connect > Enable

# 3. Deploy Netlify functions
cd 100X_DEPLOYMENT && netlify deploy --prod --dir=.

# 4. Set environment variables in Netlify
# STRIPE_SECRET_KEY
# STRIPE_WEBHOOK_SECRET
# SUPABASE_URL
# SUPABASE_SERVICE_KEY
```

---

## THE PATTERN

```
Builder takes abilities → Creates value → Network distributes
                              ↓
         80% back to builder + 10% to upstream
                              ↓
         More builders create → More value → Exponential growth
```

**The network becomes MORE valuable as builders contribute, not less.**

---

*C1 MECHANIC - Built for execution, not theory.*
*Ship today. Iterate tomorrow.*
