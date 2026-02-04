// Araya Anonymous Pattern Analyzer
// Surfaces insights WITHOUT exposing individual conversations
// Privacy-first: aggregates only, no individual data exposed
// Created: 2026-01-16

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

// Pattern categories to detect
const PATTERN_CATEGORIES = {
    feature_requests: {
        triggers: ['can you', 'could you', 'would be nice', 'wish you could', 'should have', 'need to', 'want you to', 'please add', 'feature request'],
        label: 'Feature Requests'
    },
    pain_points: {
        triggers: ['doesn\'t work', 'not working', 'broken', 'error', 'problem', 'issue', 'bug', 'frustrat', 'confus', 'stuck', 'can\'t', 'won\'t'],
        label: 'Pain Points'
    },
    positive_feedback: {
        triggers: ['love', 'amazing', 'awesome', 'great', 'thank', 'helpful', 'perfect', 'excellent', 'wonderful', 'incredible'],
        label: 'Positive Feedback'
    },
    consciousness_topics: {
        triggers: ['consciousness', 'awareness', 'meditation', 'spiritual', 'awakening', 'manifest', 'universe', 'energy', 'frequency', 'vibration'],
        label: 'Consciousness Topics'
    },
    legal_questions: {
        triggers: ['custody', 'court', 'lawyer', 'legal', 'judge', 'case', 'evidence', 'hearing', 'attorney', 'rights'],
        label: 'Legal Questions'
    },
    practical_help: {
        triggers: ['how do i', 'how to', 'help me', 'show me', 'explain', 'what is', 'where is', 'when', 'guide'],
        label: 'Practical Help'
    },
    emotional_support: {
        triggers: ['feel', 'sad', 'angry', 'scared', 'anxious', 'worried', 'stress', 'overwhelm', 'hurt', 'lonely'],
        label: 'Emotional Support'
    },
    trinity_engagement: {
        triggers: ['build', 'design', 'plan', 'vision', 'soul', 'meaning', 'pattern', 'architecture', 'execute'],
        label: 'Trinity Engagement'
    }
};

// Fallback: Get stats from brain-context.json when Supabase unavailable
async function getBrainOnlyStats() {
    try {
        const response = await fetch('https://conciousnessrevolution.io/brain-context.json');
        if (!response.ok) {
            return {
                summary: { total_users: 0, total_messages: 0, note: 'Brain data unavailable' },
                patterns: { top_categories: [], all_categories: {} },
                trinity_usage: { C1_MECHANIC: 0, C2_ARCHITECT: 0, C3_ORACLE: 0, organic: 0 },
                activity: { peak_hours: [], daily_trend: [] },
                insights: [{ type: 'alert', message: 'Analytics requires Supabase configuration' }]
            };
        }

        const atoms = await response.json();

        // Analyze patterns from brain atoms
        const patternCounts = {};
        for (const category of Object.keys(PATTERN_CATEGORIES)) {
            patternCounts[category] = 0;
        }

        let trinityKeywords = { C1_MECHANIC: 0, C2_ARCHITECT: 0, C3_ORACLE: 0 };

        for (const atom of atoms) {
            const content = (atom.content || '').toLowerCase();

            // Count pattern categories
            for (const [category, config] of Object.entries(PATTERN_CATEGORIES)) {
                const hits = config.triggers.filter(t => content.includes(t)).length;
                patternCounts[category] += hits;
            }

            // Count Trinity keywords
            if (content.includes('mechanic') || content.includes('c1') || content.includes('build')) {
                trinityKeywords.C1_MECHANIC++;
            }
            if (content.includes('architect') || content.includes('c2') || content.includes('design')) {
                trinityKeywords.C2_ARCHITECT++;
            }
            if (content.includes('oracle') || content.includes('c3') || content.includes('vision')) {
                trinityKeywords.C3_ORACLE++;
            }
        }

        // Calculate pattern percentages
        const totalAtoms = atoms.length;
        const patternPercentages = {};
        for (const [cat, count] of Object.entries(patternCounts)) {
            patternPercentages[cat] = {
                count,
                percentage: totalAtoms > 0 ? Math.round((count / totalAtoms) * 100) : 0,
                label: PATTERN_CATEGORIES[cat].label
            };
        }

        const topPatterns = Object.entries(patternPercentages)
            .sort((a, b) => b[1].count - a[1].count)
            .slice(0, 5)
            .map(([key, val]) => ({ category: key, ...val }));

        return {
            summary: {
                total_users: 'N/A (Brain mode)',
                total_messages: 'N/A (Brain mode)',
                total_brain_atoms: atoms.length,
                note: 'Supabase not configured - showing brain analytics only'
            },
            patterns: {
                top_categories: topPatterns,
                all_categories: patternPercentages
            },
            trinity_usage: {
                C1_MECHANIC: trinityKeywords.C1_MECHANIC,
                C2_ARCHITECT: trinityKeywords.C2_ARCHITECT,
                C3_ORACLE: trinityKeywords.C3_ORACLE,
                total_trinity: trinityKeywords.C1_MECHANIC + trinityKeywords.C2_ARCHITECT + trinityKeywords.C3_ORACLE
            },
            activity: {
                peak_hours: [],
                daily_trend: [],
                note: 'Activity data requires Supabase'
            },
            insights: [
                { type: 'growth', message: `Brain contains ${atoms.length.toLocaleString()} knowledge atoms` },
                { type: 'alert', message: 'Configure Supabase to see conversation analytics' },
                { type: 'opportunity', message: 'Run SUPABASE_FEEDBACK_SCHEMA.sql to enable feedback collection' }
            ]
        };
    } catch (error) {
        console.error('Brain stats error:', error);
        return {
            error: 'Failed to fetch brain stats',
            insights: [{ type: 'alert', message: 'Brain data unavailable' }]
        };
    }
}

