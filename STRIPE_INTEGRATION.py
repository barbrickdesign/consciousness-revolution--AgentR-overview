"""STRIPE_INTEGRATION.py - Payment Processing. Tiers: Free/$0, Starter/$19, Pro/$49, Enterprise/$199."""

import os; import stripe
from typing import Optional, Dict, Any

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

PRICE_IDS = {'free': None, 'starter': os.environ.get('STRIPE_PRICE_STARTER', 'price_starter_placeholder'),
             'pro': os.environ.get('STRIPE_PRICE_PRO', 'price_pro_placeholder'), 'enterprise': os.environ.get('STRIPE_PRICE_ENTERPRISE', 'price_enterprise_placeholder')}

TIERS = {'free': {'name': 'Free', 'price': 0, 'features': ['Basic tools', 'Community', 'Pattern intro']},
         'starter': {'name': 'Starter', 'price': 1900, 'features': ['Free+', 'Seven Domains', 'Weekly sessions']},
         'pro': {'name': 'Pro', 'price': 4900, 'features': ['Starter+', 'OVERKORE v13', 'Mentor access', 'Trinity']},
         'enterprise': {'name': 'Enterprise', 'price': 19900, 'features': ['Pro+', 'Custom programs', '1-on-1', 'Full autonomy']}}


