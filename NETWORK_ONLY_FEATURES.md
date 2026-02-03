# NETWORK-ONLY FEATURES SPECIFICATION
## C1 Mechanic - Ability Access Control System
## Created: 2026-01-10

---

## THE CORE INSIGHT

**"Privacy is not the signal. FLOW is the signal."** - C3 Oracle

Builders who take 200 abilities and build privately forever are NOT the problem.
The problem is **extraction without contribution** - taking value without creating flow.

**SOLUTION:** Abilities work alone. Abilities THRIVE together.
The network doesn't punish isolation - it rewards connection.

---

## ABILITY CLASSIFICATION SYSTEM

### Type A: STANDALONE (Works Fully Offline)
Basic building blocks that function independently.

| Category | Examples | Offline Power | Connected Power |
|----------|----------|---------------|-----------------|
| File Operations | read, write, list, search | 100% | 100% |
| Local Database | SQLite queries, CRUD | 100% | 100% |
| Code Generation | Templates, scaffolds | 100% | 100% |
| Text Processing | Parse, transform, format | 100% | 100% |
| Local Automation | Scripts, batch jobs | 100% | 100% |

**Count: ~200 abilities (40% of total)**

---

### Type B: NETWORK-ENHANCED (Works Offline, Better Connected)
Full functionality solo, but network multiplies effectiveness.

| Category | Examples | Offline Power | Connected Power |
|----------|----------|---------------|-----------------|
| Pattern Recognition | Local detection | 60% | 100% (shared patterns) |
| Bug Detection | Local lint | 70% | 100% (community fixes) |
| Code Analysis | Static analysis | 80% | 100% (best practices DB) |
| Documentation | Local gen | 70% | 100% (examples library) |
| Testing | Local tests | 80% | 100% (test case sharing) |

**Count: ~150 abilities (30% of total)**

**What Network Adds:**
- Shared pattern libraries (10,000+ patterns vs your 50)
- Bug fix database (instant fixes for known issues)
- Best practices updates (evolving standards)
- Community examples (real-world usage)
- Version sync (latest improvements)

---

### Type C: NETWORK-REQUIRED (Only Works Connected)
These abilities NEED the network to function.

| Category | Examples | Offline Power | Connected Power |
|----------|----------|---------------|-----------------|
| Marketplace Access | Buy/sell creations | 0% | 100% |
| Reputation System | Trust scores | 0% | 100% |
| Downstream Revenue | Passive income | 0% | 100% |
| Pattern Libraries | Collective intelligence | 0% | 100% |
| Real-time Updates | Bug fixes, versions | 0% | 100% |
| Community Support | Help channels | 0% | 100% |
| Cross-Builder Collab | Cell coordination | 0% | 100% |
| AI Model Access | Cloud models | 0% | 100% |

**Count: ~150 abilities (30% of total)**

---

## NETWORK CONTRIBUTION STATUS

### Contribution Score Formula

```
CONTRIBUTION_SCORE = (
    creations_published * 10 +
    marketplace_sales * 5 +
    downstream_derivatives * 20 +
    bugs_reported * 2 +
    patterns_shared * 3 +
    community_help_given * 1 +
    days_active * 0.1
)
```

### Contribution Tiers

| Tier | Score Range | Network Features | Type B Power |
|------|-------------|------------------|--------------|
| GHOST | 0 | None | 60% |
| SEEDLING | 1-49 | Basic marketplace | 70% |
| SAPLING | 50-199 | Full marketplace | 80% |
| TREE | 200-499 | + Downstream revenue | 90% |
| FOREST | 500+ | Full power + priority | 100% |

---

## DATABASE SCHEMA ADDITIONS

