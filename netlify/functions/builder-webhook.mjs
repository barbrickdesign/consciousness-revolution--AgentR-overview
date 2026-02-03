/**
 * BUILDER ECONOMICS WEBHOOK
 * Handles Stripe events for revenue tracking and downstream payments
 *
 * POST /api/builder-webhook
 * Stripe webhook events
 */

import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export const handler = async (event, context) => {
    const headers = {
        'Content-Type': 'application/json'
    };

    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, headers, body: 'Method not allowed' };
    }

    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_SERVICE_KEY
    );

    // Verify webhook signature
    const sig = event.headers['stripe-signature'];
    let stripeEvent;

    try {
        stripeEvent = stripe.webhooks.constructEvent(
            event.body,
            sig,
            process.env.STRIPE_BUILDER_WEBHOOK_SECRET || process.env.STRIPE_WEBHOOK_SECRET
        );
    } catch (err) {
        console.error('Webhook signature verification failed:', err.message);
        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: `Webhook Error: ${err.message}` })
        };
    }

    console.log('Received webhook event:', stripeEvent.type);

    try {
        switch (stripeEvent.type) {
            // Successful checkout
            case 'checkout.session.completed':
                await handleCheckoutCompleted(supabase, stripeEvent.data.object);
                break;

            // Payment received
            case 'payment_intent.succeeded':
                await handlePaymentSucceeded(supabase, stripeEvent.data.object);
                break;

            // Refund issued
            case 'charge.refunded':
                await handleRefund(supabase, stripeEvent.data.object);
                break;

            // Connect account updated
            case 'account.updated':
                await handleAccountUpdated(supabase, stripeEvent.data.object);
                break;

            // Transfer completed (builder received funds)
            case 'transfer.created':
                await handleTransferCreated(supabase, stripeEvent.data.object);
                break;

            default:
                console.log(`Unhandled event type: ${stripeEvent.type}`);
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ received: true })
        };

    } catch (error) {
        console.error('Webhook handler error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: error.message })
        };
    }
};

/**
 * Handle completed checkout session
 */
async function handleCheckoutCompleted(supabase, session) {
    const metadata = session.metadata || {};

    if (!metadata.creation_id) {
        console.log('No creation_id in metadata, skipping');
        return;
    }

    const builderAmount = parseInt(metadata.builder_amount_cents) || 0;
    const networkAmount = parseInt(metadata.network_amount_cents) || 0;
    const grossAmount = session.amount_total;

    // Record revenue event
    const { data: revenueEvent, error: revenueError } = await supabase
        .from('revenue_events')
        .insert({
            creation_id: metadata.creation_id,
            event_type: 'sale',
            gross_amount_cents: grossAmount,
            builder_amount_cents: builderAmount,
            network_amount_cents: networkAmount,
            buyer_foundation_id: metadata.buyer_foundation_id !== 'anonymous'
                ? metadata.buyer_foundation_id
                : null,
            seller_foundation_id: metadata.seller_foundation_id,
            stripe_payment_id: session.payment_intent,
            status: 'completed',
            metadata: {
                session_id: session.id,
                customer_email: session.customer_email,
                creation_name: metadata.creation_name,
                creation_type: metadata.creation_type
            }
        })
        .select()
        .single();

    if (revenueError) {
        console.error('Failed to record revenue event:', revenueError);
        throw revenueError;
    }

    console.log('Revenue event recorded:', revenueEvent.id);

    // Update builder balance
    await supabase.rpc('increment_builder_balance', {
        p_foundation_id: metadata.seller_foundation_id,
        p_amount: builderAmount,
        p_type: 'sale'
    });

    console.log('Builder balance updated:', metadata.seller_foundation_id);

    // Process downstream revenue
    await processDownstreamRevenue(
        supabase,
        metadata.creation_id,
        grossAmount,
        revenueEvent.id
    );
}

/**
 * Process downstream revenue for parent creations
 */
