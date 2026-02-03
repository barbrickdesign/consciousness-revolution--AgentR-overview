/**
 * CREATE STRIPE CONNECT ACCOUNT
 * Allows builders to receive payouts for marketplace sales
 *
 * POST /api/create-connect-account
 * Body: { foundation_id, email, country }
 */

import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export const handler = async (event, context) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'POST') {
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

        const { foundation_id, email, country } = JSON.parse(event.body);

        if (!foundation_id || !email) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'foundation_id and email required' })
            };
        }

        // Check if already has Connect account
        const { data: existing } = await supabase
            .from('builder_balances')
            .select('stripe_connect_id, stripe_connect_status')
            .eq('foundation_id', foundation_id)
            .single();

        if (existing?.stripe_connect_id && existing?.stripe_connect_status === 'active') {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({
                    error: 'Connect account already exists',
                    account_id: existing.stripe_connect_id
                })
            };
        }

        // Create Stripe Connect Express account
        const account = await stripe.accounts.create({
            type: 'express',
            email: email,
            country: country || 'US',
            capabilities: {
                card_payments: { requested: true },
                transfers: { requested: true }
            },
            business_type: 'individual',
            metadata: {
                foundation_id: foundation_id,
                platform: 'consciousness_revolution'
            },
            settings: {
                payouts: {
                    schedule: {
                        interval: 'weekly',
                        weekly_anchor: 'monday'
                    }
                }
            }
        });

        // Save to Supabase
        await supabase
            .from('builder_balances')
            .upsert({
                foundation_id: foundation_id,
                stripe_connect_id: account.id,
                stripe_connect_status: 'pending',
                updated_at: new Date().toISOString()
            }, {
                onConflict: 'foundation_id'
            });

        // Generate onboarding link
        const accountLink = await stripe.accountLinks.create({
            account: account.id,
            refresh_url: `${process.env.SITE_URL || 'https://consciousnessrevolution.io'}/builder/dashboard?refresh=true`,
            return_url: `${process.env.SITE_URL || 'https://consciousnessrevolution.io'}/builder/dashboard?connected=true`,
            type: 'account_onboarding'
        });

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                account_id: account.id,
                onboarding_url: accountLink.url,
                message: 'Complete Stripe onboarding to receive payouts'
            })
        };

    } catch (error) {
        console.error('Create Connect Error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Failed to create Connect account',
                details: error.message
            })
        };
    }
};