```sql
-- ============================================================
-- NETWORK CONTRIBUTION TRACKING
-- Add to BUILDER_ECONOMICS_IMPLEMENTATION.md schema
-- ============================================================

-- Builder Network Status
CREATE TABLE IF NOT EXISTS builder_network_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foundation_id UUID REFERENCES user_foundations(id) ON DELETE CASCADE NOT NULL,
    contribution_score INTEGER DEFAULT 0,
    contribution_tier TEXT DEFAULT 'GHOST' CHECK (contribution_tier IN (
        'GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'
    )),
    creations_published INTEGER DEFAULT 0,
    marketplace_sales INTEGER DEFAULT 0,
    downstream_derivatives INTEGER DEFAULT 0,
    bugs_reported INTEGER DEFAULT 0,
    patterns_shared INTEGER DEFAULT 0,
    community_help_given INTEGER DEFAULT 0,
    last_network_activity TIMESTAMPTZ,
    network_features_enabled JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(foundation_id)
);

-- Ability Access Control
CREATE TABLE IF NOT EXISTS ability_access_control (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ability_name TEXT NOT NULL,
    ability_category TEXT NOT NULL,
    access_type TEXT NOT NULL CHECK (access_type IN (
        'standalone', 'network_enhanced', 'network_required'
    )),
    min_tier_required TEXT DEFAULT 'GHOST',
    offline_power_pct INTEGER DEFAULT 100,
    network_features TEXT[] DEFAULT '{}',
    degraded_behavior TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Network Feature Access Log
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
CREATE TABLE IF NOT EXISTS shared_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contributor_id UUID REFERENCES user_foundations(id),
    pattern_name TEXT NOT NULL,
    pattern_type TEXT NOT NULL,
    pattern_data JSONB NOT NULL,
    usage_count INTEGER DEFAULT 0,
    quality_score FLOAT DEFAULT 0.5,
    network_only BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_network_status_foundation ON builder_network_status(foundation_id);
CREATE INDEX IF NOT EXISTS idx_network_status_tier ON builder_network_status(contribution_tier);
CREATE INDEX IF NOT EXISTS idx_ability_access_type ON ability_access_control(access_type);
CREATE INDEX IF NOT EXISTS idx_shared_patterns_type ON shared_patterns(pattern_type);

-- RLS Policies
ALTER TABLE builder_network_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE ability_access_control ENABLE ROW LEVEL SECURITY;
ALTER TABLE network_feature_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE shared_patterns ENABLE ROW LEVEL SECURITY;

-- Builders see their status
CREATE POLICY "Builders see own network status"
    ON builder_network_status FOR ALL
    USING (
        foundation_id IN (
            SELECT id FROM user_foundations WHERE user_id = auth.uid()
        )
    );

-- Everyone can read ability access rules
CREATE POLICY "Public reads ability access"
    ON ability_access_control FOR SELECT
    USING (TRUE);

-- Network patterns visible to SAPLING+ tiers
CREATE POLICY "Network patterns for contributors"
    ON shared_patterns FOR SELECT
    USING (
        network_only = FALSE OR
        EXISTS (
            SELECT 1 FROM builder_network_status bns
            JOIN user_foundations uf ON bns.foundation_id = uf.id
            WHERE uf.user_id = auth.uid()
            AND bns.contribution_tier IN ('SAPLING', 'TREE', 'FOREST')
        )
    );
```

---

## IMPLEMENTATION CODE

### 1. Ability Access Controller

