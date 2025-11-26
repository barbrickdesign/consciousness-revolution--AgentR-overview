# STRIPE CONFIGURATION GUIDE
## Consciousness Revolution Payment System

---

## QUICK START

### 1. Get Your API Keys

1. Go to https://dashboard.stripe.com/apikeys
2. Copy your **Secret Key** (starts with `sk_test_` or `sk_live_`)
3. Set environment variable:

```bash
# Windows PowerShell
$env:STRIPE_SECRET_KEY = "sk_test_your_key_here"

# Windows CMD
set STRIPE_SECRET_KEY=sk_test_your_key_here

# Linux/Mac
export STRIPE_SECRET_KEY=sk_test_your_key_here
```

### 2. Create Products & Prices

Run once to create products in Stripe:

```python
from STRIPE_INTEGRATION import StripeIntegration

integration = StripeIntegration()
result = integration.create_products_and_prices()
print(result)
```

This creates:
- Starter: $19/mo
- Pro: $49/mo
- Enterprise: $199/mo

Save the returned price IDs to environment variables:

```bash
STRIPE_PRICE_STARTER=price_xxxxx
STRIPE_PRICE_PRO=price_xxxxx
STRIPE_PRICE_ENTERPRISE=price_xxxxx
```

---

## WEBHOOK SETUP

### 1. Create Webhook Endpoint

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Enter URL: `https://your-site.netlify.app/.netlify/functions/stripe-webhook`
4. Select events to listen for:
   - `checkout.session.completed`
   - `checkout.session.expired`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `invoice.upcoming`
   - `customer.subscription.trial_will_end`

### 2. Get Webhook Secret

1. After creating endpoint, click "Reveal" under Signing secret
2. Copy the secret (starts with `whsec_`)
3. Set environment variable:

```bash
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here
```

### 3. Deploy Webhook Function

Copy `stripe_webhook_handler.py` to your Netlify functions folder:

```
your-project/
  netlify/
    functions/
      stripe-webhook.py  <-- rename and copy here
```

---

## ENVIRONMENT VARIABLES

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `STRIPE_SECRET_KEY` | Stripe API secret key | `sk_test_51...` |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret | `whsec_...` |

### Optional (Price IDs)

| Variable | Description |
|----------|-------------|
| `STRIPE_PRICE_STARTER` | Price ID for $19/mo tier |
| `STRIPE_PRICE_PRO` | Price ID for $49/mo tier |
| `STRIPE_PRICE_ENTERPRISE` | Price ID for $199/mo tier |

### Netlify Configuration

Add to Netlify dashboard (Site settings > Environment variables):

1. `STRIPE_SECRET_KEY`
2. `STRIPE_WEBHOOK_SECRET`
3. `STRIPE_PRICE_STARTER`
4. `STRIPE_PRICE_PRO`
5. `STRIPE_PRICE_ENTERPRISE`

---

## TEST MODE VS LIVE MODE

### Test Mode

- API keys start with `sk_test_`
- Use test card: `4242 4242 4242 4242`
- Any future expiry date
- Any 3-digit CVC
- Payments are not real

### Live Mode

- API keys start with `sk_live_`
- Real payments processed
- Real money transferred

### Switching Modes

1. Toggle "Test mode" switch in Stripe dashboard
2. Get new API keys for that mode
3. Create new webhook endpoint for that mode
4. Update environment variables

**IMPORTANT:** Always test thoroughly in test mode before going live.

---

## USAGE EXAMPLES

### Create Checkout Session

```python
from STRIPE_INTEGRATION import StripeIntegration

stripe_api = StripeIntegration()

# Create checkout for Pro tier
result = stripe_api.create_checkout_session(
    tier='pro',
    customer_email='user@example.com',
    success_url='https://yoursite.com/success',
    cancel_url='https://yoursite.com/pricing'
)

if result['success']:
    # Redirect user to Stripe checkout
    checkout_url = result['url']
```

### Check Customer Subscription

```python
# Get customer subscriptions
result = stripe_api.get_customer_subscriptions('cus_xxx')

if result['success']:
    for sub in result['subscriptions']:
        print(f"Tier: {sub['tier']}, Status: {sub['status']}")
```

### Cancel Subscription

```python
# Cancel at end of billing period
result = stripe_api.cancel_subscription(
    subscription_id='sub_xxx',
    at_period_end=True
)
```

### Create Billing Portal

```python
# Let customer manage their subscription
result = stripe_api.create_billing_portal_session(
    customer_id='cus_xxx',
    return_url='https://yoursite.com/account'
)

if result['success']:
    portal_url = result['url']
```

---

## TIER CONFIGURATION

| Tier | Price | Features |
|------|-------|----------|
| Free | $0/mo | Basic consciousness tools, Community access, Pattern Theory intro |
| Starter | $19/mo | All Free + Seven Domains access, Weekly sessions |
| Pro | $49/mo | All Starter + OVERKORE v13, Direct mentor access, Trinity system |
| Enterprise | $199/mo | All Pro + Custom programs, 1-on-1 sessions, Full autonomy training |

---

## TROUBLESHOOTING

### "Invalid API Key"

- Verify key is set: `echo $STRIPE_SECRET_KEY`
- Check key starts with `sk_test_` or `sk_live_`
- Ensure no extra spaces or quotes

### "Webhook Signature Verification Failed"

- Verify webhook secret is correct
- Ensure you're using raw request body (not parsed JSON)
- Check endpoint URL matches exactly

### "Price Not Found"

- Run `create_products_and_prices()` first
- Update environment variables with returned price IDs
- Verify you're in correct mode (test vs live)

### Webhook Not Receiving Events

1. Check Netlify function logs
2. Verify webhook endpoint is active in Stripe dashboard
3. Test with Stripe CLI: `stripe listen --forward-to localhost:8888/.netlify/functions/stripe-webhook`

---

## LOCAL TESTING

### Using Stripe CLI

1. Install: https://stripe.com/docs/stripe-cli
2. Login: `stripe login`
3. Forward webhooks:

```bash
stripe listen --forward-to localhost:8888/.netlify/functions/stripe-webhook
```

4. Trigger test events:

```bash
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
```

---

## SECURITY CHECKLIST

- [ ] Never commit API keys to git
- [ ] Use environment variables for all secrets
- [ ] Verify webhook signatures
- [ ] Use HTTPS for all endpoints
- [ ] Test thoroughly before live mode
- [ ] Monitor webhook failures in Stripe dashboard
- [ ] Set up alerts for failed payments

---

## SUPPORT

- Stripe Docs: https://stripe.com/docs
- API Reference: https://stripe.com/docs/api
- Webhook Guide: https://stripe.com/docs/webhooks

---

*Built by C1 Mechanic - Consciousness Revolution Platform*
