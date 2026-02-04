// Discord Community API - Live data for community.html
// Queries discord_users + xp_log from Supabase
// Pattern: direct REST (no SDK) from araya-memory.mjs

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY;

async function supabase(table, query = '') {
    const url = `${SUPABASE_URL}/rest/v1/${table}${query}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'apikey': SUPABASE_KEY,
            'Authorization': `Bearer ${SUPABASE_KEY}`,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(`Supabase ${table}: ${error}`);
    }

    return response.json();
}

// Role gradient map (matches community.html theme)
const ROLE_GRADIENTS = {
    'Commander': 'linear-gradient(135deg,#f59e0b,#ef4444)',
    'Architect': 'linear-gradient(135deg,#8b5cf6,#6366f1)',
    'Builder':   'linear-gradient(135deg,#00f0ff,#0ea5e9)',
    'Oracle':    'linear-gradient(135deg,#ec4899,#8b5cf6)',
    'Seedling':  'linear-gradient(135deg,#22c55e,#0ea5e9)',
    'default':   'linear-gradient(135deg,#6366f1,#0ea5e9)'
};

function getGradient(role) {
    return ROLE_GRADIENTS[role] || ROLE_GRADIENTS['default'];
}

function getInitials(name) {
    if (!name) return '??';
    const parts = name.replace(/[^a-zA-Z0-9 .]/g, '').trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
}

function mapRole(level) {
    if (level >= 5) return 'Commander';
    if (level >= 4) return 'Architect';
    if (level >= 3) return 'Oracle';
    if (level >= 2) return 'Builder';
    return 'Seedling';
}

function timeAgo(timestamp) {
    const now = new Date();
    const then = new Date(timestamp);
    const diff = Math.floor((now - then) / 1000);
    if (diff < 60) return 'just now';
    if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
    if (diff < 604800) return Math.floor(diff / 86400) + 'd ago';
    return then.toLocaleDateString();
}

export async function handler(event) {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'GET') {
        return { statusCode: 405, headers, body: JSON.stringify({ error: 'GET only' }) };
    }

    const params = event.queryStringParameters || {};
    const type = params.type || 'all';

    try {
        const result = {};

        // Members: from discord_users ordered by total_xp
        if (type === 'members' || type === 'all') {
            const users = await supabase('discord_users',
                '?select=user_id,username,current_level,total_xp,builder_score,last_active,verification_status&order=total_xp.desc&limit=30'
            );

            result.members = users.map(u => ({
                name: u.username || 'Unknown',
                initials: getInitials(u.username),
                role: mapRole(u.current_level || 0),
                score: u.builder_score || u.total_xp || 0,
                gradient: getGradient(mapRole(u.current_level || 0)),
                level: u.current_level || 0,
                verified: u.verification_status === 'verified',
                lastActive: u.last_active
            }));
        }

        // Activity: from xp_log (recent actions as a feed)
        if (type === 'activity' || type === 'all') {
            const activity = await supabase('xp_log',
                '?select=user_id,xp_amount,reason,timestamp&order=timestamp.desc&limit=20'
            );

            // Get usernames for the activity entries
            const userIds = [...new Set(activity.map(a => a.user_id))];
            let userMap = {};
            if (userIds.length > 0) {
                const userFilter = userIds.map(id => `user_id.eq.${id}`).join(',');
                const actUsers = await supabase('discord_users',
                    `?select=user_id,username,current_level&or=(${userFilter})`
                );
                actUsers.forEach(u => { userMap[u.user_id] = u; });
            }

            result.activity = activity.map(a => {
                const u = userMap[a.user_id] || {};
                const username = u.username || 'Builder';
                const role = mapRole(u.current_level || 0);
                return {
                    user: username,
                    initials: getInitials(username),
                    gradient: getGradient(role),
                    time: timeAgo(a.timestamp),
                    channel: 'activity',
                    text: a.reason || `Earned ${a.xp_amount} XP`,
                    xp: a.xp_amount
                };
            });
        }

        // Stats
        if (type === 'stats' || type === 'all') {
            const allUsers = await supabase('discord_users', '?select=user_id&limit=1000');
            const recentXp = await supabase('xp_log',
                '?select=xp_amount&timestamp=gte.' + new Date(Date.now() - 86400000).toISOString() + '&limit=1000'
            );

            result.stats = {
                totalMembers: allUsers.length,
                totalXpToday: recentXp.reduce((sum, x) => sum + (x.xp_amount || 0), 0),
                activeLast24h: recentXp.length,
                lastUpdated: new Date().toISOString()
            };
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ success: true, data: result })
        };

    } catch (error) {
        console.error('Discord community API error:', error.message);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                success: false,
                error: error.message,
                fallback: true
            })
        };
    }
}
