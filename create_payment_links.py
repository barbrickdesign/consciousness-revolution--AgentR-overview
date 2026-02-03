"""
STRIPE PAYMENT LINKS GENERATOR
Created: 2024-12-24

Automatically creates payment links for all 3 products.
Saves links to a JSON file for easy access.
"""

import stripe
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.stripe')

# Stripe API key from environment (NEVER hardcode!)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
if not stripe.api_key:
    raise ValueError("STRIPE_SECRET_KEY not found in environment. Check .env.stripe")

PRODUCTS = {
    'founding_member': {
        'price_id': 'price_1Si4sWIBd71iNToyQiR5WRY5',
        'name': 'Consciousness Founding Member - $47/month',
        'description': 'Lifetime founding member rate. Full platform access.'
    },
    'pattern_tools_pro': {
        'price_id': 'price_1Si4szIBd71iNToyZghCXYaE',
        'name': 'Pattern Tools Pro - $99/month',
        'description': 'All consciousness tools + priority support.'
    },
    'emergency_consulting': {
        'price_id': 'price_1Si4tKIBd71iNToyUtO6McaO',
        'name': 'Emergency Consulting - $500',
        'description': '1-hour emergency consciousness consultation.'
    }
}

def create_payment_link(price_id, name, description):
    """Create a Stripe payment link."""
    try:
        payment_link = stripe.PaymentLink.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            after_completion={
                'type': 'redirect',
                'redirect': {
                    'url': 'https://conciousnessrevolution.io/success.html'
                }
            },
            allow_promotion_codes=True,
            billing_address_collection='required',
        )

        return payment_link.url

    except stripe.error.StripeError as e:
        print(f"Error creating payment link for {name}: {str(e)}")
        return None

def main():
    """Create payment links for all products."""
    print("=" * 80)
    print("CREATING STRIPE PAYMENT LINKS")
    print("=" * 80)

    results = {}

    for key, product in PRODUCTS.items():
        print(f"\nCreating payment link for: {product['name']}")
        print(f"Price ID: {product['price_id']}")

        url = create_payment_link(
            product['price_id'],
            product['name'],
            product['description']
        )

        if url:
            print(f"✓ Success! URL: {url}")
            results[key] = {
                'name': product['name'],
                'price_id': product['price_id'],
                'payment_url': url,
                'created': datetime.now().isoformat()
            }
        else:
            print(f"✗ Failed to create payment link")
            results[key] = {
                'name': product['name'],
                'price_id': product['price_id'],
                'payment_url': 'CREATION_FAILED',
                'created': datetime.now().isoformat()
            }

    # Save to JSON file
    output_file = 'PAYMENT_LINKS.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Payment links saved to: {output_file}")
    print("=" * 80)

    # Display summary
    print("\n📋 PAYMENT LINKS SUMMARY:\n")
    for key, data in results.items():
        print(f"🔗 {data['name']}")
        print(f"   {data['payment_url']}\n")

    # Generate HTML buttons
    print("\n" + "=" * 80)
    print("HTML BUTTONS (Copy to your website):")
    print("=" * 80 + "\n")

    for key, data in results.items():
        if data['payment_url'] != 'CREATION_FAILED':
            print(f"""<!-- {data['name']} -->
<a href="{data['payment_url']}" class="btn btn-primary">
    {data['name'].split(' - ')[0]}
</a>
""")

    print("\n✓ REVENUE INFRASTRUCTURE READY!")
    print("Copy the URLs above and add them to your website.\n")

if __name__ == '__main__':
    main()
