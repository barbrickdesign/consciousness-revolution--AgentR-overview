"""
stripe_webhook_handler.py - Netlify Function for Stripe Webhooks
C1 Mechanic Build - Webhook Processing

Deploy to: netlify/functions/stripe-webhook.py
"""

import os
import json
import stripe
from datetime import datetime

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')


def handler(event, context):
    """
    Netlify serverless function handler for Stripe webhooks

    Args:
        event: Netlify event object
        context: Netlify context object

    Returns:
        Response dict with statusCode and body
    """

    # Only accept POST requests
    if event.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

    # Get payload and signature
    payload = event.get('body', '')
    sig_header = event.get('headers', {}).get('stripe-signature', '')

    if not sig_header:
        # Try lowercase header
        sig_header = event.get('headers', {}).get('Stripe-Signature', '')

    if not WEBHOOK_SECRET:
        print("[ERROR] STRIPE_WEBHOOK_SECRET not configured")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Webhook secret not configured'})
        }

    # Verify signature and construct event
    try:
        stripe_event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"[ERROR] Invalid payload: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid payload'})
        }
    except stripe.error.SignatureVerificationError as e:
        print(f"[ERROR] Invalid signature: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid signature'})
        }

    # Process the event
    event_type = stripe_event['type']
    event_data = stripe_event['data']['object']

    print(f"[WEBHOOK] Received event: {event_type}")

    try:
        result = process_event(event_type, event_data)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'received': True,
                'type': event_type,
                'result': result
            })
        }
    except Exception as e:
        print(f"[ERROR] Processing failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def process_event(event_type: str, event_data: dict) -> dict:
    """
    Process different webhook event types

    Args:
        event_type: Stripe event type string
        event_data: Event data object

    Returns:
        Processing result
    """

    # ==================== CHECKOUT EVENTS ====================

    if event_type == 'checkout.session.completed':
        return handle_checkout_completed(event_data)

    elif event_type == 'checkout.session.expired':
        return handle_checkout_expired(event_data)

    # ==================== SUBSCRIPTION EVENTS ====================

    elif event_type == 'customer.subscription.created':
        return handle_subscription_created(event_data)

    elif event_type == 'customer.subscription.updated':
        return handle_subscription_updated(event_data)

    elif event_type == 'customer.subscription.deleted':
        return handle_subscription_deleted(event_data)

    elif event_type == 'customer.subscription.trial_will_end':
        return handle_trial_ending(event_data)

    # ==================== PAYMENT EVENTS ====================

    elif event_type == 'invoice.paid':
        return handle_invoice_paid(event_data)

    elif event_type == 'invoice.payment_failed':
        return handle_payment_failed(event_data)

    elif event_type == 'invoice.upcoming':
        return handle_invoice_upcoming(event_data)

    # ==================== CUSTOMER EVENTS ====================

    elif event_type == 'customer.created':
        return handle_customer_created(event_data)

    elif event_type == 'customer.updated':
        return handle_customer_updated(event_data)

    else:
        print(f"[INFO] Unhandled event type: {event_type}")
        return {'status': 'ignored', 'event_type': event_type}


# ==================== EVENT HANDLERS ====================

def handle_checkout_completed(session: dict) -> dict:
    """
    Handle successful checkout completion

    This is the main event for new subscriptions.
    Update user's subscription status in your database here.
    """
    customer_id = session.get('customer')
    customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')
    subscription_id = session.get('subscription')
    mode = session.get('mode')
    metadata = session.get('metadata', {})
    tier = metadata.get('tier', 'unknown')

    print(f"[CHECKOUT] Completed - Customer: {customer_email}, Tier: {tier}")

    # =====================================================
    # TODO: Update your database here
    # Example:
    # db.users.update(
    #     {'email': customer_email},
    #     {'$set': {
    #         'stripe_customer_id': customer_id,
    #         'subscription_id': subscription_id,
    #         'tier': tier,
    #         'subscription_status': 'active',
    #         'updated_at': datetime.utcnow()
    #     }}
    # )
    # =====================================================

    # Log the event
    log_event('checkout_completed', {
        'customer_id': customer_id,
        'customer_email': customer_email,
        'subscription_id': subscription_id,
        'tier': tier,
        'mode': mode
    })

    return {
        'status': 'success',
        'action': 'subscription_activated',
        'customer_email': customer_email,
        'tier': tier
    }


def handle_checkout_expired(session: dict) -> dict:
    """Handle expired checkout session"""
    customer_email = session.get('customer_email')

    print(f"[CHECKOUT] Expired - Customer: {customer_email}")

    log_event('checkout_expired', {
        'customer_email': customer_email,
        'session_id': session.get('id')
    })

    return {
        'status': 'noted',
        'action': 'checkout_expired'
    }


def handle_subscription_created(subscription: dict) -> dict:
    """Handle new subscription creation"""
    customer_id = subscription.get('customer')
    status = subscription.get('status')
    tier = subscription.get('metadata', {}).get('tier', 'unknown')

    print(f"[SUBSCRIPTION] Created - Customer: {customer_id}, Status: {status}, Tier: {tier}")

    log_event('subscription_created', {
        'customer_id': customer_id,
        'subscription_id': subscription.get('id'),
        'status': status,
        'tier': tier
    })

    return {
        'status': 'success',
        'action': 'subscription_created',
        'tier': tier
    }


def handle_subscription_updated(subscription: dict) -> dict:
    """
    Handle subscription updates (upgrades, downgrades, cancellations)

    Update user's subscription tier/status in your database.
    """
    customer_id = subscription.get('customer')
    status = subscription.get('status')
    cancel_at_period_end = subscription.get('cancel_at_period_end')
    tier = subscription.get('metadata', {}).get('tier', 'unknown')

    print(f"[SUBSCRIPTION] Updated - Customer: {customer_id}, Status: {status}, Tier: {tier}")

    # =====================================================
    # TODO: Update your database here
    # Example:
    # db.users.update(
    #     {'stripe_customer_id': customer_id},
    #     {'$set': {
    #         'tier': tier,
    #         'subscription_status': status,
    #         'cancel_at_period_end': cancel_at_period_end,
    #         'updated_at': datetime.utcnow()
    #     }}
    # )
    # =====================================================

    log_event('subscription_updated', {
        'customer_id': customer_id,
        'subscription_id': subscription.get('id'),
        'status': status,
        'tier': tier,
        'cancel_at_period_end': cancel_at_period_end
    })

    return {
        'status': 'success',
        'action': 'subscription_updated',
        'tier': tier,
        'subscription_status': status
    }


def handle_subscription_deleted(subscription: dict) -> dict:
    """
    Handle subscription cancellation/deletion

    Downgrade user to free tier in your database.
    """
    customer_id = subscription.get('customer')

    print(f"[SUBSCRIPTION] Deleted - Customer: {customer_id}")

    # =====================================================
    # TODO: Update your database here
    # Example:
    # db.users.update(
    #     {'stripe_customer_id': customer_id},
    #     {'$set': {
    #         'tier': 'free',
    #         'subscription_status': 'cancelled',
    #         'subscription_id': None,
    #         'updated_at': datetime.utcnow()
    #     }}
    # )
    # =====================================================

    log_event('subscription_deleted', {
        'customer_id': customer_id,
        'subscription_id': subscription.get('id')
    })

    return {
        'status': 'success',
        'action': 'subscription_cancelled',
        'new_tier': 'free'
    }


def handle_trial_ending(subscription: dict) -> dict:
    """Handle trial ending soon notification"""
    customer_id = subscription.get('customer')
    trial_end = subscription.get('trial_end')

    print(f"[SUBSCRIPTION] Trial ending - Customer: {customer_id}")

    # TODO: Send reminder email to customer

    log_event('trial_ending', {
        'customer_id': customer_id,
        'trial_end': trial_end
    })

    return {
        'status': 'noted',
        'action': 'trial_ending_notification'
    }


def handle_invoice_paid(invoice: dict) -> dict:
    """Handle successful payment"""
    customer_id = invoice.get('customer')
    amount_paid = invoice.get('amount_paid')
    subscription_id = invoice.get('subscription')

    print(f"[INVOICE] Paid - Customer: {customer_id}, Amount: ${amount_paid/100:.2f}")

    log_event('invoice_paid', {
        'customer_id': customer_id,
        'subscription_id': subscription_id,
        'amount': amount_paid,
        'invoice_id': invoice.get('id')
    })

    return {
        'status': 'success',
        'action': 'payment_received',
        'amount': amount_paid
    }


def handle_payment_failed(invoice: dict) -> dict:
    """
    Handle failed payment

    Notify user about payment failure.
    """
    customer_id = invoice.get('customer')
    customer_email = invoice.get('customer_email')
    amount_due = invoice.get('amount_due')
    attempt_count = invoice.get('attempt_count', 1)

    print(f"[INVOICE] Payment Failed - Customer: {customer_email}, Attempt: {attempt_count}")

    # =====================================================
    # TODO: Send payment failure email
    # Example:
    # send_email(
    #     to=customer_email,
    #     subject='Payment Failed - Action Required',
    #     template='payment_failed',
    #     data={'amount': amount_due/100, 'attempt': attempt_count}
    # )
    # =====================================================

    log_event('payment_failed', {
        'customer_id': customer_id,
        'customer_email': customer_email,
        'amount_due': amount_due,
        'attempt_count': attempt_count,
        'invoice_id': invoice.get('id')
    })

    return {
        'status': 'alert',
        'action': 'payment_failed',
        'customer_email': customer_email,
        'attempt_count': attempt_count
    }


def handle_invoice_upcoming(invoice: dict) -> dict:
    """Handle upcoming invoice notification"""
    customer_id = invoice.get('customer')
    amount_due = invoice.get('amount_due')

    print(f"[INVOICE] Upcoming - Customer: {customer_id}, Amount: ${amount_due/100:.2f}")

    log_event('invoice_upcoming', {
        'customer_id': customer_id,
        'amount_due': amount_due
    })

    return {
        'status': 'noted',
        'action': 'invoice_upcoming'
    }


def handle_customer_created(customer: dict) -> dict:
    """Handle new customer creation"""
    customer_id = customer.get('id')
    email = customer.get('email')

    print(f"[CUSTOMER] Created - {email}")

    log_event('customer_created', {
        'customer_id': customer_id,
        'email': email
    })

    return {
        'status': 'success',
        'action': 'customer_created'
    }


def handle_customer_updated(customer: dict) -> dict:
    """Handle customer update"""
    customer_id = customer.get('id')
    email = customer.get('email')

    print(f"[CUSTOMER] Updated - {email}")

    log_event('customer_updated', {
        'customer_id': customer_id,
        'email': email
    })

    return {
        'status': 'noted',
        'action': 'customer_updated'
    }


# ==================== UTILITY FUNCTIONS ====================

def log_event(event_name: str, data: dict):
    """
    Log webhook event for debugging and audit

    In production, send to your logging service.
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'event': event_name,
        'data': data
    }

    # Print for Netlify function logs
    print(f"[LOG] {json.dumps(log_entry)}")

    # =====================================================
    # TODO: Send to your logging service
    # Example:
    # - Write to database
    # - Send to analytics
    # - Push to monitoring service
    # =====================================================


# ==================== LOCAL TESTING ====================

if __name__ == '__main__':
    """Test the webhook handler locally"""

    print("=" * 60)
    print("STRIPE WEBHOOK HANDLER - LOCAL TEST")
    print("=" * 60)

    # Simulate a checkout completed event
    test_event = {
        'httpMethod': 'POST',
        'headers': {
            'stripe-signature': 'test_signature'
        },
        'body': json.dumps({
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_123',
                    'customer': 'cus_test_123',
                    'customer_email': 'test@example.com',
                    'subscription': 'sub_test_123',
                    'mode': 'subscription',
                    'metadata': {
                        'tier': 'pro'
                    }
                }
            }
        })
    }

    print("\nTest event structure ready")
    print("In production, this handler receives webhooks from Stripe")
    print("\nSupported events:")
    events = [
        'checkout.session.completed',
        'checkout.session.expired',
        'customer.subscription.created',
        'customer.subscription.updated',
        'customer.subscription.deleted',
        'invoice.paid',
        'invoice.payment_failed'
    ]
    for e in events:
        print(f"  - {e}")
