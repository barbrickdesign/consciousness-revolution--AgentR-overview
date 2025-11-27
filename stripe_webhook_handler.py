"""stripe_webhook_handler.py - Netlify Function for Stripe Webhooks."""

import os; import json; import stripe
from datetime import datetime

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

def handler(event, context):
    """Netlify serverless function handler for Stripe webhooks."""
    if event.get('httpMethod') != 'POST': return {'statusCode': 405, 'body': json.dumps({'error': 'Method not allowed'})}
    payload, sig = event.get('body', ''), event.get('headers', {}).get('stripe-signature') or event.get('headers', {}).get('Stripe-Signature', '')
    if not WEBHOOK_SECRET: return {'statusCode': 500, 'body': json.dumps({'error': 'Webhook secret not configured'})}
    try: stripe_event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
    except ValueError: return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid payload'})}
    except stripe.error.SignatureVerificationError: return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid signature'})}
    event_type, event_data = stripe_event['type'], stripe_event['data']['object']
    print(f"[WEBHOOK] {event_type}")
    try:
        result = process_event(event_type, event_data)
        return {'statusCode': 200, 'body': json.dumps({'received': True, 'type': event_type, 'result': result})}
    except Exception as e: return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def process_event(event_type: str, data: dict) -> dict:
    """Route events to handlers."""
    handlers = {
        'checkout.session.completed': handle_checkout_completed,
        'checkout.session.expired': lambda d: log_and_return('checkout_expired', d, 'noted'),
        'customer.subscription.created': handle_subscription_created,
        'customer.subscription.updated': handle_subscription_updated,
        'customer.subscription.deleted': handle_subscription_deleted,
        'customer.subscription.trial_will_end': lambda d: log_and_return('trial_ending', d, 'noted'),
        'invoice.paid': handle_invoice_paid,
        'invoice.payment_failed': handle_payment_failed,
        'invoice.upcoming': lambda d: log_and_return('invoice_upcoming', d, 'noted'),
        'customer.created': lambda d: log_and_return('customer_created', d, 'success'),
        'customer.updated': lambda d: log_and_return('customer_updated', d, 'noted'),
    }
    return handlers.get(event_type, lambda d: {'status': 'ignored', 'event_type': event_type})(data)

def handle_checkout_completed(session: dict) -> dict:
    cid, email = session.get('customer'), session.get('customer_email') or session.get('customer_details', {}).get('email')
    sub_id, tier = session.get('subscription'), session.get('metadata', {}).get('tier', 'unknown')
    print(f"[CHECKOUT] {email}, Tier: {tier}")
    log_event('checkout_completed', {'customer_id': cid, 'email': email, 'subscription_id': sub_id, 'tier': tier})
    # TODO: Update database - set user tier=tier, subscription_status='active'
    return {'status': 'success', 'action': 'subscription_activated', 'email': email, 'tier': tier}

def handle_subscription_created(sub: dict) -> dict:
    cid, status, tier = sub.get('customer'), sub.get('status'), sub.get('metadata', {}).get('tier', 'unknown')
    print(f"[SUBSCRIPTION] Created - {cid}, {status}, {tier}")
    log_event('subscription_created', {'customer_id': cid, 'subscription_id': sub.get('id'), 'status': status, 'tier': tier})
    return {'status': 'success', 'action': 'subscription_created', 'tier': tier}

def handle_subscription_updated(sub: dict) -> dict:
    cid, status, tier = sub.get('customer'), sub.get('status'), sub.get('metadata', {}).get('tier', 'unknown')
    cancel_end = sub.get('cancel_at_period_end')
    print(f"[SUBSCRIPTION] Updated - {cid}, {status}, {tier}")
    log_event('subscription_updated', {'customer_id': cid, 'subscription_id': sub.get('id'), 'status': status, 'tier': tier, 'cancel_at_period_end': cancel_end})
    # TODO: Update database - set tier, status, cancel_at_period_end
    return {'status': 'success', 'action': 'subscription_updated', 'tier': tier, 'subscription_status': status}

def handle_subscription_deleted(sub: dict) -> dict:
    cid = sub.get('customer')
    print(f"[SUBSCRIPTION] Deleted - {cid}")
    log_event('subscription_deleted', {'customer_id': cid, 'subscription_id': sub.get('id')})
    # TODO: Downgrade user to free tier
    return {'status': 'success', 'action': 'subscription_cancelled', 'new_tier': 'free'}

def handle_invoice_paid(inv: dict) -> dict:
    cid, amount = inv.get('customer'), inv.get('amount_paid')
    print(f"[INVOICE] Paid - {cid}, ${amount/100:.2f}")
    log_event('invoice_paid', {'customer_id': cid, 'amount': amount, 'invoice_id': inv.get('id')})
    return {'status': 'success', 'action': 'payment_received', 'amount': amount}

def handle_payment_failed(inv: dict) -> dict:
    cid, email, amount, attempt = inv.get('customer'), inv.get('customer_email'), inv.get('amount_due'), inv.get('attempt_count', 1)
    print(f"[INVOICE] Payment Failed - {email}, Attempt: {attempt}")
    log_event('payment_failed', {'customer_id': cid, 'email': email, 'amount_due': amount, 'attempt_count': attempt})
    # TODO: Send payment failure email
    return {'status': 'alert', 'action': 'payment_failed', 'email': email, 'attempt_count': attempt}

def log_and_return(event_name: str, data: dict, status: str) -> dict:
    log_event(event_name, {'id': data.get('id'), 'customer': data.get('customer')})
    return {'status': status, 'action': event_name}

def log_event(event_name: str, data: dict):
    print(f"[LOG] {json.dumps({'timestamp': datetime.utcnow().isoformat(), 'event': event_name, 'data': data})}")

if __name__ == '__main__':
    print("=" * 60 + "\nSTRIPE WEBHOOK HANDLER\n" + "=" * 60)
    print("\nSupported events: checkout.session.completed/expired, customer.subscription.created/updated/deleted, invoice.paid/payment_failed")
