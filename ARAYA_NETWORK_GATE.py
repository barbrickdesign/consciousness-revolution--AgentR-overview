"""
ARAYA NETWORK GATE - Anti-Godzilla Protection
==============================================
Gates Araya capabilities based on builder tier.
Extractors can still use Araya, but with degraded power.
Contributors get full network-enhanced features.

The Philosophy: "Privacy is not the signal. FLOW is the signal."
We don't exclude. We let them self-select by making isolation expensive.

Usage:
    from ARAYA_NETWORK_GATE import check_capability, get_tier_info, CAPABILITY_MAP

    access = check_capability(foundation_id, 'pattern_library')
    if not access['allowed']:
        return access['message']
"""

import requests
from functools import wraps
from flask import request, jsonify

# ============================================
# CONFIGURATION
# ============================================

# Ability Access API (deployed via Netlify)
ABILITY_ACCESS_API = "https://consciousnessrevolution.io/.netlify/functions/ability-access"

# Local fallback when offline
LOCAL_FALLBACK = True

# Tier definitions (synced with ability-access.mjs)
TIER_REQUIREMENTS = {
    'GHOST': 0,
    'SEEDLING': 1,
    'SAPLING': 50,
    'TREE': 200,
    'FOREST': 500
}

TIER_MULTIPLIERS = {
    'GHOST': 0.6,
    'SEEDLING': 0.7,
    'SAPLING': 0.8,
    'TREE': 0.9,
    'FOREST': 1.0
}

# ============================================
# ARAYA CAPABILITY CLASSIFICATION
# ============================================

CAPABILITY_MAP = {
    # Type A: STANDALONE - Works offline at full power
    # These are YOURS. No network needed. Ever.
    'basic_chat': {
        'type': 'standalone',
        'power': 100,
        'description': 'Basic conversation and guidance'
    },
    'pattern_theory_basics': {
        'type': 'standalone',
        'power': 100,
        'description': 'Core Pattern Theory principles (3->7->13->infinity)'
    },
    'manipulation_detection': {
        'type': 'standalone',
        'power': 100,
        'description': 'Recognize manipulation patterns'
    },
    'local_file_read': {
        'type': 'standalone',
        'power': 100,
        'description': 'Read files from allowed directories'
    },
    'consciousness_journal': {
        'type': 'standalone',
        'power': 100,
        'description': 'Personal journaling and reflection'
    },

    # Type B: NETWORK-ENHANCED - Works alone but better connected
    # 60% power alone, 100% with contribution
    'pattern_library': {
        'type': 'network_enhanced',
        'offline_power': 60,
        'min_tier': 'GHOST',
        'description': 'Access to shared pattern database',
        'degraded_behavior': 'Only basic patterns available. Contribute to unlock full library.',
        'network_features': ['community_patterns', 'real_time_updates', 'pattern_sharing']
    },
    'file_write': {
        'type': 'network_enhanced',
        'offline_power': 80,
        'min_tier': 'SEEDLING',
        'description': 'Write files to your website',
        'degraded_behavior': 'No automatic backup to cloud. Local only.',
        'network_features': ['cloud_backup', 'version_sync', 'collaboration']
    },
    'advanced_analysis': {
        'type': 'network_enhanced',
        'offline_power': 50,
        'min_tier': 'SAPLING',
        'description': 'Deep pattern analysis with historical context',
        'degraded_behavior': 'Analysis limited to your own history.',
        'network_features': ['aggregate_insights', 'trend_analysis', 'peer_comparison']
    },

    # Type C: NETWORK-REQUIRED - Only works connected
    # These require the network because they ARE the network
    'marketplace_publish': {
        'type': 'network_required',
        'min_tier': 'SEEDLING',
        'description': 'Publish creations to marketplace',
        'unlock_hint': 'Share your first creation to become a SEEDLING'
    },
    'downstream_revenue': {
        'type': 'network_required',
        'min_tier': 'TREE',
        'description': 'Earn 10% from derivative works',
        'unlock_hint': 'Reach TREE tier (200+ points) for passive income'
    },
    'pattern_synthesis': {
        'type': 'network_required',
        'min_tier': 'SAPLING',
        'description': 'AI-powered pattern synthesis across network',
        'unlock_hint': 'Reach SAPLING tier (50+ points) to unlock synthesis'
    },
    'builder_dashboard': {
        'type': 'network_required',
        'min_tier': 'SEEDLING',
        'description': 'Full revenue and contribution dashboard',
        'unlock_hint': 'Make your first contribution to unlock dashboard'
    },
    'white_label': {
        'type': 'network_required',
        'min_tier': 'FOREST',
        'description': 'Full white-label Araya deployment',
        'unlock_hint': 'Reach FOREST tier (500+ points) for white-label'
    },
    'api_access': {
        'type': 'network_required',
        'min_tier': 'FOREST',
        'description': 'Direct API access for integrations',
        'unlock_hint': 'Reach FOREST tier for full API access'
    }
}

