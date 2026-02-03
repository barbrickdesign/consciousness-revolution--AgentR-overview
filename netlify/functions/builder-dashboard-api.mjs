/**
 * BUILDER DASHBOARD API
 * Get builder's earnings, creations, and stats
 *
 * GET /api/builder-dashboard-api?foundation_id=xxx
 */

import { createClient } from '@supabase/supabase-js';

export const handler = async (event, context) => {
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'GET') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const supabase = createClient(
            process.env.SUPABASE_URL,
            process.env.SUPABASE_SERVICE_KEY
        );

        const { foundation_id } = event.queryStringParameters || {};

        if (!foundation_id) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'foundation_id required' })
            };
        }

        // Get builder balance
        const { data: balance } = await supabase
            .from('builder_balances')
            .select('*')
            .eq('foundation_id', foundation_id)
            .single();

        // Get creations
        const { data: creations } = await supabase
            .from('builder_creations')
            .select('*')
            .eq('foundation_id', foundation_id)
            .order('created_at', { ascending: false });

        // Get recent revenue events
        const { data: recentRevenue } = await supabase
            .from('revenue_events')
            .select('*')
            .eq('seller_foundation_id', foundation_id)
            .order('created_at', { ascending: false })
            .limit(20);

        // Get downstream earnings
        const { data: downstreamEarnings } = await supabase
            .from('downstream_revenue')
            .select(`
                *,
                builder_creations!derived_creation_id(name, type)
            `)
            .eq('original_builder_id', foundation_id)
            .order('created_at', { ascending: false })
            .limit(20);

        // Calculate stats
        const stats = {
            total_creations: creations?.length || 0,
            marketplace_creations: creations?.filter(c => c.visibility === 'marketplace').length || 0,
            private_creations: creations?.filter(c => c.visibility === 'private').length || 0,
            total_sales: creations?.reduce((sum, c) => sum + (c.total_sales || 0), 0) || 0,
            total_revenue: creations?.reduce((sum, c) => sum + (c.total_revenue_cents || 0), 0) || 0,
            average_rating: creations?.length > 0
                ? creations.reduce((sum, c) => sum + (c.rating_avg || 0), 0) / creations.length
                : 0
        };

        // Calculate time-based metrics
        const now = new Date();
        const thirtyDaysAgo = new Date(now - 30 * 24 * 60 * 60 * 1000);
        const sevenDaysAgo = new Date(now - 7 * 24 * 60 * 60 * 1000);

        const recentEvents = recentRevenue || [];
        const last30Days = recentEvents.filter(e =>
            new Date(e.created_at) > thirtyDaysAgo
        );
        const last7Days = recentEvents.filter(e =>
            new Date(e.created_at) > sevenDaysAgo
        );

        const timeMetrics = {
            revenue_30_days: last30Days.reduce((sum, e) => sum + (e.builder_amount_cents || 0), 0),
            revenue_7_days: last7Days.reduce((sum, e) => sum + (e.builder_amount_cents || 0), 0),
            sales_30_days: last30Days.length,
            sales_7_days: last7Days.length
        };

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                balance: balance || {
                    available_balance_cents: 0,
                    pending_balance_cents: 0,
                    lifetime_earnings_cents: 0,
                    lifetime_downstream_cents: 0,
                    stripe_connect_status: 'not_connected'
                },
                creations: creations || [],
                recent_revenue: recentRevenue || [],
                downstream_earnings: downstreamEarnings || [],
                stats: stats,
                time_metrics: timeMetrics
            })
        };

    } catch (error) {
        console.error('Builder Dashboard Error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Failed to fetch dashboard data',
                details: error.message
            })
        };
    }
};
