"""
STRIPE_INTEGRATION.py - Core Payment Processing for Consciousness Revolution Platform
C1 Mechanic Build - Complete Stripe Integration

4-Tier Pricing:
- Free: $0
- Starter: $19/mo
- Pro: $49/mo
- Enterprise: $199/mo
"""

import os
import stripe
from typing import Optional, Dict, Any
from datetime import datetime

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Price IDs - Replace with actual Stripe Price IDs after creation
PRICE_IDS = {
    'free': None,  # No payment needed
    'starter': os.environ.get('STRIPE_PRICE_STARTER', 'price_starter_placeholder'),
    'pro': os.environ.get('STRIPE_PRICE_PRO', 'price_pro_placeholder'),
    'enterprise': os.environ.get('STRIPE_PRICE_ENTERPRISE', 'price_enterprise_placeholder')
}

# Tier configuration
TIERS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'features': ['Basic consciousness tools', 'Community access', 'Pattern Theory intro']
    },
    'starter': {
        'name': 'Starter',
        'price': 1900,  # cents
        'features': ['All Free features', 'Seven Domains access', 'Weekly consciousness sessions']
    },
    'pro': {
        'name': 'Pro',
        'price': 4900,  # cents
        'features': ['All Starter features', 'OVERKORE v13 protocol', 'Direct mentor access', 'Trinity system']
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 19900,  # cents
        'features': ['All Pro features', 'Custom consciousness programs', '1-on-1 sessions', 'Full autonomy training']
    }
}


