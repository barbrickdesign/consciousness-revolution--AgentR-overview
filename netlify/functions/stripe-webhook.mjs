// Stripe Webhook Handler
// Captures payment confirmation and triggers welcome email
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function handler(event, context) {
    // Only accept POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    const sig = event.headers['stripe-signature'];
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

    let stripeEvent;

    try {
        // Verify webhook signature
        stripeEvent = stripe.webhooks.constructEvent(
            event.body,
            sig,
            webhookSecret
        );
    } catch (err) {
        console.error('Webhook signature verification failed:', err.message);
        return {
            statusCode: 400,
            body: JSON.stringify({ error: `Webhook Error: ${err.message}` })
        };
    }

    // Handle the event
    switch (stripeEvent.type) {
        case 'checkout.session.completed': {
            const session = stripeEvent.data.object;

            console.log('Payment successful for session:', session.id);
            console.log('Customer email:', session.customer_details?.email);
            console.log('Amount total:', session.amount_total);

            // Extract customer info
            const customerEmail = session.customer_details?.email;
            const customerName = session.customer_details?.name || 'Consciousness Revolutionary';
            const amountPaid = session.amount_total ? (session.amount_total / 100).toFixed(2) : '0.00';
            const currency = session.currency?.toUpperCase() || 'USD';

            if (customerEmail) {
                // Trigger welcome email via our email function
                try {
                    const emailResponse = await fetch(
                        `${process.env.URL || 'https://conciousnessrevolution.io'}/.netlify/functions/send-welcome-email`,
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                email: customerEmail,
                                name: customerName,
                                amount: amountPaid,
                                currency: currency,
                                sessionId: session.id,
                                productName: 'Consciousness Revolution Membership'
                            })
                        }
                    );

                    const emailResult = await emailResponse.json();
                    console.log('Email send result:', emailResult);
                } catch (emailError) {
                    console.error('Failed to send welcome email:', emailError);
                    // Don't fail the webhook - log and continue
                }
            }

            break;
        }

        case 'customer.subscription.created': {
            const subscription = stripeEvent.data.object;
            console.log('Subscription created:', subscription.id);
            break;
        }

        case 'customer.subscription.updated': {
            const subscription = stripeEvent.data.object;
            console.log('Subscription updated:', subscription.id, 'Status:', subscription.status);
            break;
        }

        case 'customer.subscription.deleted': {
            const subscription = stripeEvent.data.object;
            console.log('Subscription cancelled:', subscription.id);
            break;
        }

        case 'invoice.paid': {
            const invoice = stripeEvent.data.object;
            console.log('Invoice paid:', invoice.id);
            break;
        }

        case 'invoice.payment_failed': {
            const invoice = stripeEvent.data.object;
            console.log('Invoice payment failed:', invoice.id);
            break;
        }

        default:
            console.log(`Unhandled event type: ${stripeEvent.type}`);
    }

    // Return success response to Stripe
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ received: true })
    };
}
