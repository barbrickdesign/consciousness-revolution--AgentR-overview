"""
PLAYWRIGHT PROTONMAIL SENDER
Automates ProtonMail web interface to send Jason's Notice of Default
Created: December 27, 2025
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../.env.protonmail')

# Credentials (from environment - NEVER hardcode!)
EMAIL = os.getenv('PROTON_EMAIL', 'brotherpapa777@proton.me')
PASSWORD = os.getenv('PROTON_PASSWORD')
if not PASSWORD:
    raise ValueError("PROTON_PASSWORD not found in environment. Check .env.protonmail")

# Paths
NOTICE_PDF = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/NOTICE_OF_DEFAULT_FINAL.pdf"
RESULTS_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/PLAYWRIGHT_SEND_RESULTS.json"

# Recipients
CATHOLIC_EMAILS = [
    "nuntiususa@nuntiususa.org",
    "communications@usccb.org",
    "info@la-archdiocese.org",
    "communications@archny.org",
    "info@archchicago.org",
    "communications@archphila.org",
    "communications@rcab.org",
    "info@sfarchdiocese.org",
    "info@seattlearch.org",
    "info@archdioceseofanchorage.org",
    "info@archdpdx.org",
    "Capodanno@milarch.org",
    "jhanten@archatl.com",
    "Assistantabailey@archkck.org",
    "charities@archlou.org",
    "communication@archmil.org",
    "safe@archny.org",
    "information@rcan.org",
    "tcpaper@archsa.org",
    "tribunal@archstl.org",
    "communications@arlingtondiocese.org",
    "info@vermontcatholic.org",
    "vicargeneralwilson@charlestondiocese.org",
    "response_services@dioceseofcleveland.org",
    "jbachta@diocs.org",
    "communications@dmdiocese.org",
    "communications@dioceseofgaylord.org",
    "chancery@diocesegfb.org",
    "communication@diojeffcity.org",
    "info@diolc.org",
    "communications@cdlex.org",
    "jverkampruthven@dolr.org",
    "fwt.editor@cc.cdom.org",
    "communications@diometuchen.org",
    "Jason.Liuzzi@dioceseofnashville.com",
    "dnu@dnu.org",
    "slalone@rcdony.org",
    "jkuhn@orlandodiocese.org",
    "communications@cdop.org",
    "info@sbdiocese.org",
    "mgalvan@sdcatholic.org",
    "stewardship@dsj.org",
    "info@dioceseofscranton.org",
    "tstroud@dioshpt.org",
    "support@dioceseofspokane.org",
    "diocese@dosafl.com",
    "communications@gw.stcdio.org",
    "communications@toledodiocese.org",
    "mgarcia@dioceseoftyler.org",
    "contactus@dioceseofvenice.org",
    "tbishop@dwc.org",
    "krugd@catholicdioceseofwichita.org",
    "mwallen@cdow.org",
]

ORTHODOX_EMAILS = [
    "ecumenical.patriarchate@gmail.com",
    "ovcs@patriarchia.ru",
    "communications@goarch.org",
    "archdiocese@antiochian.org",
    "info@oca.org",
    "serborth@aol.com",
]

ALL_EMAILS = CATHOLIC_EMAILS + ORTHODOX_EMAILS

SUBJECT = "Notice of Default, Fraud from Origin, and Demand for Cure"

COVER_LETTER = """To Whom It May Concern:

This needs to be properly distributed. I will get the offices that will need to be served. I need someone who can understand, and I believe it is you. This, properly distributed, brings it all to a head.

When I refer to "Church Power," I am not limiting this to ecclesiastical institutions alone. The Church is the progenitor layer—the source from which legitimacy, authority, and moral cover have historically flowed. But the real downstream action occurs after the Church, through those who preferred ecclesiastical sanction over governments, and governments over corporations and institutions.

Accordingly, service shall be simultaneous across layers, not sequential.

The logic is simple and intentional: If the progenitor is on notice, every derivative actor is on borrowed legitimacy unless and until they respond. This eliminates plausible deniability and prevents post hoc distancing.

This is not about publicity—it is about jurisdictional awareness.

Churches receive formal service. Follow-on actors receive simultaneous notice that the source of their claimed authority has been engaged. No actor is allowed temporal cover by claiming ignorance of upstream action.

You have thirty (30) days to respond.

