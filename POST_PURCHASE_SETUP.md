# Post-Purchase Workflow Setup Guide

## What Was Built

Three components that complete the payment flow:

### 1. stripe-webhook.mjs
**Path:** `netlify/functions/stripe-webhook.mjs`

Receives payment confirmations from Stripe and triggers welcome emails.

Events handled:
- `checkout.session.completed` - Payment successful, triggers email
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Subscription changed
- `customer.subscription.deleted` - Subscription cancelled
- `invoice.paid` - Invoice paid
- `invoice.payment_failed` - Payment failed

### 2. send-welcome-email.mjs
**Path:** `netlify/functions/send-welcome-email.mjs`

Sends welcome email via Gmail SMTP after successful payment.

Includes:
- Payment confirmation
- Links to ARAYA chat
- Quick start guide
- What they get access to

### 3. success.html (Updated)
**Path:** `success.html`

Redesigned to:
- Point to real products (ARAYA, 7 Domains Dashboard)
- Honest about what exists
- Clear call to action
- No fake "login credentials" promises

---

## Setup Required in Stripe Dashboard

### Step 1: Add Environment Variables in Netlify

Go to: Netlify Dashboard > Site settings > Environment variables

Add these:
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
GMAIL_USER=darrick.preble@gmail.com
GMAIL_APP_PASSWORD=gzzvemuxppfnjsup
```

### Step 2: Create Webhook in Stripe

1. Go to: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Endpoint URL: `https://conciousnessrevolution.io/.netlify/functions/stripe-webhook`
4. Select events to listen:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Click "Add endpoint"
6. Copy the "Signing secret" (starts with `whsec_`)
7. Add it to Netlify as `STRIPE_WEBHOOK_SECRET`

### Step 3: Deploy

```bash
cd 100X_DEPLOYMENT
netlify deploy --prod --dir=.
```

---

## Test the Flow

### Local Email Test (Already Verified)
```bash
node test-email.mjs darrickpreble@proton.me
```
Result: SUCCESS - Email received

### Full Flow Test
1. Go to pricing page
2. Click subscribe
3. Use test card: 4242 4242 4242 4242
4. Complete checkout
5. Verify redirect to success.html
6. Check email arrives

### Webhook Test (After Deploy)
1. In Stripe Dashboard > Webhooks > Your endpoint
2. Click "Send test webhook"
3. Select `checkout.session.completed`
4. Click "Send test webhook"
5. Check Netlify function logs

---

## Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `netlify/functions/stripe-webhook.mjs` | CREATED | Handle Stripe webhooks |
| `netlify/functions/send-welcome-email.mjs` | CREATED | Send welcome emails |
| `success.html` | REPLACED | Honest success page |
| `test-email.mjs` | CREATED | Test email locally |
| `.env.example` | UPDATED | Document env vars |
| `package.json` | UPDATED | Added nodemailer |

---

## Email Credentials

Already configured:
- **Gmail:** darrick.preble@gmail.com
- **App Password:** gzzvemuxppfnjsup
- **SMTP Server:** smtp.gmail.com:587

These are hardcoded in the function as fallback, but should be set in Netlify env vars for production.

---

## Troubleshooting

### Email not sending
1. Check Netlify function logs
2. Verify GMAIL_APP_PASSWORD env var
3. Test locally with `node test-email.mjs`

### Webhook not triggering
1. Check Stripe webhook dashboard for failed deliveries
2. Verify STRIPE_WEBHOOK_SECRET matches
3. Check Netlify function logs

### Success page not showing
1. Verify `?session_id=` parameter in URL
2. Check browser console for errors

---

## Next Steps After Deploy

1. [ ] Set Netlify env vars
2. [ ] Create Stripe webhook endpoint
3. [ ] Deploy to production
4. [ ] Run test payment
5. [ ] Verify email arrives
6. [ ] Monitor first real customer

---

Last Updated: December 26, 2025
Built by C1 MECHANIC
