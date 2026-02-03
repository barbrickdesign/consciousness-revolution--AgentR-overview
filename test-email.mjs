// Test script for welcome email
// Run: node test-email.mjs

import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
        user: 'darrick.preble@gmail.com',
        pass: 'gzzvemuxppfnjsup'
    }
});

const testEmail = process.argv[2] || 'darrickpreble@proton.me';

// [AUTO-REMOVED] console.log('Testing email send to:', testEmail);

const mailOptions = {
    from: '"Consciousness Revolution" <darrick.preble@gmail.com>',
    to: testEmail,
    subject: 'TEST - Welcome to the Consciousness Revolution!',
    html: `
        <h1>Test Email</h1>
        <p>This is a test of the post-purchase email system.</p>
        <p>If you receive this, the email workflow is working!</p>
        <p><a href="https://conciousnessrevolution.io/araya-chat.html">Talk to ARAYA</a></p>
    `,
    text: 'Test email - if you see this, email workflow is working!'
};

try {
    const info = await transporter.sendMail(mailOptions);
    console.log('SUCCESS! Email sent:', info.messageId);
    console.log('Response:', info.response);
} catch (error) {
    console.error('FAILED:', error.message);
    console.error('Code:', error.code);
}