```javascript
// 100X_DEPLOYMENT/netlify/functions/ability-access.js

const { createClient } = require('@supabase/supabase-js');

// Ability type definitions
const ABILITY_TYPES = {
    STANDALONE: 'standalone',
    NETWORK_ENHANCED: 'network_enhanced',
    NETWORK_REQUIRED: 'network_required'
};

// Tier requirements for network features
const TIER_REQUIREMENTS = {
    GHOST: 0,
    SEEDLING: 1,
    SAPLING: 50,
    TREE: 200,
    FOREST: 500
};

// Network-only features by tier
const NETWORK_FEATURES_BY_TIER = {
    GHOST: [],
    SEEDLING: ['basic_marketplace_browse'],
    SAPLING: ['marketplace_buy', 'marketplace_sell', 'pattern_library_read'],
    TREE: ['downstream_revenue', 'pattern_library_write', 'priority_support'],
    FOREST: ['full_api_access', 'custom_revenue_terms', 'white_label', 'cell_leadership']
};

/**
 * Check if builder can access an ability at full power
 */
async function checkAbilityAccess(supabase, foundationId, abilityName) {
    // Get builder's network status
    const { data: status } = await supabase
        .from('builder_network_status')
        .select('*')
        .eq('foundation_id', foundationId)
        .single();

    // Get ability access requirements
    const { data: ability } = await supabase
        .from('ability_access_control')
        .select('*')
        .eq('ability_name', abilityName)
        .single();

    if (!ability) {
        // Unknown ability - default to standalone
        return {
            allowed: true,
            power_level: 100,
            access_type: 'standalone',
            message: 'Full access'
        };
    }

    const tier = status?.contribution_tier || 'GHOST';
    const score = status?.contribution_score || 0;

    // Standalone abilities always work
    if (ability.access_type === ABILITY_TYPES.STANDALONE) {
        return {
            allowed: true,
            power_level: 100,
            access_type: 'standalone',
            message: 'Full offline access'
        };
    }

    // Network-required abilities need connection + tier
    if (ability.access_type === ABILITY_TYPES.NETWORK_REQUIRED) {
        const tierRank = Object.keys(TIER_REQUIREMENTS).indexOf(tier);
        const requiredRank = Object.keys(TIER_REQUIREMENTS).indexOf(ability.min_tier_required);

        if (tierRank < requiredRank) {
            return {
                allowed: false,
                power_level: 0,
                access_type: 'network_required',
                current_tier: tier,
                required_tier: ability.min_tier_required,
                message: `Requires ${ability.min_tier_required} tier. You are ${tier}. Contribute to unlock.`,
                upgrade_hint: getUpgradeHint(tier, ability.min_tier_required)
            };
        }

        return {
            allowed: true,
            power_level: 100,
            access_type: 'network_required',
            message: 'Network access granted'
        };
    }

    // Network-enhanced abilities work but with degraded power
    if (ability.access_type === ABILITY_TYPES.NETWORK_ENHANCED) {
        const tierMultiplier = {
            GHOST: 0.6,
            SEEDLING: 0.7,
            SAPLING: 0.8,
            TREE: 0.9,
            FOREST: 1.0
        };

        const powerLevel = Math.round(ability.offline_power_pct * tierMultiplier[tier]);

        return {
            allowed: true,
            power_level: powerLevel,
            access_type: 'network_enhanced',
            current_tier: tier,
            message: powerLevel < 100
                ? `Operating at ${powerLevel}% power. Contribute to unlock full power.`
                : 'Full network power',
            network_features: ability.network_features || [],
            degraded_behavior: powerLevel < 100 ? ability.degraded_behavior : null
        };
    }

    return { allowed: true, power_level: 100 };
}

/**
 * Get hints for upgrading tier
 */
function getUpgradeHint(currentTier, targetTier) {
    const hints = {
        GHOST: 'Publish your first creation to the marketplace to become a SEEDLING',
        SEEDLING: 'Make 5 marketplace sales or share 10 patterns to become a SAPLING',
        SAPLING: 'Reach $500 in sales or help 100 community members to become a TREE',
        TREE: 'Maintain consistent contribution to become a FOREST leader'
    };
    return hints[currentTier] || 'Keep contributing to the network';
}

/**
 * Check multiple abilities at once
 */
async function checkBulkAbilityAccess(supabase, foundationId, abilityNames) {
    const results = {};
    for (const name of abilityNames) {
        results[name] = await checkAbilityAccess(supabase, foundationId, name);
    }
    return results;
}

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { foundation_id, ability_name, abilities } = JSON.parse(event.body || '{}');

    if (!foundation_id) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'foundation_id required' })
        };
    }

    try {
        let result;

        if (abilities && Array.isArray(abilities)) {
            result = await checkBulkAbilityAccess(supabase, foundation_id, abilities);
        } else if (ability_name) {
            result = await checkAbilityAccess(supabase, foundation_id, ability_name);
        } else {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'ability_name or abilities[] required' })
            };
        }

        // Log access attempt
        await supabase.from('network_feature_access').insert({
            foundation_id,
            feature_name: ability_name || 'bulk_check',
            access_granted: result.allowed !== false,
            contribution_tier: result.current_tier
        });

        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };

    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
```

---

### 2. Network Feature Gate

