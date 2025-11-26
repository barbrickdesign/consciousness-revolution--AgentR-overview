/**
 * STRIPE WEBHOOK HANDLER
 * Netlify serverless function to handle Stripe webhook events
 * Processes payment confirmations, subscription changes, and failures
 */

import Stripe from 'stripe';

// Initialize Stripe
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

export async function handler(event, context) {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  // Get Stripe signature from headers
  const sig = event.headers['stripe-signature'];

  let stripeEvent;

  try {
    // Verify webhook signature
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      endpointSecret
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return {
      statusCode: 400,
      body: JSON.stringify({ error: `Webhook Error: ${err.message}` })
    };
  }

  // Log event received
  console.log('Webhook event received:', {
    type: stripeEvent.type,
    id: stripeEvent.id,
    created: new Date(stripeEvent.created * 1000).toISOString()
  });

  // Handle different event types
  try {
    switch (stripeEvent.type) {
      case 'checkout.session.completed': {
        const session = stripeEvent.data.object;
        console.log('Payment successful:', {
          sessionId: session.id,
          customerId: session.customer,
          customerEmail: session.customer_details?.email,
          amountTotal: session.amount_total,
          currency: session.currency,
          mode: session.mode
        });

        // TODO: Grant access to product
        // - Add customer to database
        // - Send welcome email
        // - Grant course/subscription access
        await grantProductAccess(session);
        break;
      }

      case 'checkout.session.expired': {
        const session = stripeEvent.data.object;
        console.log('Checkout session expired:', {
          sessionId: session.id,
          customerEmail: session.customer_details?.email
        });
        // Could send reminder email here
        break;
      }

      case 'customer.subscription.created': {
        const subscription = stripeEvent.data.object;
        console.log('Subscription created:', {
          subscriptionId: subscription.id,
          customerId: subscription.customer,
          status: subscription.status,
          priceId: subscription.items.data[0]?.price.id
        });
        break;
      }

      case 'customer.subscription.updated': {
        const subscription = stripeEvent.data.object;
        console.log('Subscription updated:', {
          subscriptionId: subscription.id,
          customerId: subscription.customer,
          status: subscription.status,
          cancelAtPeriodEnd: subscription.cancel_at_period_end
        });

        // Handle subscription changes
        if (subscription.cancel_at_period_end) {
          console.log('Subscription will cancel at period end');
          // Could send retention email
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = stripeEvent.data.object;
        console.log('Subscription cancelled:', {
          subscriptionId: subscription.id,
          customerId: subscription.customer,
          canceledAt: new Date(subscription.canceled_at * 1000).toISOString()
        });

        // TODO: Revoke access
        await revokeSubscriptionAccess(subscription);
        break;
      }

      case 'payment_intent.succeeded': {
        const paymentIntent = stripeEvent.data.object;
        console.log('Payment intent succeeded:', {
          paymentIntentId: paymentIntent.id,
          amount: paymentIntent.amount,
          currency: paymentIntent.currency
        });
        break;
      }

      case 'payment_intent.payment_failed': {
        const paymentIntent = stripeEvent.data.object;
        console.error('Payment failed:', {
          paymentIntentId: paymentIntent.id,
          errorMessage: paymentIntent.last_payment_error?.message,
          customerEmail: paymentIntent.receipt_email
        });

        // TODO: Send payment failure notification
        break;
      }

      case 'invoice.payment_succeeded': {
        const invoice = stripeEvent.data.object;
        console.log('Invoice payment succeeded:', {
          invoiceId: invoice.id,
          customerId: invoice.customer,
          amountPaid: invoice.amount_paid,
          subscriptionId: invoice.subscription
        });
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = stripeEvent.data.object;
        console.error('Invoice payment failed:', {
          invoiceId: invoice.id,
          customerId: invoice.customer,
          attemptCount: invoice.attempt_count
        });

        // TODO: Send payment failure notification to customer
        break;
      }

      default:
        console.log(`Unhandled event type: ${stripeEvent.type}`);
    }

    // Return success response
    return {
      statusCode: 200,
      body: JSON.stringify({ received: true, type: stripeEvent.type })
    };

  } catch (error) {
    console.error('Error processing webhook:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Webhook processing failed',
        details: error.message
      })
    };
  }
}

/**
 * Grant product access after successful payment
 */
async function grantProductAccess(session) {
  const customerEmail = session.customer_details?.email;
  const mode = session.mode;
  const lineItems = session.line_items?.data || [];

  console.log('Granting access:', {
    email: customerEmail,
    mode: mode,
    sessionId: session.id
  });

  // TODO: Implement access grant logic
  // 1. Add customer to database
  // 2. Determine product type from price ID
  // 3. Send appropriate welcome email
  // 4. Grant access to course/subscription

  // For now, just log
  console.log('Access granted to:', customerEmail);

  // Example: Send to external service
  // await fetch('https://yourdomain.com/api/grant-access', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({
  //     email: customerEmail,
  //     sessionId: session.id,
  //     mode: mode
  //   })
  // });
}

/**
 * Revoke subscription access after cancellation
 */
async function revokeSubscriptionAccess(subscription) {
  const customerId = subscription.customer;

  console.log('Revoking access for customer:', customerId);

  // TODO: Implement access revoke logic
  // 1. Find customer in database
  // 2. Revoke access to subscription features
  // 3. Send cancellation confirmation email

  // For now, just log
  console.log('Access revoked for:', customerId);
}
