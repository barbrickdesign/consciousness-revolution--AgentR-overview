// Stripe Checkout Session Creator
// Netlify Serverless Function
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function handler(event, context) {
    // Handle CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { price_id, success_url, cancel_url } = JSON.parse(event.body);

        if (!price_id) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Missing price_id' })
            };
        }

        // Create Stripe checkout session
        const session = await stripe.checkout.sessions.create({
            mode: 'subscription',
            payment_method_types: ['card'],
            line_items: [
                {
                    price: price_id,
                    quantity: 1
                }
            ],
            success_url: success_url || 'https://conciousnessrevolution.io/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url: cancel_url || 'https://conciousnessrevolution.io/pricing-live.html'
        });

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sessionId: session.id, url: session.url })
        };

    } catch (error) {
        console.error('Stripe error:', error);

        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                error: error.message || 'Failed to create checkout session'
            })
        };
    }
}
