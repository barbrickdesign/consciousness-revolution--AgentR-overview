/**
 * CREATE CHECKOUT SESSION
 * Netlify serverless function to create Stripe checkout sessions
 * Supports both one-time payments and subscriptions
 */

import Stripe from 'stripe';

// Initialize Stripe with secret key from environment
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function handler(event, context) {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

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

  try {
    // Parse request body
    const { priceId, successUrl, cancelUrl, customerEmail, metadata } = JSON.parse(event.body);

    // Validate required parameters
    if (!priceId || !successUrl || !cancelUrl) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          error: 'Missing required parameters: priceId, successUrl, cancelUrl'
        })
      };
    }

    // Retrieve price to determine if it's a subscription
    const price = await stripe.prices.retrieve(priceId);
    const isSubscription = price.type === 'recurring';

    // Build checkout session parameters
    const sessionParams = {
      mode: isSubscription ? 'subscription' : 'payment',
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      success_url: successUrl,
      cancel_url: cancelUrl,
      automatic_tax: { enabled: false }, // Enable if you want automatic tax calculation
    };

    // Add customer email if provided
    if (customerEmail) {
      sessionParams.customer_email = customerEmail;
    }

    // Add metadata if provided
    if (metadata) {
      sessionParams.metadata = metadata;
    }

    // Add subscription-specific parameters
    if (isSubscription) {
      sessionParams.subscription_data = {
        metadata: metadata || {}
      };
    }

    // Create checkout session
    const session = await stripe.checkout.sessions.create(sessionParams);

    // Log successful session creation
    console.log('Checkout session created:', {
      sessionId: session.id,
      priceId: priceId,
      mode: sessionParams.mode,
      customerEmail: customerEmail || 'not provided'
    });

    // Return session URL
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        url: session.url,
        sessionId: session.id
      })
    };

  } catch (error) {
    console.error('Checkout session error:', error);

    // Return error response
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        error: error.message || 'Failed to create checkout session',
        details: process.env.NODE_ENV === 'development' ? error.stack : undefined
      })
    };
  }
}
