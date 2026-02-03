"""
PROTONMAIL PLAYWRIGHT SENDER - PRODUCTION VERSION
Sends Jason's Notice of Default to churches via ProtonMail web automation
Created: December 27, 2025

Usage:
  python PROTON_PLAYWRIGHT_SENDER.py              # Dry run (shows what would send)
  python PROTON_PLAYWRIGHT_SENDER.py --test       # Send to Derek, Jason, Erica only
  python PROTON_PLAYWRIGHT_SENDER.py --send       # LIVE: Send to all 59 churches
"""

from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../.env.protonmail')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Account to send from (from environment - NEVER hardcode!)
SENDER_EMAIL = os.getenv('PROTON_EMAIL', 'darrickpreble@protonmail.com')
SENDER_PASSWORD = os.getenv('PROTON_PASSWORD')
if not SENDER_PASSWORD:
    raise ValueError("PROTON_PASSWORD not found in environment. Check .env.protonmail")

# Paths
NOTICE_PDF = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/NOTICE_OF_DEFAULT_FINAL.pdf"
RESULTS_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/SEND_RESULTS.json"

# Email content
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

# ============================================================================
# RECIPIENT LISTS
# ============================================================================

TEST_EMAILS = [
    "darrick.preble@gmail.com",
    "evdoxiadisj@gmail.com",
    "ericadavis2011@gmail.com",
]

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

ALL_CHURCH_EMAILS = CATHOLIC_EMAILS + ORTHODOX_EMAILS

# ============================================================================
# FUNCTIONS
# ============================================================================

def login_protonmail(page):
    """Log into ProtonMail"""
    print(f"Logging in as {SENDER_EMAIL}...")
    page.goto("https://mail.proton.me/login")
    time.sleep(3)

    page.wait_for_selector('input[id="username"]', timeout=15000)
    page.fill('input[id="username"]', SENDER_EMAIL)
    page.fill('input[id="password"]', SENDER_PASSWORD)
    page.click('button[type="submit"]')

    # Wait for inbox
    try:
        page.wait_for_selector('[data-testid="sidebar:compose"]', timeout=60000)
        print("Login successful!")
        return True
    except:
        print("Login may have failed - checking...")
        page.screenshot(path="login_check.png")
        return False


def dismiss_popups(page):
    """Dismiss any upgrade or notification popups"""
    try:
        maybe_later = page.locator('text=Maybe later')
        if maybe_later.count() > 0:
            maybe_later.click()
            time.sleep(1)
    except:
        pass

    try:
        close_btns = page.locator('button[aria-label="Close"]')
        if close_btns.count() > 0:
            close_btns.first.click()
            time.sleep(0.5)
    except:
        pass


def send_single_email(page, to_email, subject, body, attachment_path=None):
    """Send a single email through ProtonMail web interface"""
    try:
        # Click compose
        page.click('[data-testid="sidebar:compose"]')
        time.sleep(2)

        # Dismiss any popups
        dismiss_popups(page)
        time.sleep(1)

        # Fill To field
        to_container = page.locator('[data-testid="composer:to"]')
        to_container.click()
        time.sleep(0.3)
        page.keyboard.type(to_email)
        time.sleep(0.3)
        page.keyboard.press('Tab')

        # Fill Subject
        subj = page.locator('input[data-testid="composer:subject"]')
        if subj.count() > 0:
            subj.fill(subject)
        else:
            page.locator('input[placeholder="Subject"]').fill(subject)

        time.sleep(0.5)

        # Fill Body via iframe
        try:
            iframe = page.frame_locator('iframe[data-testid="rooster-iframe"]')
            body_el = iframe.locator('div[contenteditable="true"]')
            body_el.click()
            # Type the body
            page.keyboard.type(body, delay=1)  # Small delay for stability
        except:
            # Fallback
            page.locator('[contenteditable="true"]').first.click()
            page.keyboard.type(body, delay=1)

        time.sleep(1)

        # Attach PDF if provided
        if attachment_path and os.path.exists(attachment_path):
            print(f"    Attaching: {os.path.basename(attachment_path)}")
            # Find the attachment button and file input
            attach_btn = page.locator('[data-testid="composer:attachment-button"]')
            if attach_btn.count() > 0:
                attach_btn.click()
                time.sleep(1)

            # Set file on the hidden input
            file_input = page.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.set_input_files(attachment_path)
                time.sleep(3)  # Wait for upload
                print("    Attachment uploaded!")

        # Click Send
        page.locator('button:has-text("Send")').click()
        time.sleep(3)

        # Check for errors
        error = page.locator('text=Recipient missing')
        if error.count() > 0:
            print(f"    ERROR: Recipient missing for {to_email}")
            # Close composer
            page.locator('button[aria-label="Close"]').click()
            return False

        return True

    except Exception as e:
        print(f"    ERROR: {e}")
        # Try to close composer
        try:
            page.locator('button[aria-label="Close"]').click()
        except:
            pass
        return False


