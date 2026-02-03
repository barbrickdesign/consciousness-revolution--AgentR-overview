// Create Checkout - Netlify Function
// Creates Stripe checkout session for course/product purchases

const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;

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
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { priceId, email, customerEmail, successUrl, cancelUrl } = JSON.parse(event.body);
        const finalEmail = customerEmail || email;

        if (!STRIPE_SECRET_KEY) {
            return {
                statusCode: 500,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ error: 'Stripe not configured' })
            };
        }

        // Use default price if not provided
        const finalPriceId = priceId || process.env.STRIPE_PRICE_BUILDER_PRO || 'price_1She0KIBd71iNToy3S6IWn2I';

        // Create Stripe checkout session
        const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${STRIPE_SECRET_KEY}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'mode': 'payment',
                'line_items[0][price]': finalPriceId,
                'line_items[0][quantity]': '1',
                'success_url': successUrl || 'https://conciousnessrevolution.io/success.html?session_id={CHECKOUT_SESSION_ID}',
                'cancel_url': cancelUrl || 'https://conciousnessrevolution.io/',
                ...(finalEmail && { 'customer_email': finalEmail })
            })
        });

        if (!response.ok) {
            const error = await response.text();
            console.error('Stripe error:', error);
            return {
                statusCode: 500,
                headers: { 'Access-Control-Allow-Origin': '*' },
                body: JSON.stringify({ error: 'Failed to create checkout session' })
            };
        }

        const session = await response.json();

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sessionId: session.id,
                url: session.url
            })
        };

    } catch (error) {
        console.error('Checkout error:', error);
        return {
            statusCode: 500,
            headers: { 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ error: 'Failed to create checkout' })
        };
    }
}
