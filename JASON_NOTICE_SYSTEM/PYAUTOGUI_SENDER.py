"""
PYAUTOGUI PROTONMAIL SENDER
Uses existing logged-in browser session via mouse/keyboard automation
Created: December 27, 2025
"""

import pyautogui
import time
import pyperclip
from datetime import datetime
import json

# Safety settings
pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True  # Move mouse to corner to abort

# Paths
RESULTS_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/PYAUTOGUI_RESULTS.json"

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


def click_new_message():
    """Click the New message button in ProtonMail"""
    # Look for the purple "New message" button
    try:
        loc = pyautogui.locateOnScreen('new_message_btn.png', confidence=0.8)
        if loc:
            pyautogui.click(loc)
            return True
    except:
        pass

    # Fallback: use keyboard shortcut
    pyautogui.hotkey('c')  # ProtonMail shortcut for compose
    return True


def send_email_via_gui(to_email, subject, body):
    """Send an email using the existing ProtonMail browser window"""
    try:
        # Click compose (keyboard shortcut 'c' or 'n')
        print(f"  Composing...")
        pyautogui.press('n')  # New message shortcut
        time.sleep(2)

        # Type recipient
        print(f"  Entering recipient: {to_email}")
        pyperclip.copy(to_email)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)

        # Skip CC/BCC, go to subject
        pyautogui.press('tab')
        time.sleep(0.3)

        # Type subject
        print(f"  Entering subject...")
        pyperclip.copy(subject)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)

        # Type body
        print(f"  Entering body...")
        pyperclip.copy(body)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        # Send with Ctrl+Enter
        print(f"  Sending...")
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(3)

        return True

    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def run_sender(emails, dry_run=True):
    """Send to list of emails"""

    if dry_run:
        print("=" * 60)
        print("DRY RUN - Would send to:")
        print("=" * 60)
        for i, email in enumerate(emails, 1):
            print(f"  [{i}] {email}")
        print("=" * 60)
        return

    results = {
        "started": datetime.now().isoformat(),
        "total": len(emails),
        "sent": [],
        "failed": []
    }

    print("=" * 60)
    print("STARTING SEND - Keep ProtonMail window focused!")
    print("Move mouse to corner to ABORT")
    print("=" * 60)

    # Give user time to focus browser
    print("\nFocusing ProtonMail in 3 seconds...")
    time.sleep(3)

    for i, email in enumerate(emails, 1):
        print(f"\n[{i}/{len(emails)}] {email}")

        success = send_email_via_gui(email, SUBJECT, COVER_LETTER)

        if success:
            print(f"  -> SENT!")
            results["sent"].append(email)
        else:
            print(f"  -> FAILED!")
            results["failed"].append(email)

        # Wait between emails
        if i < len(emails):
            print("  Waiting 5 seconds...")
            time.sleep(5)

    results["completed"] = datetime.now().isoformat()

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {len(results['sent'])} sent, {len(results['failed'])} failed")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--send":
            print("\nThis will send to ALL 59 churches using your browser!")
            print("Make sure ProtonMail (brotherpapa777) is open and focused.")
            run_sender(ALL_EMAILS, dry_run=False)
        elif sys.argv[1] == "--test":
            # Send to first 3 only
            run_sender(ALL_EMAILS[:3], dry_run=False)
    else:
        run_sender(ALL_EMAILS, dry_run=True)