async function processDownstreamRevenue(supabase, creation_id, gross_amount, revenue_event_id) {
    // Get all parent creations in lineage
    const { data: lineage, error: lineageError } = await supabase
        .from('creation_lineage')
        .select(`
            parent_creation_id,
            parent_foundation_id,
            relationship,
            revenue_share_active
        `)
        .eq('child_creation_id', creation_id)
        .eq('revenue_share_active', true);

    if (lineageError || !lineage || lineage.length === 0) {
        console.log('No upstream lineage found for creation:', creation_id);
        return;
    }

    for (const parent of lineage) {
        if (!parent.parent_foundation_id || !parent.parent_creation_id) {
            continue;
        }

        // Get parent's downstream share percentage
        const { data: parentCreation } = await supabase
            .from('builder_creations')
            .select('downstream_share_pct')
            .eq('id', parent.parent_creation_id)
            .single();

        const downstreamPct = parentCreation?.downstream_share_pct || 10;
        const downstreamAmount = Math.floor(gross_amount * downstreamPct / 100);

        if (downstreamAmount <= 0) {
            continue;
        }

        // Record downstream revenue
        const { error: downstreamError } = await supabase
            .from('downstream_revenue')
            .insert({
                original_creation_id: parent.parent_creation_id,
                derived_creation_id: creation_id,
                original_builder_id: parent.parent_foundation_id,
                revenue_event_id: revenue_event_id,
                amount_cents: downstreamAmount,
                depth: 1
            });

        if (downstreamError) {
            console.error('Failed to record downstream revenue:', downstreamError);
            continue;
        }

        // Update original builder's balance
        await supabase.rpc('increment_builder_balance', {
            p_foundation_id: parent.parent_foundation_id,
            p_amount: downstreamAmount,
            p_type: 'downstream'
        });

        console.log(`Downstream payment: ${downstreamAmount} cents to ${parent.parent_foundation_id}`);
    }
}

/**
 * Handle successful payment intent
 */
async function handlePaymentSucceeded(supabase, paymentIntent) {
    // Additional processing if needed
    console.log('Payment succeeded:', paymentIntent.id);
}

/**
 * Handle refund
 */
async function handleRefund(supabase, charge) {
    const paymentIntent = charge.payment_intent;

    // Find original revenue event
    const { data: originalEvent } = await supabase
        .from('revenue_events')
        .select('*')
        .eq('stripe_payment_id', paymentIntent)
        .single();

    if (!originalEvent) {
        console.log('Original revenue event not found for refund');
        return;
    }

    // Record refund event
    await supabase.from('revenue_events').insert({
        creation_id: originalEvent.creation_id,
        event_type: 'refund',
        gross_amount_cents: -charge.amount_refunded,
        builder_amount_cents: -Math.floor(charge.amount_refunded * 0.8),
        network_amount_cents: -Math.floor(charge.amount_refunded * 0.2),
        seller_foundation_id: originalEvent.seller_foundation_id,
        buyer_foundation_id: originalEvent.buyer_foundation_id,
        stripe_refund_id: charge.refunds.data[0]?.id,
        status: 'completed',
        metadata: {
            original_event_id: originalEvent.id
        }
    });

    // Deduct from builder balance
    await supabase.rpc('increment_builder_balance', {
        p_foundation_id: originalEvent.seller_foundation_id,
        p_amount: -Math.floor(charge.amount_refunded * 0.8),
        p_type: 'sale'
    });

    console.log('Refund processed for:', paymentIntent);
}

/**
 * Handle Connect account status update
 */
async function handleAccountUpdated(supabase, account) {
    const foundationId = account.metadata?.foundation_id;

    if (!foundationId) {
        console.log('No foundation_id in account metadata');
        return;
    }

    // Determine account status
    let status = 'pending';
    if (account.charges_enabled && account.payouts_enabled) {
        status = 'active';
    } else if (account.requirements?.disabled_reason) {
        status = 'restricted';
    }

    // Update balance record
    await supabase
        .from('builder_balances')
        .update({
            stripe_connect_status: status,
            updated_at: new Date().toISOString()
        })
        .eq('stripe_connect_id', account.id);

    console.log(`Connect account ${account.id} status: ${status}`);
}

/**
 * Handle transfer created (funds sent to builder)
 */
async function handleTransferCreated(supabase, transfer) {
    const destination = transfer.destination;

    // Find builder by Connect account
    const { data: balance } = await supabase
        .from('builder_balances')
        .select('foundation_id')
        .eq('stripe_connect_id', destination)
        .single();

    if (!balance) {
        console.log('Builder not found for transfer destination:', destination);
        return;
    }

    // Move from pending to available (if tracking pending separately)
    console.log(`Transfer ${transfer.id} created: ${transfer.amount} cents to ${balance.foundation_id}`);
}
