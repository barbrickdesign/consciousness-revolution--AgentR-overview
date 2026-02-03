// Auth Signup Function
// Creates new user via Supabase Auth with optional foundation record
// Created: 2026-01-10

import { createClient } from '@supabase/supabase-js';

function getSupabaseAdmin() {
    const url = process.env.SUPABASE_URL;
    const key = process.env.SUPABASE_SERVICE_ROLE_SECRET || process.env.SUPABASE_SERVICE_KEY;

    if (!url || !key) {
        throw new Error('Supabase configuration missing');
    }
    return createClient(url, key, {
        auth: { autoRefreshToken: false, persistSession: false }
    });
}

export async function handler(event, context) {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 204, headers };
    }

    // Only accept POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { email, password, full_name } = JSON.parse(event.body || '{}');

        // Validate required fields
        if (!email || !password) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Email and password required' })
            };
        }

        // Validate password strength
        if (password.length < 8) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Password must be at least 8 characters' })
            };
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Invalid email format' })
            };
        }

        const supabase = getSupabaseAdmin();

        // Create user via Supabase Auth
        const { data: authData, error: authError } = await supabase.auth.admin.createUser({
            email: email.toLowerCase().trim(),
            password,
            email_confirm: true, // Auto-confirm for beta
            user_metadata: {
                full_name: full_name || '',
                signup_source: 'beta_form',
                signup_date: new Date().toISOString()
            }
        });

        if (authError) {
            console.error('Auth error:', authError.message);

            // Handle specific errors
            if (authError.message.includes('already registered')) {
                return {
                    statusCode: 409,
                    headers,
                    body: JSON.stringify({ error: 'Email already registered. Please login instead.' })
                };
            }

            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: authError.message || 'Signup failed' })
            };
        }

        // Create foundation record for the user
        if (authData?.user) {
            const { error: foundationError } = await supabase
                .from('user_foundations')
                .insert({
                    user_id: authData.user.id,
                    email: email.toLowerCase().trim(),
                    full_name: full_name || '',
                    consciousness_level: 0.5,
                    manipulation_immunity: 0.3,
                    truth_recognition: 0.3,
                    pattern_recognition: 0.3,
                    account_tier: 'beta',
                    account_status: 'active'
                });

            if (foundationError) {
                console.warn('Foundation creation warning:', foundationError.message);
                // Non-blocking - foundation can be created later
            }

            // Create network status record
            const { error: networkError } = await supabase
                .from('builder_network_status')
                .insert({
                    foundation_id: authData.user.id,
                    contribution_score: 10, // Welcome bonus
                    contribution_tier: 'SEEDLING'
                });

            if (networkError) {
                console.warn('Network status creation warning:', networkError.message);
            }
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                message: 'Account created successfully!',
                user: {
                    id: authData.user.id,
                    email: authData.user.email
                }
            })
        };

    } catch (error) {
        console.error('Signup error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Server error. Please try again.' })
        };
    }
}