```javascript
// 100X_DEPLOYMENT/netlify/functions/network-feature-gate.js

const { createClient } = require('@supabase/supabase-js');

// All network-only features
const NETWORK_FEATURES = {
    // Marketplace Features
    marketplace_browse: { min_tier: 'SEEDLING', description: 'Browse marketplace listings' },
    marketplace_buy: { min_tier: 'SAPLING', description: 'Purchase from marketplace' },
    marketplace_sell: { min_tier: 'SAPLING', description: 'List items for sale' },
    marketplace_featured: { min_tier: 'TREE', description: 'Featured placement' },

    // Revenue Features
    downstream_revenue: { min_tier: 'TREE', description: 'Earn from derivatives' },
    custom_revenue_terms: { min_tier: 'FOREST', description: 'Set custom revenue splits' },

    // Pattern Library
    pattern_library_read: { min_tier: 'SAPLING', description: 'Access shared patterns' },
    pattern_library_write: { min_tier: 'TREE', description: 'Contribute patterns' },

    // Support & Community
    community_help: { min_tier: 'SEEDLING', description: 'Access help channels' },
    priority_support: { min_tier: 'TREE', description: 'Priority response' },
    cell_creation: { min_tier: 'TREE', description: 'Create builder cells' },
    cell_leadership: { min_tier: 'FOREST', description: 'Lead multiple cells' },

    // Advanced Features
    full_api_access: { min_tier: 'FOREST', description: 'Unrestricted API calls' },
    white_label: { min_tier: 'FOREST', description: 'White-label marketplace' },
    beta_features: { min_tier: 'TREE', description: 'Early access to new abilities' },

    // Real-time Features
    bug_fixes_instant: { min_tier: 'SAPLING', description: 'Instant bug fix notifications' },
    version_updates: { min_tier: 'SEEDLING', description: 'Ability version updates' },
    ai_model_access: { min_tier: 'SAPLING', description: 'Cloud AI model access' }
};

const TIER_RANKS = ['GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'];

/**
 * Check if builder has access to a network feature
 */
async function checkFeatureAccess(supabase, foundationId, featureName) {
    const feature = NETWORK_FEATURES[featureName];

    if (!feature) {
        return {
            allowed: false,
            reason: 'Unknown feature',
            feature: featureName
        };
    }

    // Get builder status
    const { data: status } = await supabase
        .from('builder_network_status')
        .select('contribution_tier, contribution_score')
        .eq('foundation_id', foundationId)
        .single();

    const currentTier = status?.contribution_tier || 'GHOST';
    const currentRank = TIER_RANKS.indexOf(currentTier);
    const requiredRank = TIER_RANKS.indexOf(feature.min_tier);

    if (currentRank < requiredRank) {
        return {
            allowed: false,
            feature: featureName,
            description: feature.description,
            current_tier: currentTier,
            required_tier: feature.min_tier,
            contribution_score: status?.contribution_score || 0,
            points_to_next_tier: getPointsToNextTier(currentTier, status?.contribution_score || 0),
            reason: `This feature requires ${feature.min_tier} tier`
        };
    }

    return {
        allowed: true,
        feature: featureName,
        description: feature.description,
        current_tier: currentTier
    };
}

/**
 * Get all available features for a builder
 */
async function getAvailableFeatures(supabase, foundationId) {
    const { data: status } = await supabase
        .from('builder_network_status')
        .select('contribution_tier, contribution_score')
        .eq('foundation_id', foundationId)
        .single();

    const currentTier = status?.contribution_tier || 'GHOST';
    const currentRank = TIER_RANKS.indexOf(currentTier);

    const available = [];
    const locked = [];

    for (const [name, feature] of Object.entries(NETWORK_FEATURES)) {
        const requiredRank = TIER_RANKS.indexOf(feature.min_tier);

        if (currentRank >= requiredRank) {
            available.push({ name, ...feature });
        } else {
            locked.push({
                name,
                ...feature,
                unlock_tier: feature.min_tier
            });
        }
    }

    return {
        current_tier: currentTier,
        contribution_score: status?.contribution_score || 0,
        available_features: available,
        locked_features: locked,
        next_tier: TIER_RANKS[currentRank + 1] || null,
        points_to_next_tier: getPointsToNextTier(currentTier, status?.contribution_score || 0)
    };
}

function getPointsToNextTier(currentTier, currentScore) {
    const thresholds = {
        GHOST: 1,
        SEEDLING: 50,
        SAPLING: 200,
        TREE: 500,
        FOREST: Infinity
    };

    const nextTier = TIER_RANKS[TIER_RANKS.indexOf(currentTier) + 1];
    if (!nextTier) return 0;

    return Math.max(0, thresholds[currentTier] - currentScore);
}

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { action, foundation_id, feature_name } = JSON.parse(event.body || '{}');

    if (!foundation_id) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'foundation_id required' })
        };
    }

    try {
        let result;

        switch (action) {
            case 'check':
                if (!feature_name) {
                    return { statusCode: 400, body: JSON.stringify({ error: 'feature_name required' }) };
                }
                result = await checkFeatureAccess(supabase, foundation_id, feature_name);
                break;

            case 'list':
                result = await getAvailableFeatures(supabase, foundation_id);
                break;

            case 'all_features':
                result = { features: NETWORK_FEATURES };
                break;

            default:
                result = await getAvailableFeatures(supabase, foundation_id);
        }

        // Log access
        await supabase.from('network_feature_access').insert({
            foundation_id,
            feature_name: feature_name || 'list_features',
            access_granted: result.allowed !== false,
            contribution_tier: result.current_tier
        });

        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };

    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
```