def run_sender(mode="dry_run"):
    """
    Main sender function

    mode: "dry_run" - just show what would be sent
          "test" - send to Derek, Jason, Erica only
          "live" - send to all 59 churches
    """

    if mode == "test":
        emails = TEST_EMAILS
        print(f"\n{'='*60}")
        print("TEST MODE - Sending to 3 test recipients")
        print(f"{'='*60}\n")
    elif mode == "live":
        emails = ALL_CHURCH_EMAILS
        print(f"\n{'='*60}")
        print(f"LIVE MODE - Sending to {len(emails)} churches")
        print(f"{'='*60}\n")
    else:
        emails = ALL_CHURCH_EMAILS
        print(f"\n{'='*60}")
        print("DRY RUN - No emails will be sent")
        print(f"{'='*60}")
        print(f"\nWould send to {len(emails)} recipients:")
        for i, email in enumerate(emails, 1):
            print(f"  [{i}] {email}")
        print(f"\nSubject: {SUBJECT}")
        print(f"Attachment: {NOTICE_PDF}")
        print(f"\nTo send for real, run:")
        print("  python PROTON_PLAYWRIGHT_SENDER.py --test   (test with 3 recipients)")
        print("  python PROTON_PLAYWRIGHT_SENDER.py --send   (send to all 59)")
        return

    results = {
        "started": datetime.now().isoformat(),
        "mode": mode,
        "sender": SENDER_EMAIL,
        "total": len(emails),
        "sent": [],
        "failed": []
    }

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        if not login_protonmail(page):
            print("LOGIN FAILED!")
            browser.close()
            return

        time.sleep(2)
        dismiss_popups(page)

        for i, email in enumerate(emails, 1):
            print(f"\n[{i}/{len(emails)}] Sending to: {email}")

            success = send_single_email(
                page,
                email,
                SUBJECT,
                COVER_LETTER,
                NOTICE_PDF
            )

            if success:
                print(f"    -> SENT!")
                results["sent"].append({"email": email, "time": datetime.now().isoformat()})
            else:
                print(f"    -> FAILED!")
                results["failed"].append({"email": email, "time": datetime.now().isoformat()})

            # Rate limit
            if i < len(emails):
                print("    Waiting 5 seconds...")
                time.sleep(5)

        results["completed"] = datetime.now().isoformat()

        # Save results
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"COMPLETE!")
        print(f"  Sent: {len(results['sent'])}")
        print(f"  Failed: {len(results['failed'])}")
        print(f"  Results saved to: {RESULTS_FILE}")
        print(f"{'='*60}")

        print("\nClosing browser in 5 seconds...")
        time.sleep(5)
        browser.close()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--test":
            run_sender(mode="test")

        elif arg == "--send":
            # Require --force flag for safety
            if len(sys.argv) > 2 and sys.argv[2] == "--force":
                print("\n" + "!"*60)
                print("LIVE MODE - SENDING TO ALL 59 CHURCHES!")
                print("!"*60)
                run_sender(mode="live")
            else:
                print("\n" + "!"*60)
                print("WARNING: This will send to 59 church email addresses!")
                print("!"*60)
                print("\nTo confirm, add --force:")
                print("  python PROTON_PLAYWRIGHT_SENDER.py --send --force")

        else:
            print(f"Unknown argument: {arg}")
            print("Usage:")
            print("  python PROTON_PLAYWRIGHT_SENDER.py              # Dry run")
            print("  python PROTON_PLAYWRIGHT_SENDER.py --test       # Test (3 recipients)")
            print("  python PROTON_PLAYWRIGHT_SENDER.py --send       # Show warning")
            print("  python PROTON_PLAYWRIGHT_SENDER.py --send --force  # LIVE (59 churches)")
    else:
        run_sender(mode="dry_run")