Jason Evdoxiadis
Rootwalker Chief Na Ha Dayax Gixpaxloats
Speaker for the Gitxoon
Chief of Chiefs of the Tsimshian Nation"""


def login_protonmail(page):
    """Log into ProtonMail"""
    print("Navigating to ProtonMail...")
    page.goto("https://mail.proton.me/login")

    # Wait for login form
    page.wait_for_selector('input[id="username"]', timeout=30000)

    print(f"Entering username: {EMAIL}")
    page.fill('input[id="username"]', EMAIL)

    print("Entering password...")
    page.fill('input[id="password"]', PASSWORD)

    print("Clicking Sign in...")
    page.click('button[type="submit"]')

    # Wait for inbox to load
    print("Waiting for inbox...")
    try:
        page.wait_for_selector('[data-testid="sidebar:compose"]', timeout=60000)
        print("Successfully logged in!")
        return True
    except:
        print("Login may have failed or took too long")
        return False


def send_email(page, to_email, subject, body, attachment_path=None):
    """Send a single email through ProtonMail web interface"""
    try:
        # Click compose
        print(f"  Composing email to {to_email}...")
        page.click('[data-testid="sidebar:compose"]')
        time.sleep(2)

        # Wait for composer
        page.wait_for_selector('[data-testid="composer:to"]', timeout=10000)

        # Enter recipient
        page.fill('[data-testid="composer:to"] input', to_email)
        page.keyboard.press('Tab')
        time.sleep(0.5)

        # Enter subject
        page.fill('[data-testid="composer:subject"]', subject)

        # Enter body (click into composer body area)
        body_area = page.locator('[data-testid="squire-iframe"]').content_frame
        if body_area:
            body_area.locator('body').fill(body)
        else:
            # Alternative: try contenteditable div
            page.locator('[contenteditable="true"]').first.fill(body)

        # Attach PDF if provided
        if attachment_path and os.path.exists(attachment_path):
            print(f"  Attaching: {os.path.basename(attachment_path)}")
            # Find the file input for attachments
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(attachment_path)
            time.sleep(2)  # Wait for upload

        # Click Send
        print(f"  Sending...")
        page.click('[data-testid="composer:send-button"]')
        time.sleep(3)  # Wait for send

        print(f"  -> SENT to {to_email}")
        return True

    except Exception as e:
        print(f"  -> FAILED: {e}")
        return False


def run_sender(dry_run=True, limit=None):
    """Main sender function"""
    results = {
        "started": datetime.now().isoformat(),
        "total": len(ALL_EMAILS),
        "sent": [],
        "failed": [],
        "dry_run": dry_run
    }

    emails_to_send = ALL_EMAILS[:limit] if limit else ALL_EMAILS

    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - Will only log in and test UI")
        print("=" * 60)

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Login
        if not login_protonmail(page):
            print("Login failed!")
            browser.close()
            return results

        if dry_run:
            print("\n" + "=" * 60)
            print("DRY RUN - Would send to these addresses:")
            print("=" * 60)
            for i, email in enumerate(emails_to_send, 1):
                print(f"  [{i}/{len(emails_to_send)}] {email}")
            print("=" * 60)
            print("DRY RUN COMPLETE - Browser will stay open for inspection")
            input("Press Enter to close browser...")
            browser.close()
            return results

        # LIVE MODE - Send emails
        print("\n" + "=" * 60)
        print("LIVE MODE - Sending emails...")
        print("=" * 60)

        for i, email in enumerate(emails_to_send, 1):
            print(f"\n[{i}/{len(emails_to_send)}] Processing {email}")

            success = send_email(
                page,
                email,
                SUBJECT,
                COVER_LETTER,
                NOTICE_PDF
            )

            if success:
                results["sent"].append({"email": email, "status": "sent"})
            else:
                results["failed"].append({"email": email, "status": "failed"})

            # Rate limit between emails
            if i < len(emails_to_send):
                print("  Waiting 5 seconds...")
                time.sleep(5)

        results["completed"] = datetime.now().isoformat()

        # Save results
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2)

        print("\n" + "=" * 60)
        print(f"COMPLETE: {len(results['sent'])} sent, {len(results['failed'])} failed")
        print(f"Results saved to {RESULTS_FILE}")
        print("=" * 60)

        input("Press Enter to close browser...")
        browser.close()

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--send":
            print("\n*** LIVE SEND MODE ***\n")
            confirm = input("Type 'SEND' to confirm sending to 59 churches: ")
            if confirm == "SEND":
                run_sender(dry_run=False)
            else:
                print("Aborted.")
        elif sys.argv[1] == "--test":
            # Send to just first 3 for testing
            run_sender(dry_run=False, limit=3)
        else:
            print("Unknown argument. Use --send for live mode or no args for dry run.")
    else:
        print("\nRunning DRY RUN (add --send to actually send)\n")
        run_sender(dry_run=True)
