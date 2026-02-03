// ability-access.mjs
// Ability Access Controller - Check if builder can use abilities at full power

import { createClient } from '@supabase/supabase-js';

const ABILITY_TYPES = {
    STANDALONE: 'standalone',
    NETWORK_ENHANCED: 'network_enhanced',
    NETWORK_REQUIRED: 'network_required'
};

const TIER_REQUIREMENTS = {
    GHOST: 0,
    SEEDLING: 1,
    SAPLING: 50,
    TREE: 200,
    FOREST: 500
};

const TIER_MULTIPLIERS = {
    GHOST: 0.6,
    SEEDLING: 0.7,
    SAPLING: 0.8,
    TREE: 0.9,
    FOREST: 1.0
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
            message: 'Full access (default)'
        };
    }

    const tier = status?.contribution_tier || 'GHOST';
    const score = status?.contribution_score || 0;

    // Standalone abilities always work at full power
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
        const requiredRank = Object.keys(TIER_REQUIREMENTS).indexOf(ability.min_tier_required || 'GHOST');

        if (tierRank < requiredRank) {
            return {
                allowed: false,
                power_level: 0,
                access_type: 'network_required',
                current_tier: tier,
                current_score: score,
                required_tier: ability.min_tier_required,
                message: `Requires ${ability.min_tier_required} tier. You are ${tier}. Contribute to unlock.`,
                upgrade_hint: getUpgradeHint(tier)
            };
        }

        return {
            allowed: true,
            power_level: 100,
            access_type: 'network_required',
            current_tier: tier,
            message: 'Network access granted'
        };
    }

    // Network-enhanced abilities work but with degraded power
    if (ability.access_type === ABILITY_TYPES.NETWORK_ENHANCED) {
        const multiplier = TIER_MULTIPLIERS[tier] || 0.6;
        const powerLevel = Math.round((ability.offline_power_pct || 100) * multiplier);

        return {
            allowed: true,
            power_level: powerLevel,
            access_type: 'network_enhanced',
            current_tier: tier,
            current_score: score,
            message: powerLevel < 100
                ? `Operating at ${powerLevel}% power. Contribute to unlock full power.`
                : 'Full network power',
            network_features: ability.network_features || [],
            degraded_behavior: powerLevel < 100 ? ability.degraded_behavior : null,
            upgrade_hint: powerLevel < 100 ? getUpgradeHint(tier) : null
        };
    }

    return { allowed: true, power_level: 100 };
}

function getUpgradeHint(currentTier) {
    const hints = {
        GHOST: 'Publish your first creation to the marketplace to become a SEEDLING (+10 points)',
        SEEDLING: 'Make 5 marketplace sales or share 10 patterns to become a SAPLING (need 50 points)',
        SAPLING: 'Reach 200 points through sales and contributions to become a TREE',
        TREE: 'Maintain consistent contribution (500+ points) to become a FOREST leader'
    };
    return hints[currentTier] || 'Keep contributing to the network';
}

async function checkBulkAbilityAccess(supabase, foundationId, abilityNames) {
    const results = {};
    for (const name of abilityNames) {
        results[name] = await checkAbilityAccess(supabase, foundationId, name);
    }
    return results;
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

    const { foundation_id, ability_name, abilities } = body;

    if (!foundation_id) {
        return new Response(JSON.stringify({ error: 'foundation_id required' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        let result;

        if (abilities && Array.isArray(abilities)) {
            result = await checkBulkAbilityAccess(supabase, foundation_id, abilities);
        } else if (ability_name) {
            result = await checkAbilityAccess(supabase, foundation_id, ability_name);
        } else {
            return new Response(JSON.stringify({ error: 'ability_name or abilities[] required' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        // Log access attempt (non-blocking)
        supabase.from('network_feature_access').insert({
            foundation_id,
            feature_name: ability_name || 'bulk_check',
            access_granted: result.allowed !== false,
            contribution_tier: result.current_tier || 'GHOST'
        }).then(() => {});

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
