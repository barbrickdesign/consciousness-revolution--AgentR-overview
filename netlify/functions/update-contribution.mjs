// update-contribution.mjs
// Contribution Score Updater - Record contributions and update tier

import { createClient } from '@supabase/supabase-js';

// Point values for different contribution actions
const CONTRIBUTION_POINTS = {
    creation_published: 10,
    marketplace_sale: 5,
    downstream_derivative: 20,
    bug_reported: 2,
    pattern_shared: 3,
    community_help: 1,
    daily_active: 0.1,
    review_given: 2,
    tutorial_completed: 1,
    referral: 15
};

const TIER_THRESHOLDS = {
    GHOST: 0,
    SEEDLING: 1,
    SAPLING: 50,
    TREE: 200,
    FOREST: 500
};

const TIER_RANKS = ['GHOST', 'SEEDLING', 'SAPLING', 'TREE', 'FOREST'];

function calculateTier(score) {
    if (score >= TIER_THRESHOLDS.FOREST) return 'FOREST';
    if (score >= TIER_THRESHOLDS.TREE) return 'TREE';
    if (score >= TIER_THRESHOLDS.SAPLING) return 'SAPLING';
    if (score >= TIER_THRESHOLDS.SEEDLING) return 'SEEDLING';
    return 'GHOST';
}

function getFeaturesByTier(tier) {
    const features = {
        GHOST: [],
        SEEDLING: ['version_updates', 'community_help', 'marketplace_browse'],
        SAPLING: ['marketplace_buy', 'marketplace_sell', 'pattern_library_read', 'bug_fixes_instant', 'ai_model_access'],
        TREE: ['downstream_revenue', 'pattern_library_write', 'priority_support', 'cell_creation', 'beta_features', 'marketplace_featured'],
        FOREST: ['full_api_access', 'custom_revenue_terms', 'white_label', 'cell_leadership']
    };

    // Accumulate features from all lower tiers
    const tierIndex = TIER_RANKS.indexOf(tier);
    let accumulated = [];
    for (let i = 0; i <= tierIndex; i++) {
        accumulated = [...accumulated, ...features[TIER_RANKS[i]]];
    }
    return accumulated;
}

async function recordContribution(supabase, foundationId, contributionType, metadata = {}) {
    const points = CONTRIBUTION_POINTS[contributionType];

    if (points === undefined) {
        return {
            success: false,
            error: 'Unknown contribution type',
            type: contributionType,
            valid_types: Object.keys(CONTRIBUTION_POINTS)
        };
    }

    // Get or create current status
    let { data: status } = await supabase
        .from('builder_network_status')
        .select('*')
        .eq('foundation_id', foundationId)
        .single();

    if (!status) {
        const { data: newStatus, error } = await supabase
            .from('builder_network_status')
            .insert({
                foundation_id: foundationId,
                contribution_score: 0,
                contribution_tier: 'GHOST',
                network_features_enabled: []
            })
            .select()
            .single();

        if (error) {
            return { success: false, error: error.message };
        }
        status = newStatus;
    }

    // Calculate new values
    const previousScore = status.contribution_score || 0;
    const previousTier = status.contribution_tier || 'GHOST';
    const newScore = previousScore + points;
    const newTier = calculateTier(newScore);
    const tierChanged = newTier !== previousTier;

    // Build update object
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

    // Update features if tier changed
    if (tierChanged) {
        updates.network_features_enabled = getFeaturesByTier(newTier);
    }

    // Save updates
    const { error: updateError } = await supabase
        .from('builder_network_status')
        .update(updates)
        .eq('foundation_id', foundationId);

    if (updateError) {
        return { success: false, error: updateError.message };
    }

    // Build response
    const response = {
        success: true,
        contribution_type: contributionType,
        points_earned: points,
        previous_score: previousScore,
        new_score: newScore,
        previous_tier: previousTier,
        new_tier: newTier,
        tier_changed: tierChanged
    };

    if (tierChanged) {
        response.unlocked_features = getFeaturesByTier(newTier).filter(
            f => !getFeaturesByTier(previousTier).includes(f)
        );
        response.celebration_message = getCelebrationMessage(newTier);
    }

    // Calculate progress to next tier
    const nextTierIndex = TIER_RANKS.indexOf(newTier) + 1;
    if (nextTierIndex < TIER_RANKS.length) {
        const nextTier = TIER_RANKS[nextTierIndex];
        response.next_tier = nextTier;
        response.points_to_next_tier = TIER_THRESHOLDS[nextTier] - newScore;
    }

    return response;
}

function getCelebrationMessage(tier) {
    const messages = {
        SEEDLING: 'You planted your first seed in the network. Watch it grow.',
        SAPLING: 'Your contributions are taking root. Marketplace access unlocked.',
        TREE: 'You stand tall in the forest. Downstream revenue and cell creation unlocked.',
        FOREST: 'You are the forest itself. Maximum power achieved. Lead the way.'
    };
    return messages[tier] || 'Contribution recorded';
}

async function getContributionHistory(supabase, foundationId, limit = 20) {
    const { data: history } = await supabase
        .from('network_feature_access')
        .select('feature_name, access_granted, accessed_at')
        .eq('foundation_id', foundationId)
        .order('accessed_at', { ascending: false })
        .limit(limit);

    return history || [];
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

    const { action, foundation_id, contribution_type, metadata } = body;

    if (!foundation_id) {
        return new Response(JSON.stringify({ error: 'foundation_id required' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        let result;

        switch (action) {
            case 'record':
            case undefined:
                if (!contribution_type) {
                    return new Response(JSON.stringify({
                        error: 'contribution_type required',
                        valid_types: Object.keys(CONTRIBUTION_POINTS)
                    }), {
                        status: 400,
                        headers: { 'Content-Type': 'application/json' }
                    });
                }
                result = await recordContribution(supabase, foundation_id, contribution_type, metadata);
                break;

            case 'history':
                result = await getContributionHistory(supabase, foundation_id);
                break;

            case 'point_values':
                result = {
                    contribution_points: CONTRIBUTION_POINTS,
                    tier_thresholds: TIER_THRESHOLDS
                };
                break;

            default:
                result = { error: 'Unknown action', valid_actions: ['record', 'history', 'point_values'] };
        }

        return new Response(JSON.stringify(result), {
            status: result.error ? 400 : 200,
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