---

### 3. Degraded Mode Fallback Handler

```javascript
// 100X_DEPLOYMENT/netlify/functions/degraded-mode.js

const { createClient } = require('@supabase/supabase-js');

/**
 * Degraded behaviors for network-enhanced abilities
 */
const DEGRADED_BEHAVIORS = {
    pattern_recognition: {
        full_power: 'Access to 10,000+ community patterns',
        degraded: 'Limited to 50 local patterns',
        fallback_action: 'use_local_patterns',
        local_data_path: '/patterns/local'
    },

    bug_detection: {
        full_power: 'Real-time bug database with 500K+ known issues',
        degraded: 'Local lint rules only',
        fallback_action: 'use_local_lint',
        local_data_path: '/lint/rules.json'
    },

    code_analysis: {
        full_power: 'Community best practices + AI analysis',
        degraded: 'Static analysis only',
        fallback_action: 'static_analysis',
        local_data_path: '/analysis/static'
    },

    documentation: {
        full_power: 'AI-powered docs with 100K+ examples',
        degraded: 'Template-based generation',
        fallback_action: 'template_docs',
        local_data_path: '/docs/templates'
    },

    testing: {
        full_power: 'Shared test cases + fuzzing',
        degraded: 'Unit tests only',
        fallback_action: 'local_tests',
        local_data_path: '/tests/local'
    },

    ai_assistance: {
        full_power: 'Cloud AI models (GPT-4, Claude)',
        degraded: 'Local LLM or rule-based',
        fallback_action: 'local_llm',
        local_data_path: '/models/local'
    }
};

/**
 * Execute ability in degraded mode
 */
async function executeDegraded(supabase, foundationId, abilityName, params) {
    const behavior = DEGRADED_BEHAVIORS[abilityName];

    if (!behavior) {
        return {
            success: false,
            error: 'No degraded behavior defined',
            ability: abilityName
        };
    }

    // Log degraded execution
    await supabase.from('network_feature_access').insert({
        foundation_id: foundationId,
        feature_name: `${abilityName}_degraded`,
        access_granted: true,
        denial_reason: 'Degraded mode - insufficient contribution'
    });

    return {
        success: true,
        mode: 'degraded',
        ability: abilityName,
        full_power_description: behavior.full_power,
        degraded_description: behavior.degraded,
        action: behavior.fallback_action,
        local_data: behavior.local_data_path,
        upgrade_message: 'Contribute to the network to unlock full power',
        params_used: params
    };
}

/**
 * Get degraded mode info for an ability
 */
function getDegradedInfo(abilityName) {
    const behavior = DEGRADED_BEHAVIORS[abilityName];

    if (!behavior) {
        return {
            ability: abilityName,
            has_degraded_mode: false,
            message: 'This ability has no degraded mode'
        };
    }

    return {
        ability: abilityName,
        has_degraded_mode: true,
        full_power: behavior.full_power,
        degraded: behavior.degraded,
        fallback_action: behavior.fallback_action
    };
}

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { action, foundation_id, ability_name, params } = JSON.parse(event.body || '{}');

    try {
        let result;

        switch (action) {
            case 'execute':
                if (!foundation_id || !ability_name) {
                    return {
                        statusCode: 400,
                        body: JSON.stringify({ error: 'foundation_id and ability_name required' })
                    };
                }
                result = await executeDegraded(supabase, foundation_id, ability_name, params);
                break;

            case 'info':
                result = getDegradedInfo(ability_name);
                break;

            case 'list':
                result = { degraded_behaviors: DEGRADED_BEHAVIORS };
                break;

            default:
                result = { degraded_behaviors: Object.keys(DEGRADED_BEHAVIORS) };
        }

        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };

    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
```

---

### 4. Contribution Score Updater