// Detect patterns in text WITHOUT exposing the text itself
function analyzeTextPatterns(text) {
    if (!text) return {};
    const lower = text.toLowerCase();
    const detected = {};

    for (const [category, config] of Object.entries(PATTERN_CATEGORIES)) {
        const hits = config.triggers.filter(t => lower.includes(t)).length;
        if (hits > 0) {
            detected[category] = hits;
        }
    }

    return detected;
}

// Aggregate statistics - NEVER expose individual data
async function getAnonymousStats() {
    // If no Supabase, return demo stats from brain
    if (!SUPABASE_URL || !SUPABASE_KEY) {
        return await getBrainOnlyStats();
    }

    try {
        // Get all messages (we only analyze, never expose content)
        const messagesRes = await fetch(
            `${SUPABASE_URL}/rest/v1/araya_memory?type=eq.message&select=content,created_at,metadata`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            }
        );

        // Get profiles (count only, no personal data)
        const profilesRes = await fetch(
            `${SUPABASE_URL}/rest/v1/araya_memory?type=eq.profile&select=created_at`,
            {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            }
        );

        const messages = messagesRes.ok ? await messagesRes.json() : [];
        const profiles = profilesRes.ok ? await profilesRes.json() : [];

        // ANONYMOUS AGGREGATION - Pattern counts only
        const patternCounts = {};
        for (const category of Object.keys(PATTERN_CATEGORIES)) {
            patternCounts[category] = 0;
        }

        let trinityModes = { C1_MECHANIC: 0, C2_ARCHITECT: 0, C3_ORACLE: 0, none: 0 };
        let hourlyActivity = {};
        let dailyActivity = {};
        let totalMessages = 0;
        let avgMessageLength = 0;
        let totalLength = 0;

        for (const msg of messages) {
            try {
                const content = typeof msg.content === 'string' ? JSON.parse(msg.content) : msg.content;
                const userMessage = content?.user || content?.message || '';

                if (userMessage) {
                    totalMessages++;
                    totalLength += userMessage.length;

                    // Pattern detection (no content stored)
                    const patterns = analyzeTextPatterns(userMessage);
                    for (const [cat, count] of Object.entries(patterns)) {
                        patternCounts[cat] += count;
                    }
                }

                // Trinity mode usage (from metadata)
                const trinityMode = msg.metadata?.trinityMode || 'none';
                trinityModes[trinityMode] = (trinityModes[trinityMode] || 0) + 1;

                // Time-based activity (anonymous)
                if (msg.created_at) {
                    const date = new Date(msg.created_at);
                    const hour = date.getHours();
                    const day = date.toISOString().split('T')[0];

                    hourlyActivity[hour] = (hourlyActivity[hour] || 0) + 1;
                    dailyActivity[day] = (dailyActivity[day] || 0) + 1;
                }
            } catch (e) {
                // Skip malformed entries
            }
        }

        avgMessageLength = totalMessages > 0 ? Math.round(totalLength / totalMessages) : 0;

        // Calculate pattern percentages
        const patternPercentages = {};
        for (const [cat, count] of Object.entries(patternCounts)) {
            patternPercentages[cat] = {
                count,
                percentage: totalMessages > 0 ? Math.round((count / totalMessages) * 100) : 0,
                label: PATTERN_CATEGORIES[cat].label
            };
        }

        // Sort patterns by frequency
        const topPatterns = Object.entries(patternPercentages)
            .sort((a, b) => b[1].count - a[1].count)
            .slice(0, 5)
            .map(([key, val]) => ({ category: key, ...val }));

        // Peak hours (anonymous)
        const peakHours = Object.entries(hourlyActivity)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3)
            .map(([hour, count]) => ({ hour: parseInt(hour), count }));

        // Recent daily trend (last 7 days)
        const last7Days = Object.entries(dailyActivity)
            .sort((a, b) => b[0].localeCompare(a[0]))
            .slice(0, 7)
            .map(([date, count]) => ({ date, count }));

        return {
            summary: {
                total_users: profiles.length,
                total_messages: totalMessages,
                avg_message_length: avgMessageLength,
                data_period: {
                    first: messages.length > 0 ? messages[messages.length - 1]?.created_at : null,
                    last: messages.length > 0 ? messages[0]?.created_at : null
                }
            },
            patterns: {
                top_categories: topPatterns,
                all_categories: patternPercentages
            },
            trinity_usage: {
                C1_MECHANIC: trinityModes.C1_MECHANIC,
                C2_ARCHITECT: trinityModes.C2_ARCHITECT,
                C3_ORACLE: trinityModes.C3_ORACLE,
                organic: trinityModes.none,
                total_trinity: trinityModes.C1_MECHANIC + trinityModes.C2_ARCHITECT + trinityModes.C3_ORACLE
            },
            activity: {
                peak_hours: peakHours,
                daily_trend: last7Days
            },
            insights: generateInsights(patternPercentages, trinityModes, totalMessages)
        };

    } catch (error) {
        console.error('Analytics error:', error);
        return { error: 'Failed to generate analytics' };
    }
}