class StripeIntegration:
    """Stripe payment processing."""
    def __init__(self):
        if not stripe.api_key: raise ValueError("STRIPE_SECRET_KEY not set")

    def create_checkout_session(self, tier: str, customer_email: str, success_url: str, cancel_url: str,
                                 customer_id: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create checkout session for subscription."""
        if tier == 'free': return {'success': True, 'tier': 'free', 'message': 'Free tier - no payment required'}
        if tier not in PRICE_IDS: raise ValueError(f"Invalid tier: {tier}")
        params = {'mode': 'subscription', 'payment_method_types': ['card'], 'line_items': [{'price': PRICE_IDS[tier], 'quantity': 1}],
                  'success_url': success_url + '?session_id={CHECKOUT_SESSION_ID}', 'cancel_url': cancel_url,
                  'metadata': {'tier': tier, 'platform': 'consciousness_revolution', **(metadata or {})},
                  'subscription_data': {'metadata': {'tier': tier}}, 'allow_promotion_codes': True}
        if customer_id: params['customer'] = customer_id
        else: params['customer_email'] = customer_email
        try:
            s = stripe.checkout.Session.create(**params)
            return {'success': True, 'session_id': s.id, 'url': s.url, 'tier': tier}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e), 'tier': tier}

    def create_one_time_checkout(self, amount: int, description: str, customer_email: str, success_url: str, cancel_url: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create one-time payment checkout."""
        try:
            s = stripe.checkout.Session.create(mode='payment', payment_method_types=['card'],
                line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': description}, 'unit_amount': amount}, 'quantity': 1}],
                customer_email=customer_email, success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}', cancel_url=cancel_url, metadata=metadata or {})
            return {'success': True, 'session_id': s.id, 'url': s.url}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def create_customer(self, email: str, name: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create Stripe customer."""
        try:
            c = stripe.Customer.create(email=email, name=name, metadata={'platform': 'consciousness_revolution', **(metadata or {})})
            return {'success': True, 'customer_id': c.id, 'email': c.email}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve customer."""
        try:
            c = stripe.Customer.retrieve(customer_id)
            return {'success': True, 'customer': {'id': c.id, 'email': c.email, 'name': c.name, 'created': c.created, 'metadata': c.metadata}}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def get_customer_by_email(self, email: str) -> Dict[str, Any]:
        """Find customer by email."""
        try:
            cs = stripe.Customer.list(email=email, limit=1)
            return {'success': True, 'found': True, 'customer_id': cs.data[0].id, 'email': cs.data[0].email} if cs.data else {'success': True, 'found': False}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def update_customer(self, customer_id: str, email: Optional[str] = None, name: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Update customer."""
        try:
            params = {}
            if email: params['email'] = email
            if name: params['name'] = name
            if metadata: params['metadata'] = metadata
            return {'success': True, 'customer_id': stripe.Customer.modify(customer_id, **params).id}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details."""
        try:
            s = stripe.Subscription.retrieve(subscription_id)
            return {'success': True, 'subscription': {'id': s.id, 'status': s.status, 'current_period_start': s.current_period_start,
                    'current_period_end': s.current_period_end, 'cancel_at_period_end': s.cancel_at_period_end, 'tier': s.metadata.get('tier', 'unknown')}}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def get_customer_subscriptions(self, customer_id: str) -> Dict[str, Any]:
        """Get all subscriptions for customer."""
        try:
            subs = stripe.Subscription.list(customer=customer_id)
            return {'success': True, 'subscriptions': [{'id': s.id, 'status': s.status, 'tier': s.metadata.get('tier', 'unknown'), 'current_period_end': s.current_period_end} for s in subs.data]}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def cancel_subscription(self, subscription_id: str, at_period_end: bool = True) -> Dict[str, Any]:
        """Cancel subscription."""
        try:
            s = stripe.Subscription.modify(subscription_id, cancel_at_period_end=True) if at_period_end else stripe.Subscription.delete(subscription_id)
            return {'success': True, 'subscription_id': s.id, 'status': s.status, 'cancel_at_period_end': getattr(s, 'cancel_at_period_end', False)}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def update_subscription_tier(self, subscription_id: str, new_tier: str, prorate: bool = True) -> Dict[str, Any]:
        """Upgrade or downgrade subscription tier."""
        if new_tier not in PRICE_IDS or new_tier == 'free': return {'success': False, 'error': f"Invalid tier: {new_tier}"}
        try:
            s = stripe.Subscription.retrieve(subscription_id)
            u = stripe.Subscription.modify(subscription_id, items=[{'id': s['items']['data'][0].id, 'price': PRICE_IDS[new_tier]}],
                                           proration_behavior='create_prorations' if prorate else 'none', metadata={'tier': new_tier})
            return {'success': True, 'subscription_id': u.id, 'new_tier': new_tier, 'status': u.status}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def create_billing_portal_session(self, customer_id: str, return_url: str) -> Dict[str, Any]:
        """Create billing portal session."""
        try: return {'success': True, 'url': stripe.billing_portal.Session.create(customer=customer_id, return_url=return_url).url}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def handle_webhook_event(self, payload: bytes, sig_header: str, webhook_secret: str) -> Dict[str, Any]:
        """Handle incoming webhook events."""
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
            return {'success': True, 'event_type': event['type'], 'event_data': event['data']['object']}
        except ValueError as e: return {'success': False, 'error': f"Invalid payload: {e}"}
        except stripe.error.SignatureVerificationError as e: return {'success': False, 'error': f"Invalid signature: {e}"}

    def create_products_and_prices(self) -> Dict[str, Any]:
        """Create products and prices in Stripe (run once)."""
        prices = {}
        try:
            for tk, td in TIERS.items():
                if tk == 'free': continue
                prod = stripe.Product.create(name=f"Consciousness Revolution - {td['name']}", description=', '.join(td['features']), metadata={'tier': tk})
                price = stripe.Price.create(product=prod.id, unit_amount=td['price'], currency='usd', recurring={'interval': 'month'}, metadata={'tier': tk})
                prices[tk] = {'product_id': prod.id, 'price_id': price.id}
            return {'success': True, 'prices': prices, 'message': 'Add these price IDs to env vars'}
        except stripe.error.StripeError as e: return {'success': False, 'error': str(e)}

    def get_tier_info(self, tier: str) -> Dict[str, Any]:
        return {'success': True, 'tier': TIERS[tier]} if tier in TIERS else {'success': False, 'error': f"Unknown tier: {tier}"}

    def list_all_tiers(self) -> Dict[str, Any]: return {'success': True, 'tiers': TIERS}


def create_checkout(tier: str, email: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
    """Quick checkout session."""
    return StripeIntegration().create_checkout_session(tier=tier, customer_email=email, success_url=success_url, cancel_url=cancel_url)

def get_or_create_customer(email: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Get or create customer."""
    si = StripeIntegration(); r = si.get_customer_by_email(email)
    if r['success'] and r.get('found'): return {'success': True, 'customer_id': r['customer_id'], 'created': False}
    cr = si.create_customer(email, name)
    return {'success': True, 'customer_id': cr['customer_id'], 'created': True} if cr['success'] else cr


if __name__ == '__main__':
    print("="*50 + "\nSTRIPE INTEGRATION\n" + "="*50)
    if not os.environ.get('STRIPE_SECRET_KEY'):
        print("\n[WARN] STRIPE_SECRET_KEY not set\nTiers:")
        for t, i in TIERS.items(): print(f"  {t}: ${i['price']/100:.0f}/mo")
    else:
        print("\n[OK] Stripe configured -", "TEST" if stripe.api_key.startswith('sk_test') else "LIVE", "mode")
        for t, i in TIERS.items(): print(f"  {i['name']}: ${i['price']/100:.0f}/mo")
