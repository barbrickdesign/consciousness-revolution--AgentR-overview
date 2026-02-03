// network-feature-gate.mjs
// Network Feature Gate - Check/list network-only features by tier

import { createClient } from '@supabase/supabase-js';

// All network-only features with tier requirements
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
    pattern_library_read: { min_tier: 'SAPLING', description: 'Access 10,000+ shared patterns' },
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

const TIER_THRESHOLDS = {
    GHOST: 0,
    SEEDLING: 1,
    SAPLING: 50,
    TREE: 200,
    FOREST: 500
};

async function checkFeatureAccess(supabase, foundationId, featureName) {
    const feature = NETWORK_FEATURES[featureName];

    if (!feature) {
        return {
            allowed: false,
            reason: 'Unknown feature',
            feature: featureName
        };
    }

    const { data: status } = await supabase
        .from('builder_network_status')
        .select('contribution_tier, contribution_score')
        .eq('foundation_id', foundationId)
        .single();

    const currentTier = status?.contribution_tier || 'GHOST';
    const currentScore = status?.contribution_score || 0;
    const currentRank = TIER_RANKS.indexOf(currentTier);
    const requiredRank = TIER_RANKS.indexOf(feature.min_tier);

    if (currentRank < requiredRank) {
        return {
            allowed: false,
            feature: featureName,
            description: feature.description,
            current_tier: currentTier,
            required_tier: feature.min_tier,
            contribution_score: currentScore,
            points_to_next_tier: getPointsToNextTier(currentTier, currentScore),
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

async function getAvailableFeatures(supabase, foundationId) {
    const { data: status } = await supabase
        .from('builder_network_status')
        .select('contribution_tier, contribution_score')
        .eq('foundation_id', foundationId)
        .single();

    const currentTier = status?.contribution_tier || 'GHOST';
    const currentScore = status?.contribution_score || 0;
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
        contribution_score: currentScore,
        available_features: available,
        locked_features: locked,
        next_tier: TIER_RANKS[currentRank + 1] || null,
        points_to_next_tier: getPointsToNextTier(currentTier, currentScore),
        tier_progress: getTierProgress(currentTier, currentScore)
    };
}

function getPointsToNextTier(currentTier, currentScore) {
    const nextTierIndex = TIER_RANKS.indexOf(currentTier) + 1;
    if (nextTierIndex >= TIER_RANKS.length) return 0;

    const nextTier = TIER_RANKS[nextTierIndex];
    return Math.max(0, TIER_THRESHOLDS[nextTier] - currentScore);
}

function getTierProgress(currentTier, currentScore) {
    const currentThreshold = TIER_THRESHOLDS[currentTier];
    const nextTierIndex = TIER_RANKS.indexOf(currentTier) + 1;

    if (nextTierIndex >= TIER_RANKS.length) {
        return { percentage: 100, message: 'Maximum tier reached' };
    }

    const nextTier = TIER_RANKS[nextTierIndex];
    const nextThreshold = TIER_THRESHOLDS[nextTier];
    const range = nextThreshold - currentThreshold;
    const progress = currentScore - currentThreshold;
    const percentage = Math.round((progress / range) * 100);

    return {
        percentage: Math.min(100, Math.max(0, percentage)),
        current: currentScore,
        target: nextThreshold,
        remaining: nextThreshold - currentScore,
        next_tier: nextTier
    };
}

export default async (req) => {
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    let body;
    try {
        body = await req.json();
    } catch {
        body = {};
    }

    const { action, foundation_id, feature_name } = body;

    if (!foundation_id && action !== 'all_features') {
        return new Response(JSON.stringify({ error: 'foundation_id required' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        let result;

        switch (action) {
            case 'check':
                if (!feature_name) {
                    return new Response(JSON.stringify({ error: 'feature_name required' }), {
                        status: 400,
                        headers: { 'Content-Type': 'application/json' }
                    });
                }
                result = await checkFeatureAccess(supabase, foundation_id, feature_name);
                break;

            case 'list':
                result = await getAvailableFeatures(supabase, foundation_id);
                break;

            case 'all_features':
                result = {
                    features: NETWORK_FEATURES,
                    tiers: TIER_RANKS,
                    thresholds: TIER_THRESHOLDS
                };
                break;

            default:
                result = await getAvailableFeatures(supabase, foundation_id);
        }

        // Log access (non-blocking)
        if (foundation_id) {
            supabase.from('network_feature_access').insert({
                foundation_id,
                feature_name: feature_name || 'list_features',
                access_granted: result.allowed !== false,
                contribution_tier: result.current_tier || 'GHOST'
            }).then(() => {});
        }

        return new Response(JSON.stringify(result), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

// Config removed - using netlify.toml redirect instead