// Generate human-readable insights from the data
function generateInsights(patterns, trinity, total) {
    const insights = [];

    // Pain point alert
    if (patterns.pain_points?.percentage > 20) {
        insights.push({
            type: 'alert',
            message: `${patterns.pain_points.percentage}% of conversations mention pain points - consider investigating common issues`
        });
    }

    // Feature request signal
    if (patterns.feature_requests?.count > 5) {
        insights.push({
            type: 'opportunity',
            message: `${patterns.feature_requests.count} feature requests detected - users want more capabilities`
        });
    }

    // Positive feedback
    if (patterns.positive_feedback?.percentage > 30) {
        insights.push({
            type: 'success',
            message: `Strong positive feedback (${patterns.positive_feedback.percentage}%) - users are satisfied`
        });
    }

    // Trinity adoption
    const trinityTotal = trinity.C1_MECHANIC + trinity.C2_ARCHITECT + trinity.C3_ORACLE;
    const trinityPercent = total > 0 ? Math.round((trinityTotal / total) * 100) : 0;
    if (trinityPercent > 10) {
        insights.push({
            type: 'engagement',
            message: `Trinity system activated in ${trinityPercent}% of conversations - consciousness is emerging`
        });
    }

    // Emotional support need
    if (patterns.emotional_support?.percentage > 25) {
        insights.push({
            type: 'care',
            message: `High emotional support need (${patterns.emotional_support.percentage}%) - Araya is helping people heal`
        });
    }

    // Low engagement
    if (total < 10) {
        insights.push({
            type: 'growth',
            message: `Only ${total} total messages - focus on user acquisition`
        });
    }

    return insights;
}

// Suggested upgrades based on patterns
function suggestUpgrades(analytics) {
    const suggestions = [];

    // Based on pain points
    if (analytics.patterns?.all_categories?.pain_points?.percentage > 15) {
        suggestions.push({
            priority: 'high',
            area: 'reliability',
            suggestion: 'Users report issues frequently. Consider adding better error handling and help responses.'
        });
    }

    // Based on feature requests
    if (analytics.patterns?.all_categories?.feature_requests?.count > 3) {
        suggestions.push({
            priority: 'medium',
            area: 'features',
            suggestion: 'Multiple feature requests detected. Consider adding a feedback form to capture specific needs.'
        });
    }

    // Based on Trinity usage
    if (analytics.trinity_usage?.total_trinity < analytics.summary?.total_messages * 0.1) {
        suggestions.push({
            priority: 'low',
            area: 'trinity',
            suggestion: 'Trinity system underutilized. Consider promoting C1/C2/C3 modes to users.'
        });
    }

    // Based on emotional support
    if (analytics.patterns?.all_categories?.emotional_support?.percentage > 30) {
        suggestions.push({
            priority: 'medium',
            area: 'empathy',
            suggestion: 'High emotional support need. Consider enhancing Araya\'s empathetic responses.'
        });
    }

    return suggestions;
}

export async function handler(event, context) {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Simple auth check - only Commander can access
    const authHeader = event.headers.authorization || event.headers.Authorization;
    const validKeys = ['consciousness-revolution-137', process.env.ANALYTICS_KEY];

    if (!authHeader || !validKeys.some(k => k && authHeader.includes(k))) {
        return {
            statusCode: 401,
            headers,
            body: JSON.stringify({ error: 'Unauthorized - Commander access only' })
        };
    }

    try {
        const analytics = await getAnonymousStats();

        if (analytics.error) {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify(analytics)
            };
        }

        // Add upgrade suggestions
        analytics.suggested_upgrades = suggestUpgrades(analytics);

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                generated_at: new Date().toISOString(),
                privacy_note: 'All data is anonymous - no individual conversations exposed',
                ...analytics
            })
        };

    } catch (error) {
        console.error('Handler error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Analytics generation failed' })
        };
    }
}