# ============================================
# CORE FUNCTIONS
# ============================================

def get_tier_rank(tier):
    """Get numeric rank for tier comparison"""
    tiers = list(TIER_REQUIREMENTS.keys())
    return tiers.index(tier) if tier in tiers else 0

def check_capability_local(tier, capability_name):
    """Check capability access locally (for offline/fallback)"""
    capability = CAPABILITY_MAP.get(capability_name)

    if not capability:
        # Unknown capability - default to allowed (standalone)
        return {
            'allowed': True,
            'power_level': 100,
            'access_type': 'standalone',
            'message': 'Full access (unknown capability defaults to standalone)'
        }

    cap_type = capability.get('type')

    # Standalone - always full power
    if cap_type == 'standalone':
        return {
            'allowed': True,
            'power_level': 100,
            'access_type': 'standalone',
            'message': f"Full offline access: {capability.get('description')}"
        }

    # Network-required - check tier
    if cap_type == 'network_required':
        min_tier = capability.get('min_tier', 'GHOST')
        if get_tier_rank(tier) < get_tier_rank(min_tier):
            return {
                'allowed': False,
                'power_level': 0,
                'access_type': 'network_required',
                'current_tier': tier,
                'required_tier': min_tier,
                'message': f"Requires {min_tier} tier. You are {tier}.",
                'upgrade_hint': capability.get('unlock_hint', 'Contribute to unlock')
            }
        return {
            'allowed': True,
            'power_level': 100,
            'access_type': 'network_required',
            'current_tier': tier,
            'message': f"Network access granted: {capability.get('description')}"
        }

    # Network-enhanced - degraded power based on tier
    if cap_type == 'network_enhanced':
        multiplier = TIER_MULTIPLIERS.get(tier, 0.6)
        offline_power = capability.get('offline_power', 100)
        power_level = int(offline_power * multiplier)

        return {
            'allowed': True,
            'power_level': power_level,
            'access_type': 'network_enhanced',
            'current_tier': tier,
            'message': f"Operating at {power_level}% power." if power_level < 100 else f"Full network power: {capability.get('description')}",
            'degraded_behavior': capability.get('degraded_behavior') if power_level < 100 else None,
            'network_features': capability.get('network_features', []),
            'upgrade_hint': get_upgrade_hint(tier) if power_level < 100 else None
        }

    return {'allowed': True, 'power_level': 100}

def check_capability(foundation_id, capability_name):
    """
    Check if a builder can use a capability.
    First tries network API, falls back to local.
    """
    # Try network API first
    try:
        response = requests.post(
            ABILITY_ACCESS_API,
            json={
                'foundation_id': foundation_id,
                'ability_name': capability_name
            },
            timeout=5
        )

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[NetworkGate] API unavailable: {e}")

    # Fallback to local check
    if LOCAL_FALLBACK:
        # Get tier from local cache or default to GHOST
        tier = get_cached_tier(foundation_id) or 'GHOST'
        return check_capability_local(tier, capability_name)

    # If no fallback, assume standalone access
    return {
        'allowed': True,
        'power_level': 60,  # Degraded but functional
        'access_type': 'offline_fallback',
        'message': 'Operating offline. Connect to network for full power.'
    }

def get_cached_tier(foundation_id):
    """Get tier from local cache (Cyclotron)"""
    # TODO: Implement Cyclotron lookup for cached tier
    # For now, default to GHOST
    return 'GHOST'

def get_upgrade_hint(current_tier):
    """Get hint for upgrading to next tier"""
    hints = {
        'GHOST': 'Publish your first creation to become SEEDLING (+10 points)',
        'SEEDLING': 'Make 5 marketplace sales or share 10 patterns to become SAPLING (need 50 points)',
        'SAPLING': 'Reach 200 points through sales and contributions to become TREE',
        'TREE': 'Maintain consistent contribution (500+ points) to become FOREST leader'
    }
    return hints.get(current_tier, 'Keep contributing to the network')

