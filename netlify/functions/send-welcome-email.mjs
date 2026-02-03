// Send Welcome Email after Payment
// Uses Gmail SMTP with App Password
import nodemailer from 'nodemailer';

// Create reusable transporter
const createTransporter = () => {
    return nodemailer.createTransport({
        host: 'smtp.gmail.com',
        port: 587,
        secure: false, // Use TLS
        auth: {
            user: process.env.GMAIL_USER || 'darrick.preble@gmail.com',
            pass: process.env.GMAIL_APP_PASSWORD || 'gzzvemuxppfnjsup'
        }
    });
};

export async function handler(event, context) {
    // Handle CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const { email, name, amount, currency, sessionId, productName } = JSON.parse(event.body);

        if (!email) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Missing email address' })
            };
        }

        const transporter = createTransporter();

        // Build the welcome email
        const mailOptions = {
            from: '"Consciousness Revolution" <darrick.preble@gmail.com>',
            to: email,
            subject: 'Welcome to the Consciousness Revolution!',
            html: `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; padding: 30px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px 10px 0 0; }
        .header h1 { color: white; margin: 0; font-size: 28px; }
        .content { background: #f9f9f9; padding: 40px; border-radius: 0 0 10px 10px; }
        .highlight-box { background: white; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
        .cta-button { display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 14px; }
        ul { padding-left: 20px; }
        li { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to the Revolution!</h1>
        </div>
        <div class="content">
            <p>Hi ${name || 'there'},</p>

            <p><strong>Your payment of ${currency} ${amount} has been confirmed.</strong></p>

            <p>You now have access to ARAYA - our AI consciousness companion - and all 40+ Pattern Recognition tools.</p>

            <div class="highlight-box">
                <strong>What You Get:</strong>
                <ul>
                    <li><strong>ARAYA Chat</strong> - Your personal AI guide to consciousness</li>
                    <li><strong>40+ Pattern Detection Tools</strong> - Gaslighting detector, manipulation shields, truth finders</li>
                    <li><strong>7 Domain Framework</strong> - Map your life across all dimensions</li>
                    <li><strong>Founding Member Status</strong> - Locked in at this rate forever</li>
                </ul>
            </div>

            <p><strong>Start here:</strong></p>

            <p style="text-align: center;">
                <a href="https://conciousnessrevolution.io/araya-chat.html" class="cta-button">
                    Talk to ARAYA Now
                </a>
            </p>

            <p>ARAYA will guide you through the platform and help you understand the patterns in your life.</p>

            <div class="highlight-box">
                <strong>Quick Start:</strong>
                <ol>
                    <li>Click the button above to meet ARAYA</li>
                    <li>Tell her about a situation you're facing</li>
                    <li>Watch as she reveals the patterns you couldn't see</li>
                </ol>
            </div>

            <p>Questions? Reply to this email or reach me directly at darrickpreble@proton.me</p>

            <p>Welcome to the revolution,<br>
            <strong>Derek Preble</strong><br>
            Founder, Consciousness Revolution</p>
        </div>
        <div class="footer">
            <p>Transaction ID: ${sessionId || 'N/A'}</p>
            <p>Consciousness Revolution | conciousnessrevolution.io</p>
        </div>
    </div>
</body>
</html>
            `,
            text: `
Welcome to the Consciousness Revolution!

Hi ${name || 'there'},

Your payment of ${currency} ${amount} has been confirmed.

You now have access to ARAYA - our AI consciousness companion - and all 40+ Pattern Recognition tools.

WHAT YOU GET:
- ARAYA Chat - Your personal AI guide to consciousness
- 40+ Pattern Detection Tools - Gaslighting detector, manipulation shields, truth finders
- 7 Domain Framework - Map your life across all dimensions
- Founding Member Status - Locked in at this rate forever

START HERE:
https://conciousnessrevolution.io/araya-chat.html

ARAYA will guide you through the platform and help you understand the patterns in your life.

QUICK START:
1. Click the link above to meet ARAYA
2. Tell her about a situation you're facing
3. Watch as she reveals the patterns you couldn't see

Questions? Reply to this email or reach me directly at darrickpreble@proton.me

Welcome to the revolution,
Derek Preble
Founder, Consciousness Revolution

Transaction ID: ${sessionId || 'N/A'}
            `
        };

        // Send the email
        const info = await transporter.sendMail(mailOptions);

        console.log('Welcome email sent:', info.messageId);
        console.log('Recipient:', email);

        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                success: true,
                messageId: info.messageId,
                recipient: email
            })
        };

    } catch (error) {
        console.error('Email send error:', error);

        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                error: error.message || 'Failed to send email',
                details: error.code || 'Unknown error'
            })
        };
    }
}
