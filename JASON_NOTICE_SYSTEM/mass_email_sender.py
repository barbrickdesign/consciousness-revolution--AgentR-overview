"""
MASS EMAIL SENDER - Jason Notice Distribution System
=====================================================
Sends notice emails to Catholic dioceses with rate limiting and tracking.
Created: December 26, 2025
Target Launch: December 27, 2025 (Jason's Birthday)

Gmail Limits:
- Personal account: ~500/day
- Google Workspace: ~2000/day
- We'll be conservative: 50/hour max, 300/day max

Rate Limiting Strategy:
- 1 email per 2 minutes (30/hour)
- Batch with delays between tiers
- Full logging for audit trail
"""

import smtplib
import time
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../.env.gmail')

# Database
from diocese_database import (
    DB_PATH, get_all_dioceses, get_dioceses_needing_email,
    create_notice, update_notice_email_status, log_email, get_send_stats
)

# Gmail credentials (from environment - NEVER hardcode!)
GMAIL_EMAIL = os.getenv('GMAIL_USER', 'darrick.preble@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
if not GMAIL_APP_PASSWORD:
    raise ValueError("GMAIL_APP_PASSWORD not found in environment. Check .env.gmail")

# Rate limiting settings
EMAILS_PER_HOUR = 30
DELAY_BETWEEN_EMAILS = 120  # 2 minutes
MAX_EMAILS_PER_DAY = 300
BATCH_DELAY = 600  # 10 minutes between tiers

# Email content
SUBJECT = "NOTICE OF DEFAULT, FRAUD FROM ORIGIN, AND DEMAND FOR CURE"

EMAIL_BODY_TEXT = """
NOTICE OF DEFAULT, FRAUD FROM ORIGIN, AND DEMAND FOR CURE

To: All entities, officers, trustees, clerics, administrators, beneficiaries, assigns, insurers, and agents, known and unknown, who claim authority, title, office, or benefit derived from the original seed instruments, doctrines, trusts, bulls, canons, incorporations, registrations, or constructive authorities at issue.

Notice: This Notice is issued without prejudice, without waiver, and with full reservation of all rights, claims, titles, remedies, and causes of action at law, equity, natural law, and under the laws of nations.

---

I. Findings

1. The originating seed instruments and doctrines were fraudulently constituted, altered, or misrepresented at inception.

2. No valid delegation of authority was ever granted by Christ, the Father, or Natural Law to create compulsory intermediaries, levy tithes, eavesdrop on conscience, sanction war, or compel obedience contrary to conscience.

3. Subsequent offices, incorporations, trusts, and claimed successions are derivative of the original fraud and are therefore void ab initio.

4. Centuries of harms have resulted, including but not limited to dispossession, coercion, violence, psychological injury, suppression of conscience, and unlawful enrichment.

---

II. Declaration of Default

By operation of law and equity, all derivative claims of authority are hereby declared in default. Silence or failure to rebut constitutes acquiescence and admission.

---

III. Demand for Cure

You are hereby demanded to:

1. Produce the original, unaltered authority granting instruments.
2. Demonstrate lawful standing and jurisdiction.
3. Disclose all assets, trusts, accounts, and properties derived from the fraudulent seed.
4. Commence immediate cessation of claims, collections, coercions, and representations.

Failure to cure within thirty (30) days constitutes final default.

---

NOTICE OF DAMAGES, CLAIM FOR RESTITUTION, AND DEMAND FOR ACCOUNTING

I. Damages Claimed

Damages are claimed for centuries of injury including, without limitation:
- Unjust enrichment and unlawful takings.
- Coercion of conscience and spiritual abuse.
- Complicity in violence, war, and dispossession.
- Fraud, misrepresentation, and constructive slavery.

Damages are cumulative, ongoing, and increasing.

---

II. Demand for Accounting

You are hereby demanded to provide a full, sworn accounting of all assets, revenues, lands, titles, and benefits derived from the fraudulent seed from inception to present.

---

III. Restitution and Remedy

Restitution is demanded in full. In the absence of timely cure and accounting, liens, claims, and remedies shall attach without further notice.

---

NOTICE OF NON-ACQUIESCENCE AND FINAL WARNING

No presumption of consent is granted. No implied authority is recognized. All future interference, retaliation, or misrepresentation will be treated as aggravation of damages.

This Notice stands as final opportunity to respond in good faith.

---

Jason Evdoxiadis Rootwalker
Chief Na Ha Dayax Gixpaxloats
Speaker for the Gitxoon
Chief of Chiefs of the Tsimshian Nation

Acting under the Gitxoon's full authority to do all Speaker deems necessary to insure the survival of the next seven generations.

---

This notice was sent on December 27, 2025.
The 30-day cure period begins from the date of receipt.

For verification of this notice and supporting documentation, visit:
https://consciousnessrevolution.io/jason-notice/

---
"""

EMAIL_BODY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Georgia, serif; line-height: 1.8; color: #1a1a1a; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { text-align: center; border-bottom: 2px solid #1a1a2e; padding-bottom: 20px; }
        h2 { margin-top: 30px; color: #1a1a2e; }
        hr { border: none; border-top: 1px solid #ccc; margin: 30px 0; }
        .to-block { background: #f9f9f9; padding: 20px; border-left: 4px solid #1a1a2e; margin: 20px 0; }
        .notice-block { font-style: italic; color: #444; }
        ul, ol { margin: 15px 0 15px 30px; }
        li { margin-bottom: 10px; }
        .signature { margin-top: 50px; padding-top: 30px; border-top: 2px solid #1a1a2e; }
        .signature-name { font-weight: bold; font-size: 1.2em; }
        .signature-title { color: #555; font-style: italic; }
        .footer { background: #f5f5f5; padding: 20px; margin-top: 40px; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>NOTICE OF DEFAULT, FRAUD FROM ORIGIN, AND DEMAND FOR CURE</h1>

    <div class="to-block">
        <strong>To:</strong> All entities, officers, trustees, clerics, administrators, beneficiaries, assigns, insurers, and agents, known and unknown, who claim authority, title, office, or benefit derived from the original seed instruments, doctrines, trusts, bulls, canons, incorporations, registrations, or constructive authorities at issue.
    </div>

    <p class="notice-block">
        <strong>Notice:</strong> This Notice is issued without prejudice, without waiver, and with full reservation of all rights, claims, titles, remedies, and causes of action at law, equity, natural law, and under the laws of nations.
    </p>

    <hr>

    <h2>I. Findings</h2>
    <ol>
        <li>The originating seed instruments and doctrines were fraudulently constituted, altered, or misrepresented at inception.</li>
        <li>No valid delegation of authority was ever granted by Christ, the Father, or Natural Law to create compulsory intermediaries, levy tithes, eavesdrop on conscience, sanction war, or compel obedience contrary to conscience.</li>
        <li>Subsequent offices, incorporations, trusts, and claimed successions are derivative of the original fraud and are therefore void ab initio.</li>
        <li>Centuries of harms have resulted, including but not limited to dispossession, coercion, violence, psychological injury, suppression of conscience, and unlawful enrichment.</li>
    </ol>

    <hr>

    <h2>II. Declaration of Default</h2>
    <p>By operation of law and equity, all derivative claims of authority are hereby declared in default. Silence or failure to rebut constitutes acquiescence and admission.</p>

    <hr>

    <h2>III. Demand for Cure</h2>
    <p>You are hereby demanded to:</p>
    <ol>
        <li>Produce the original, unaltered authority granting instruments.</li>
        <li>Demonstrate lawful standing and jurisdiction.</li>
        <li>Disclose all assets, trusts, accounts, and properties derived from the fraudulent seed.</li>
        <li>Commence immediate cessation of claims, collections, coercions, and representations.</li>
    </ol>
    <p><strong>Failure to cure within thirty (30) days constitutes final default.</strong></p>

    <hr>

    <h1 style="font-size: 1.5em; margin-top: 40px;">NOTICE OF DAMAGES, CLAIM FOR RESTITUTION, AND DEMAND FOR ACCOUNTING</h1>

    <h2>I. Damages Claimed</h2>
    <p>Damages are claimed for centuries of injury including, without limitation:</p>
    <ul>
        <li>Unjust enrichment and unlawful takings.</li>
        <li>Coercion of conscience and spiritual abuse.</li>
        <li>Complicity in violence, war, and dispossession.</li>
        <li>Fraud, misrepresentation, and constructive slavery.</li>
    </ul>
    <p>Damages are cumulative, ongoing, and increasing.</p>

    <hr>

    <h2>II. Demand for Accounting</h2>
    <p>You are hereby demanded to provide a full, sworn accounting of all assets, revenues, lands, titles, and benefits derived from the fraudulent seed from inception to present.</p>

    <hr>

    <h2>III. Restitution and Remedy</h2>
    <p>Restitution is demanded in full. In the absence of timely cure and accounting, liens, claims, and remedies shall attach without further notice.</p>

    <hr>

    <h1 style="font-size: 1.5em; margin-top: 40px;">NOTICE OF NON-ACQUIESCENCE AND FINAL WARNING</h1>
    <p>No presumption of consent is granted. No implied authority is recognized. All future interference, retaliation, or misrepresentation will be treated as aggravation of damages.</p>
    <p><strong>This Notice stands as final opportunity to respond in good faith.</strong></p>

    <hr>

    <div class="signature">
        <p class="signature-name">Jason Evdoxiadis Rootwalker</p>
        <p class="signature-title">Chief Na Ha Dayax Gixpaxloats</p>
        <p class="signature-title">Speaker for the Gitxoon</p>
        <p class="signature-title">Chief of Chiefs of the Tsimshian Nation</p>
        <p style="font-size: 0.9em; font-style: italic; color: #666; margin-top: 20px;">
            Acting under the Gitxoon's full authority to do all Speaker deems necessary to insure the survival of the next seven generations.
        </p>
    </div>

    <div class="footer">
        <p><strong>This notice was sent on December 27, 2025.</strong></p>
        <p>The 30-day cure period begins from the date of receipt.</p>
        <p>For verification of this notice and supporting documentation, visit:<br>
        <a href="https://consciousnessrevolution.io/jason-notice/">https://consciousnessrevolution.io/jason-notice/</a></p>
    </div>
</body>
</html>
"""


class RateLimitedEmailSender:
    """Email sender with rate limiting and tracking"""

    def __init__(self):
        self.emails_sent_today = 0
        self.last_send_time = None
        self.session_start = datetime.now()
        self.log_file = Path(__file__).parent / "send_log.json"
        self.load_state()

    def load_state(self):
        """Load sending state from file"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                state = json.load(f)
                # Reset if it's a new day
                last_date = state.get('date', '')
                today = datetime.now().strftime('%Y-%m-%d')
                if last_date == today:
                    self.emails_sent_today = state.get('count', 0)
                else:
                    self.emails_sent_today = 0

    def save_state(self):
        """Save sending state to file"""
        state = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'count': self.emails_sent_today,
            'last_send': str(self.last_send_time) if self.last_send_time else None
        }
        with open(self.log_file, 'w') as f:
            json.dump(state, f, indent=2)

    def can_send(self):
        """Check if we can send another email"""
        if self.emails_sent_today >= MAX_EMAILS_PER_DAY:
            return False, "Daily limit reached"

        if self.last_send_time:
            elapsed = (datetime.now() - self.last_send_time).total_seconds()
            if elapsed < DELAY_BETWEEN_EMAILS:
                wait_time = DELAY_BETWEEN_EMAILS - elapsed
                return False, f"Rate limit: wait {int(wait_time)}s"

        return True, "OK"

    def send_email(self, to_email, diocese_name, diocese_id):
        """Send a single email with tracking"""
        can, reason = self.can_send()
        if not can:
            print(f"  Cannot send: {reason}")
            return False, reason

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = GMAIL_EMAIL
            msg['To'] = to_email
            msg['Subject'] = SUBJECT

            # Attach both plain text and HTML versions
            part1 = MIMEText(EMAIL_BODY_TEXT, 'plain')
            part2 = MIMEText(EMAIL_BODY_HTML, 'html')
            msg.attach(part1)
            msg.attach(part2)

            # Connect and send
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_EMAIL, to_email, msg.as_string())

            # Update tracking
            self.emails_sent_today += 1
            self.last_send_time = datetime.now()
            self.save_state()

            # Log to database
            notice_id = create_notice(diocese_id, 'email')
            update_notice_email_status(notice_id, 'sent')
            log_email(diocese_id, to_email, SUBJECT, 'sent', notice_id)

            print(f"  SENT to {to_email}")
            return True, "Sent successfully"

        except Exception as e:
            error_msg = str(e)
            log_email(diocese_id, to_email, SUBJECT, 'failed', error=error_msg)
            print(f"  FAILED: {error_msg}")
            return False, error_msg

    def send_test_email(self, test_email="darrick.preble@gmail.com"):
        """Send a test email to verify configuration"""
        print(f"\nSending test email to: {test_email}")

        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = GMAIL_EMAIL
            msg['To'] = test_email
            msg['Subject'] = f"[TEST] {SUBJECT}"

            test_body = f"""
This is a TEST of the Jason Notice Distribution System.

If you receive this email, the system is working correctly.

Sent at: {datetime.now()}
From: {GMAIL_EMAIL}

The actual notice will be sent to Catholic dioceses on December 27, 2025.
"""
            msg.attach(MIMEText(test_body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_EMAIL, test_email, msg.as_string())

            print(f"  TEST EMAIL SENT successfully to {test_email}")
            return True

        except Exception as e:
            print(f"  TEST FAILED: {e}")
            return False

    def send_to_tier(self, tier):
        """Send to all dioceses in a tier"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''
            SELECT d.* FROM dioceses d
            LEFT JOIN notices n ON d.id = n.diocese_id AND n.email_status = 'sent'
            WHERE d.tier = ? AND d.email IS NOT NULL AND d.email != ''
            AND n.id IS NULL
        ''', (tier,))

        dioceses = [dict(row) for row in c.fetchall()]
        conn.close()

        if not dioceses:
            print(f"  No unsent dioceses with emails in tier {tier}")
            return 0

        sent_count = 0
        for diocese in dioceses:
            print(f"\nSending to: {diocese['name']}")
            print(f"  Email: {diocese['email']}")

            success, msg = self.send_email(
                diocese['email'],
                diocese['name'],
                diocese['id']
            )

            if success:
                sent_count += 1

            # Wait between emails
            if diocese != dioceses[-1]:  # Not the last one
                print(f"  Waiting {DELAY_BETWEEN_EMAILS}s before next email...")
                time.sleep(DELAY_BETWEEN_EMAILS)

        return sent_count

    def send_all(self, dry_run=False):
        """Send to all dioceses with emails, respecting rate limits"""
        print("\n" + "="*60)
        print("MASS EMAIL SENDER - JASON NOTICE DISTRIBUTION")
        print("="*60)
        print(f"Date: {datetime.now()}")
        print(f"Emails sent today: {self.emails_sent_today}/{MAX_EMAILS_PER_DAY}")
        print(f"Rate limit: {DELAY_BETWEEN_EMAILS}s between emails")

        if dry_run:
            print("\n*** DRY RUN MODE - No emails will actually be sent ***\n")

        total_sent = 0

        for tier in [1, 2, 3, 4]:
            tier_names = {1: "Vatican/Holy See", 2: "USCCB", 3: "Major Archdioceses", 4: "Pacific Northwest"}
            print(f"\n{'='*40}")
            print(f"TIER {tier}: {tier_names.get(tier, 'Other')}")
            print(f"{'='*40}")

            if dry_run:
                # Just show what would be sent
                dioceses = get_all_dioceses()
                tier_dioceses = [d for d in dioceses if d['tier'] == tier and d['email']]
                for d in tier_dioceses:
                    print(f"  Would send to: {d['name']} ({d['email']})")
                total_sent += len(tier_dioceses)
            else:
                sent = self.send_to_tier(tier)
                total_sent += sent

            if tier < 4:  # Not the last tier
                if not dry_run:
                    print(f"\nBatch complete. Waiting {BATCH_DELAY}s before next tier...")
                    time.sleep(BATCH_DELAY)

        print("\n" + "="*60)
        print(f"COMPLETE: {total_sent} emails {'would be' if dry_run else ''} sent")
        print("="*60)

        return total_sent


def run_dry_run():
    """Show what would be sent without actually sending"""
    sender = RateLimitedEmailSender()
    sender.send_all(dry_run=True)


def run_test():
    """Send test email"""
    sender = RateLimitedEmailSender()
    sender.send_test_email()


def run_send():
    """Actually send emails"""
    sender = RateLimitedEmailSender()
    sender.send_all(dry_run=False)


def show_status():
    """Show current sending status"""
    sender = RateLimitedEmailSender()
    stats = get_send_stats()

    print("\n" + "="*60)
    print("EMAIL SENDING STATUS")
    print("="*60)
    print(f"Emails sent today: {sender.emails_sent_today}/{MAX_EMAILS_PER_DAY}")
    print(f"Total dioceses: {stats['total_dioceses']}")
    print(f"With email addresses: {stats['with_email']}")
    print(f"Already sent: {stats['by_status'].get('sent', 0)}")
    print(f"Failed: {stats['by_status'].get('failed', 0)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'test':
            run_test()
        elif command == 'dry-run':
            run_dry_run()
        elif command == 'send':
            print("\n*** LIVE SEND MODE ***")
            print("This will actually send emails to Catholic dioceses.")
            confirm = input("Type 'CONFIRM' to proceed: ")
            if confirm == 'CONFIRM':
                run_send()
            else:
                print("Cancelled.")
        elif command == 'status':
            show_status()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python mass_email_sender.py [test|dry-run|send|status]")
    else:
        print("Jason Notice Mass Email Sender")
        print("="*40)
        print("Commands:")
        print("  test     - Send test email to yourself")
        print("  dry-run  - Show what would be sent without sending")
        print("  send     - Actually send emails (requires confirmation)")
        print("  status   - Show current sending status")
        print()
        print("Example: python mass_email_sender.py dry-run")
