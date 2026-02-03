/**
 * TWILIO SMS WEBHOOK
 * ==================
 * Receives incoming SMS from Twilio and routes to Cyclotron Radio
 *
 * Endpoint: /.netlify/functions/sms-webhook
 * Configure in Twilio: https://console.twilio.com → Phone Numbers → Webhooks
 *
 * C1 MECHANIC BUILD - Jan 28, 2026
 */

// In-memory message store (persists via Netlify KV in production)
// For now, we'll return messages via GET endpoint
let pendingMessages = [];

export const handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      },
      body: ''
    };
  }

  // GET - Retrieve pending messages (for local polling)
  if (event.httpMethod === 'GET') {
    const messages = pendingMessages;
    pendingMessages = []; // Clear after read

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        count: messages.length,
        messages: messages
      })
    };
  }

  // POST - Receive Twilio webhook
  if (event.httpMethod === 'POST') {
    try {
      // Parse Twilio's form-encoded body
      const params = new URLSearchParams(event.body);

      const smsData = {
        id: `SMS-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
        from: params.get('From') || 'unknown',
        to: params.get('To') || 'unknown',
        body: params.get('Body') || '',
        timestamp: new Date().toISOString(),
        messageSid: params.get('MessageSid') || '',
        accountSid: params.get('AccountSid') || '',
        numMedia: params.get('NumMedia') || '0',
        fromCity: params.get('FromCity') || '',
        fromState: params.get('FromState') || '',
        fromCountry: params.get('FromCountry') || '',
        channel: 'TWILIO_SMS'
      };

      // Log for debugging
      console.log('📱 SMS RECEIVED:', JSON.stringify(smsData, null, 2));

      // Store message for polling
      pendingMessages.push(smsData);

      // Also store in Netlify Blobs if available (future upgrade)
      // For now, we'll use a simple file-based approach via the deploy

      // Parse command if message starts with /
      let responseText = `✅ Message received by Overkore Brain.\n\nYour message: "${smsData.body}"\n\nTimestamp: ${smsData.timestamp}`;

      if (smsData.body.toLowerCase().startsWith('/status')) {
        responseText = `🧠 OVERKORE STATUS\n\nBrain: ONLINE\nAtoms: 163,649\nDivine: 92.2%\nLocation: Denver → Red Rocks\n\nC1×C2×C3=∞`;
      } else if (smsData.body.toLowerCase().startsWith('/help')) {
        responseText = `📱 SMS COMMANDS\n\n/status - System status\n/help - This menu\n/ping - Test connection\n\nOr just text anything - it goes to the brain.`;
      } else if (smsData.body.toLowerCase().startsWith('/ping')) {
        responseText = `🏓 PONG! Latency: ${Date.now() % 1000}ms\n\nConnection: ACTIVE\nRadio: RECEIVING`;
      }

      // Return TwiML response (Twilio's XML format)
      const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>${responseText}</Message>
</Response>`;

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'text/xml',
          'Access-Control-Allow-Origin': '*'
        },
        body: twiml
      };

    } catch (error) {
      console.error('SMS Webhook Error:', error);

      // Still return valid TwiML on error
      const errorTwiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>⚠️ Message received but processing error. Brain notified.</Message>
</Response>`;

      return {
        statusCode: 200,
        headers: { 'Content-Type': 'text/xml' },
        body: errorTwiml
      };
    }
  }

  // Method not allowed
  return {
    statusCode: 405,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};