class StripeIntegration:
    """Core Stripe payment processing class"""

    def __init__(self):
        if not stripe.api_key:
            raise ValueError("STRIPE_SECRET_KEY environment variable not set")

    # ==================== CHECKOUT SESSIONS ====================

    def create_checkout_session(
        self,
        tier: str,
        customer_email: str,
        success_url: str,
        cancel_url: str,
        customer_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session for subscription

        Args:
            tier: One of 'starter', 'pro', 'enterprise'
            customer_email: Customer's email address
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel
            customer_id: Existing Stripe customer ID (optional)
            metadata: Additional metadata to store

        Returns:
            Checkout session object with URL
        """
        if tier == 'free':
            return {
                'success': True,
                'tier': 'free',
                'message': 'Free tier - no payment required'
            }

        if tier not in PRICE_IDS:
            raise ValueError(f"Invalid tier: {tier}. Must be one of {list(PRICE_IDS.keys())}")

        price_id = PRICE_IDS[tier]

        session_params = {
            'mode': 'subscription',
            'payment_method_types': ['card'],
            'line_items': [{
                'price': price_id,
                'quantity': 1,
            }],
            'success_url': success_url + '?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': cancel_url,
            'metadata': {
                'tier': tier,
                'platform': 'consciousness_revolution',
                **(metadata or {})
            },
            'subscription_data': {
                'metadata': {
                    'tier': tier
                }
            },
            'allow_promotion_codes': True,
        }

        if customer_id:
            session_params['customer'] = customer_id
        else:
            session_params['customer_email'] = customer_email

        try:
            session = stripe.checkout.Session.create(**session_params)
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url,
                'tier': tier
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'tier': tier
            }

    def create_one_time_checkout(
        self,
        amount: int,
        description: str,
        customer_email: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a one-time payment checkout session

        Args:
            amount: Amount in cents
            description: Product description
            customer_email: Customer email
            success_url: Success redirect URL
            cancel_url: Cancel redirect URL
            metadata: Additional metadata

        Returns:
            Checkout session object
        """
        try:
            session = stripe.checkout.Session.create(
                mode='payment',
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': description,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                customer_email=customer_email,
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata=metadata or {}
            )
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    # ==================== CUSTOMER MANAGEMENT ====================

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    'platform': 'consciousness_revolution',
                    **(metadata or {})
                }
            )
            return {
                'success': True,
                'customer_id': customer.id,
                'email': customer.email
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve customer details"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return {
                'success': True,
                'customer': {
                    'id': customer.id,
                    'email': customer.email,
                    'name': customer.name,
                    'created': customer.created,
                    'metadata': customer.metadata
                }
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_customer_by_email(self, email: str) -> Dict[str, Any]:
        """Find customer by email"""
        try:
            customers = stripe.Customer.list(email=email, limit=1)
            if customers.data:
                customer = customers.data[0]
                return {
                    'success': True,
                    'found': True,
                    'customer_id': customer.id,
                    'email': customer.email
                }
            return {
                'success': True,
                'found': False
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def update_customer(
        self,
        customer_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Update customer details"""
        try:
            update_params = {}
            if email:
                update_params['email'] = email
            if name:
                update_params['name'] = name
            if metadata:
                update_params['metadata'] = metadata

            customer = stripe.Customer.modify(customer_id, **update_params)
            return {
                'success': True,
                'customer_id': customer.id
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    # ==================== SUBSCRIPTION MANAGEMENT ====================

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'success': True,
                'subscription': {
                    'id': subscription.id,
                    'status': subscription.status,
                    'current_period_start': subscription.current_period_start,
                    'current_period_end': subscription.current_period_end,
                    'cancel_at_period_end': subscription.cancel_at_period_end,
                    'tier': subscription.metadata.get('tier', 'unknown')
                }
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_customer_subscriptions(self, customer_id: str) -> Dict[str, Any]:
        """Get all subscriptions for a customer"""
        try:
            subscriptions = stripe.Subscription.list(customer=customer_id)
            return {
                'success': True,
                'subscriptions': [{
                    'id': sub.id,
                    'status': sub.status,
                    'tier': sub.metadata.get('tier', 'unknown'),
                    'current_period_end': sub.current_period_end
                } for sub in subscriptions.data]
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> Dict[str, Any]:
        """
        Cancel a subscription

        Args:
            subscription_id: Stripe subscription ID
            at_period_end: If True, cancel at end of billing period
        """
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)

            return {
                'success': True,
                'subscription_id': subscription.id,
                'status': subscription.status,
                'cancel_at_period_end': getattr(subscription, 'cancel_at_period_end', False)
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def update_subscription_tier(
        self,
        subscription_id: str,
        new_tier: str,
        prorate: bool = True
    ) -> Dict[str, Any]:
        """
        Upgrade or downgrade subscription tier

        Args:
            subscription_id: Current subscription ID
            new_tier: New tier to switch to
            prorate: Whether to prorate the change
        """
        if new_tier not in PRICE_IDS or new_tier == 'free':
            return {
                'success': False,
                'error': f"Invalid tier: {new_tier}"
            }

        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            updated = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': PRICE_IDS[new_tier],
                }],
                proration_behavior='create_prorations' if prorate else 'none',
                metadata={'tier': new_tier}
            )

            return {
                'success': True,
                'subscription_id': updated.id,
                'new_tier': new_tier,
                'status': updated.status
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    # ==================== BILLING PORTAL ====================

    def create_billing_portal_session(
        self,
        customer_id: str,
        return_url: str
    ) -> Dict[str, Any]:
        """
        Create a billing portal session for customer self-service

        Args:
            customer_id: Stripe customer ID
            return_url: URL to return to after portal
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            return {
                'success': True,
                'url': session.url
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    # ==================== WEBHOOK HANDLING ====================

    def handle_webhook_event(
        self,
        payload: bytes,
        sig_header: str,
        webhook_secret: str
    ) -> Dict[str, Any]:
        """
        Handle incoming webhook events

        Args:
            payload: Raw request body
            sig_header: Stripe-Signature header
            webhook_secret: Webhook endpoint secret

        Returns:
            Event data and type
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return {
                'success': True,
                'event_type': event['type'],
                'event_data': event['data']['object']
            }
        except ValueError as e:
            return {
                'success': False,
                'error': f"Invalid payload: {str(e)}"
            }
        except stripe.error.SignatureVerificationError as e:
            return {
                'success': False,
                'error': f"Invalid signature: {str(e)}"
            }

    # ==================== UTILITY FUNCTIONS ====================

    def create_products_and_prices(self) -> Dict[str, Any]:
        """
        Create products and prices in Stripe (run once during setup)

        Returns:
            Created price IDs for each tier
        """
        created_prices = {}

        try:
            for tier_key, tier_data in TIERS.items():
                if tier_key == 'free':
                    continue

                # Create product
                product = stripe.Product.create(
                    name=f"Consciousness Revolution - {tier_data['name']}",
                    description=', '.join(tier_data['features']),
                    metadata={'tier': tier_key}
                )

                # Create price
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=tier_data['price'],
                    currency='usd',
                    recurring={'interval': 'month'},
                    metadata={'tier': tier_key}
                )

                created_prices[tier_key] = {
                    'product_id': product.id,
                    'price_id': price.id
                }

            return {
                'success': True,
                'prices': created_prices,
                'message': 'Add these price IDs to your environment variables'
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_tier_info(self, tier: str) -> Dict[str, Any]:
        """Get tier information"""
        if tier in TIERS:
            return {
                'success': True,
                'tier': TIERS[tier]
            }
        return {
            'success': False,
            'error': f"Unknown tier: {tier}"
        }

    def list_all_tiers(self) -> Dict[str, Any]:
        """Get all available tiers"""
        return {
            'success': True,
            'tiers': TIERS
        }


# ==================== CONVENIENCE FUNCTIONS ====================

def create_checkout(tier: str, email: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
    """Quick function to create checkout session"""
    integration = StripeIntegration()
    return integration.create_checkout_session(
        tier=tier,
        customer_email=email,
        success_url=success_url,
        cancel_url=cancel_url
    )


def get_or_create_customer(email: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Get existing customer or create new one"""
    integration = StripeIntegration()
    result = integration.get_customer_by_email(email)

    if result['success'] and result.get('found'):
        return {
            'success': True,
            'customer_id': result['customer_id'],
            'created': False
        }

    create_result = integration.create_customer(email, name)
    if create_result['success']:
        return {
            'success': True,
            'customer_id': create_result['customer_id'],
            'created': True
        }

    return create_result


# ==================== MAIN - TESTING ====================

if __name__ == '__main__':
    print("=" * 60)
    print("CONSCIOUSNESS REVOLUTION - STRIPE INTEGRATION")
    print("=" * 60)

    # Check configuration
    if not os.environ.get('STRIPE_SECRET_KEY'):
        print("\n[WARNING] STRIPE_SECRET_KEY not set")
        print("Set environment variable to test functionality")
        print("\nAvailable tiers:")
        for tier, info in TIERS.items():
            print(f"  {tier}: ${info['price']/100:.0f}/mo")
    else:
        print("\n[OK] Stripe API key configured")
        integration = StripeIntegration()

        # Test mode check
        if stripe.api_key.startswith('sk_test'):
            print("[OK] Running in TEST mode")
        else:
            print("[LIVE] Running in LIVE mode")

        print("\nTier configuration:")
        for tier, info in TIERS.items():
            print(f"  {info['name']}: ${info['price']/100:.0f}/mo")