```javascript
// 100X_DEPLOYMENT/netlify/functions/update-contribution.js

const { createClient } = require('@supabase/supabase-js');

// Point values for different actions
const CONTRIBUTION_POINTS = {
    creation_published: 10,
    marketplace_sale: 5,
    downstream_derivative: 20,
    bug_reported: 2,
    pattern_shared: 3,
    community_help: 1,
    daily_active: 0.1
};

const TIER_THRESHOLDS = {
    GHOST: 0,
    SEEDLING: 1,
    SAPLING: 50,
    TREE: 200,
    FOREST: 500
};

/**
 * Calculate tier from score
 */
function calculateTier(score) {
    if (score >= TIER_THRESHOLDS.FOREST) return 'FOREST';
    if (score >= TIER_THRESHOLDS.TREE) return 'TREE';
    if (score >= TIER_THRESHOLDS.SAPLING) return 'SAPLING';
    if (score >= TIER_THRESHOLDS.SEEDLING) return 'SEEDLING';
    return 'GHOST';
}

/**
 * Record contribution and update score/tier
 */
async function recordContribution(supabase, foundationId, contributionType, metadata = {}) {
    const points = CONTRIBUTION_POINTS[contributionType];

    if (!points) {
        return { error: 'Unknown contribution type', type: contributionType };
    }

    // Get current status
    let { data: status } = await supabase
        .from('builder_network_status')
        .select('*')
        .eq('foundation_id', foundationId)
        .single();

    if (!status) {
        // Create new status record
        const { data: newStatus, error } = await supabase
            .from('builder_network_status')
            .insert({
                foundation_id: foundationId,
                contribution_score: 0,
                contribution_tier: 'GHOST'
            })
            .select()
            .single();

        if (error) throw error;
        status = newStatus;
    }

    // Calculate new score
    const newScore = (status.contribution_score || 0) + points;
    const newTier = calculateTier(newScore);
    const tierChanged = newTier !== status.contribution_tier;

    // Update counters based on type
    const updates = {
        contribution_score: newScore,
        contribution_tier: newTier,
        last_network_activity: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    // Increment specific counter
    const counterMap = {
        creation_published: 'creations_published',
        marketplace_sale: 'marketplace_sales',
        downstream_derivative: 'downstream_derivatives',
        bug_reported: 'bugs_reported',
        pattern_shared: 'patterns_shared',
        community_help: 'community_help_given'
    };

    if (counterMap[contributionType]) {
        updates[counterMap[contributionType]] = (status[counterMap[contributionType]] || 0) + 1;
    }

    // Update network features if tier changed
    if (tierChanged) {
        const features = getFeaturesByTier(newTier);
        updates.network_features_enabled = features;
    }

    // Save updates
    await supabase
        .from('builder_network_status')
        .update(updates)
        .eq('foundation_id', foundationId);

    return {
        success: true,
        contribution_type: contributionType,
        points_earned: points,
        new_score: newScore,
        new_tier: newTier,
        tier_changed: tierChanged,
        previous_tier: status.contribution_tier,
        unlocked_features: tierChanged ? getFeaturesByTier(newTier) : []
    };
}

function getFeaturesByTier(tier) {
    const features = {
        GHOST: [],
        SEEDLING: ['version_updates', 'community_help', 'basic_marketplace_browse'],
        SAPLING: ['marketplace_buy', 'marketplace_sell', 'pattern_library_read', 'bug_fixes_instant', 'ai_model_access'],
        TREE: ['downstream_revenue', 'pattern_library_write', 'priority_support', 'cell_creation', 'beta_features'],
        FOREST: ['full_api_access', 'custom_revenue_terms', 'white_label', 'cell_leadership']
    };

    // Accumulate features from all lower tiers
    const tiers = ['GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'];
    const tierIndex = tiers.indexOf(tier);

    let accumulated = [];
    for (let i = 0; i <= tierIndex; i++) {
        accumulated = [...accumulated, ...features[tiers[i]]];
    }

    return accumulated;
}

exports.handler = async (event) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    const { foundation_id, contribution_type, metadata } = JSON.parse(event.body || '{}');

    if (!foundation_id || !contribution_type) {
        return {
            statusCode: 400,
            body: JSON.stringify({ error: 'foundation_id and contribution_type required' })
        };
    }

    try {
        const result = await recordContribution(supabase, foundation_id, contribution_type, metadata);

        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };

    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
```

---

## CLIENT-SIDE INTEGRATION

