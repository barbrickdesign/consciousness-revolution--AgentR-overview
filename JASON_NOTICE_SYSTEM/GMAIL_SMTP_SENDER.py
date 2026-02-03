"""
RELIABLE GMAIL SMTP SENDER
Sends Jason's Notice via Gmail SMTP with PDF attachment
Created: December 27, 2025
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../../.env.gmail')

# Gmail SMTP Config (from environment - NEVER hardcode!)
GMAIL_USER = os.getenv('GMAIL_USER', 'darrick.preble@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
if not GMAIL_APP_PASSWORD:
    raise ValueError("GMAIL_APP_PASSWORD not found in environment. Check .env.gmail")

# Files
PDF_PATH = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/NOTICE_OF_DEFAULT_FINAL.pdf"
RESULTS_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/JASON_NOTICE_SYSTEM/GMAIL_SEND_RESULTS.json"

# Email Content
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

# All 59 Recipients
ALL_EMAILS = [
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
    "ecumenical.patriarchate@gmail.com",
    "ovcs@patriarchia.ru",
    "communications@goarch.org",
    "archdiocese@antiochian.org",
    "info@oca.org",
    "serborth@aol.com",
]


def send_with_attachment(to_email, subject, body, pdf_path):
    """Send email with PDF attachment via Gmail SMTP"""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    # Body
    msg.attach(MIMEText(body, 'plain'))

    # Attachment
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype='pdf')
            pdf.add_header('Content-Disposition', 'attachment',
                          filename='Notice_of_Default_Fraud_from_Origin.pdf')
            msg.attach(pdf)

    # Send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)

    return True


def run_send(dry_run=True):
    """Send to all recipients"""

    if dry_run:
        print("=" * 60)
        print("DRY RUN - Would send to:")
        print("=" * 60)
        for i, email in enumerate(ALL_EMAILS, 1):
            print(f"  [{i}] {email}")
        print(f"\nTotal: {len(ALL_EMAILS)} recipients")
        print(f"Subject: {SUBJECT}")
        print(f"Attachment: {PDF_PATH}")
        print("\nTo send for real: python GMAIL_SMTP_SENDER.py --send")
        return

    results = {
        "started": datetime.now().isoformat(),
        "sender": GMAIL_USER,
        "total": len(ALL_EMAILS),
        "sent": [],
        "failed": []
    }

    print("=" * 60)
    print(f"SENDING TO {len(ALL_EMAILS)} RECIPIENTS")
    print("=" * 60)

    for i, email in enumerate(ALL_EMAILS, 1):
        print(f"[{i}/{len(ALL_EMAILS)}] {email}...", end=" ", flush=True)

        try:
            send_with_attachment(email, SUBJECT, COVER_LETTER, PDF_PATH)
            print("SENT!")
            results["sent"].append({"email": email, "time": datetime.now().isoformat()})
        except Exception as e:
            print(f"FAILED: {e}")
            results["failed"].append({"email": email, "error": str(e)})

        # Rate limit - 2 seconds between emails
        if i < len(ALL_EMAILS):
            time.sleep(2)

    results["completed"] = datetime.now().isoformat()

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"COMPLETE!")
    print(f"  Sent: {len(results['sent'])}")
    print(f"  Failed: {len(results['failed'])}")
    print(f"  Results: {RESULTS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        run_send(dry_run=False)
    else:
        run_send(dry_run=True)