def get_tier_info(foundation_id=None):
    """Get full tier information for a builder"""
    if foundation_id:
        try:
            response = requests.post(
                ABILITY_ACCESS_API,
                json={
                    'foundation_id': foundation_id,
                    'abilities': list(CAPABILITY_MAP.keys())
                },
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass

    # Return default info
    return {
        'tier': 'GHOST',
        'score': 0,
        'capabilities': {
            name: check_capability_local('GHOST', name)
            for name in CAPABILITY_MAP
        }
    }

# ============================================
# FLASK MIDDLEWARE / DECORATORS
# ============================================

def require_capability(capability_name):
    """
    Decorator to gate Flask endpoints by capability.

    Usage:
        @app.route('/advanced-analysis')
        @require_capability('advanced_analysis')
        def advanced_analysis():
            # Only runs if user has access
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get foundation_id from request
            foundation_id = None

            if request.method == 'POST':
                data = request.get_json(silent=True) or {}
                foundation_id = data.get('foundation_id')
            else:
                foundation_id = request.args.get('foundation_id')

            # Check capability
            access = check_capability(foundation_id, capability_name)

            if not access.get('allowed'):
                return jsonify({
                    'error': 'capability_locked',
                    'capability': capability_name,
                    'current_tier': access.get('current_tier', 'GHOST'),
                    'required_tier': access.get('required_tier'),
                    'message': access.get('message'),
                    'upgrade_hint': access.get('upgrade_hint')
                }), 403

            # Attach access info to request for use in endpoint
            request.capability_access = access

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_power_level(capability_name):
    """
    Get power level for current request context.
    Call this inside an endpoint to adjust behavior.
    """
    access = getattr(request, 'capability_access', None)
    if access:
        return access.get('power_level', 100)
    return 100

# ============================================
# ARAYA-SPECIFIC GATING
# ============================================

def gate_araya_response(capability_name, foundation_id, full_response, degraded_response):
    """
    Return full or degraded response based on capability access.

    Usage:
        return gate_araya_response(
            'pattern_library',
            foundation_id,
            full_response=get_full_patterns(),
            degraded_response=get_basic_patterns()
        )
    """
    access = check_capability(foundation_id, capability_name)

    if not access.get('allowed'):
        return {
            'response': f"This capability requires {access.get('required_tier')} tier. {access.get('upgrade_hint', '')}",
            'locked': True,
            'upgrade_hint': access.get('upgrade_hint')
        }

    power_level = access.get('power_level', 100)

    if power_level >= 100:
        return {
            'response': full_response,
            'power_level': 100
        }
    else:
        return {
            'response': degraded_response,
            'power_level': power_level,
            'note': f"Operating at {power_level}% power. {access.get('degraded_behavior', '')}"
        }

def enhance_araya_prompt(base_prompt, foundation_id):
    """
    Enhance Araya's system prompt based on builder tier.
    Higher tiers get more network context.
    """
    tier_info = get_tier_info(foundation_id)
    tier = tier_info.get('tier', 'GHOST')

    # Base prompt additions by tier
    tier_additions = {
        'GHOST': "\n\nNote: User is in GHOST tier. Focus on standalone capabilities.",
        'SEEDLING': "\n\nUser is a SEEDLING contributor. Include marketplace and community features.",
        'SAPLING': "\n\nUser is a SAPLING with growing contribution. Unlock advanced pattern analysis.",
        'TREE': "\n\nUser is a TREE leader. Full network features including downstream revenue.",
        'FOREST': "\n\nUser is FOREST tier. Maximum access. Include API and white-label options."
    }

    return base_prompt + tier_additions.get(tier, '')

# ============================================
# EXPORT
# ============================================

__all__ = [
    'check_capability',
    'check_capability_local',
    'get_tier_info',
    'require_capability',
    'get_power_level',
    'gate_araya_response',
    'enhance_araya_prompt',
    'CAPABILITY_MAP',
    'TIER_REQUIREMENTS',
    'TIER_MULTIPLIERS'
]

if __name__ == '__main__':
    # Test the gating system
    print("="*50)
    print("ARAYA NETWORK GATE - Test")
    print("="*50)

    # Test each capability for GHOST tier
    print("\nGHOST tier access:")
    for cap_name in CAPABILITY_MAP:
        access = check_capability_local('GHOST', cap_name)
        status = "✓" if access['allowed'] else "✗"
        power = access.get('power_level', 0)
        print(f"  {status} {cap_name}: {power}% power")

    # Test each capability for FOREST tier
    print("\nFOREST tier access:")
    for cap_name in CAPABILITY_MAP:
        access = check_capability_local('FOREST', cap_name)
        status = "✓" if access['allowed'] else "✗"
        power = access.get('power_level', 0)
        print(f"  {status} {cap_name}: {power}% power")

    print("\n" + "="*50)