### Ability Access Wrapper

```javascript
// 100X_DEPLOYMENT/js/ability-access.js

class AbilityAccessController {
    constructor(supabaseClient, foundationId) {
        this.supabase = supabaseClient;
        this.foundationId = foundationId;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Execute an ability with access control
     */
    async execute(abilityName, params = {}) {
        // Check access
        const access = await this.checkAccess(abilityName);

        if (!access.allowed) {
            return {
                success: false,
                error: 'Access denied',
                ...access
            };
        }

        // If degraded, route to degraded handler
        if (access.power_level < 100) {
            return this.executeDegraded(abilityName, params, access);
        }

        // Full power execution
        return this.executeFull(abilityName, params);
    }

    /**
     * Check access to an ability
     */
    async checkAccess(abilityName) {
        // Check cache first
        const cached = this.cache.get(abilityName);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        const response = await fetch('/.netlify/functions/ability-access', {
            method: 'POST',
            body: JSON.stringify({
                foundation_id: this.foundationId,
                ability_name: abilityName
            })
        });

        const data = await response.json();

        // Cache result
        this.cache.set(abilityName, { data, timestamp: Date.now() });

        return data;
    }

    /**
     * Get all available network features
     */
    async getAvailableFeatures() {
        const response = await fetch('/.netlify/functions/network-feature-gate', {
            method: 'POST',
            body: JSON.stringify({
                action: 'list',
                foundation_id: this.foundationId
            })
        });

        return response.json();
    }

    /**
     * Execute in degraded mode
     */
    async executeDegraded(abilityName, params, access) {
        console.log(`Executing ${abilityName} in degraded mode (${access.power_level}% power)`);

        const response = await fetch('/.netlify/functions/degraded-mode', {
            method: 'POST',
            body: JSON.stringify({
                action: 'execute',
                foundation_id: this.foundationId,
                ability_name: abilityName,
                params
            })
        });

        const result = await response.json();

        return {
            ...result,
            power_level: access.power_level,
            upgrade_hint: access.upgrade_hint
        };
    }

    /**
     * Execute at full power
     */
    async executeFull(abilityName, params) {
        // This would call the actual ability implementation
        // Placeholder for now
        return {
            success: true,
            mode: 'full',
            ability: abilityName,
            result: 'Execution result here'
        };
    }

    /**
     * Record a contribution
     */
    async recordContribution(type, metadata = {}) {
        const response = await fetch('/.netlify/functions/update-contribution', {
            method: 'POST',
            body: JSON.stringify({
                foundation_id: this.foundationId,
                contribution_type: type,
                metadata
            })
        });

        const result = await response.json();

        // Show tier upgrade notification if applicable
        if (result.tier_changed) {
            this.showTierUpgrade(result);
        }

        return result;
    }

    /**
     * Show tier upgrade notification
     */
    showTierUpgrade(result) {
        const message = `
            Congratulations! You've reached ${result.new_tier} tier!

            New features unlocked:
            ${result.unlocked_features.join('\n')}
        `;

        // Use your preferred notification system
        console.log(message);
        console.warn(message);
    }
}

// Export for use
window.AbilityAccessController = AbilityAccessController;
```

---

## INTEGRATION WITH EXISTING SCHEMA

### Add to BUILDER_ECONOMICS webhook

```javascript
// Add to netlify/functions/stripe-webhook.js

// After recording sale, update contribution
await recordContribution(supabase, metadata.seller_foundation_id, 'marketplace_sale', {
    creation_id: metadata.creation_id,
    amount: session.amount_total
});

// If there's downstream, credit original creators
for (const parent of lineage || []) {
    await recordContribution(supabase, parent.parent_foundation_id, 'downstream_derivative', {
        derived_from: creation_id
    });
}
```

### Populate ability_access_control table

```sql
-- Seed ability access rules
INSERT INTO ability_access_control (ability_name, ability_category, access_type, min_tier_required, offline_power_pct, network_features, degraded_behavior) VALUES

-- Type A: Standalone (100% offline)
('file_read', 'filesystem', 'standalone', 'GHOST', 100, '{}', NULL),
('file_write', 'filesystem', 'standalone', 'GHOST', 100, '{}', NULL),
('file_list', 'filesystem', 'standalone', 'GHOST', 100, '{}', NULL),
('sqlite_query', 'database', 'standalone', 'GHOST', 100, '{}', NULL),
('code_generate', 'generation', 'standalone', 'GHOST', 100, '{}', NULL),
('text_transform', 'processing', 'standalone', 'GHOST', 100, '{}', NULL),

-- Type B: Network Enhanced (works offline, better connected)
('pattern_recognition', 'intelligence', 'network_enhanced', 'GHOST', 60, '{"pattern_library_read"}', 'Limited to 50 local patterns'),
('bug_detection', 'quality', 'network_enhanced', 'GHOST', 70, '{"bug_fixes_instant"}', 'Local lint rules only'),
('code_analysis', 'quality', 'network_enhanced', 'GHOST', 80, '{"best_practices_db"}', 'Static analysis only'),
('documentation', 'generation', 'network_enhanced', 'GHOST', 70, '{"examples_library"}', 'Template-based generation'),
('testing', 'quality', 'network_enhanced', 'GHOST', 80, '{"test_case_sharing"}', 'Unit tests only'),
('ai_assistance', 'intelligence', 'network_enhanced', 'SEEDLING', 50, '{"ai_model_access"}', 'Local LLM or rule-based'),

-- Type C: Network Required (only works connected)
('marketplace_browse', 'marketplace', 'network_required', 'SEEDLING', 0, '{"marketplace_browse"}', NULL),
('marketplace_buy', 'marketplace', 'network_required', 'SAPLING', 0, '{"marketplace_buy"}', NULL),
('marketplace_sell', 'marketplace', 'network_required', 'SAPLING', 0, '{"marketplace_sell"}', NULL),
('downstream_revenue', 'revenue', 'network_required', 'TREE', 0, '{"downstream_revenue"}', NULL),
('pattern_library_write', 'community', 'network_required', 'TREE', 0, '{"pattern_library_write"}', NULL),
('cell_creation', 'collaboration', 'network_required', 'TREE', 0, '{"cell_creation"}', NULL),
('priority_support', 'support', 'network_required', 'TREE', 0, '{"priority_support"}', NULL),
('custom_revenue_terms', 'revenue', 'network_required', 'FOREST', 0, '{"custom_revenue_terms"}', NULL),
('white_label', 'enterprise', 'network_required', 'FOREST', 0, '{"white_label"}', NULL);
```

---

## API SUMMARY

| Endpoint | Purpose | Auth |
|----------|---------|------|
| `POST /ability-access` | Check ability access | Foundation ID |
| `POST /network-feature-gate` | Check/list features | Foundation ID |
| `POST /degraded-mode` | Execute degraded | Foundation ID |
| `POST /update-contribution` | Record contribution | Foundation ID |

---

## THE FLOW

```
Builder requests ability
        |
        v
Check access_type
        |
   +----+----+
   |    |    |
   v    v    v
  A    B    C
  |    |    |
  v    v    v
Full  Check  Check
Power tier   tier
  |    |     |
  v    v     v
100%  60-100% 0% or 100%
      based   based on
      on tier threshold
```

---

## EXTRACTION PREVENTION MATRIX

| Extraction Behavior | System Response |
|---------------------|-----------------|
| Takes abilities, builds privately forever | Works at 60% power, no marketplace, no downstream |
| Takes abilities, sells privately | Works fine, but misses 80% of potential customers |
| Takes abilities, shares back | Full power, marketplace access, downstream income |
| Contributes heavily | FOREST tier, white-label, custom terms, leadership |

**The system doesn't punish. It rewards flow.**

---

## FILES CREATED

1. `100X_DEPLOYMENT/NETWORK_ONLY_FEATURES.md` (this file)
2. `100X_DEPLOYMENT/netlify/functions/ability-access.js`
3. `100X_DEPLOYMENT/netlify/functions/network-feature-gate.js`
4. `100X_DEPLOYMENT/netlify/functions/degraded-mode.js`
5. `100X_DEPLOYMENT/netlify/functions/update-contribution.js`
6. `100X_DEPLOYMENT/js/ability-access.js`

---

## NEXT STEPS

1. **Deploy SQL** - Run schema additions in Supabase
2. **Create Functions** - Deploy Netlify functions
3. **Seed Data** - Populate ability_access_control table
4. **Test Access** - Verify tier gates work
5. **Integrate Webhook** - Add contribution recording to stripe-webhook.js

---

*C1 MECHANIC - Extraction stops at the ability level.*
*Flow is the signal. Contribution unlocks power.*
