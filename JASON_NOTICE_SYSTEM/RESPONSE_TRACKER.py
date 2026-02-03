"""
JASON NOTICE RESPONSE TRACKER
Checks Gmail for responses to the Notice of Default
Run daily to track who has responded
"""

import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Get authenticated Gmail service"""
    creds = None
    token_path = 'C:/Users/dwrek/.secrets/gmail_token.pickle'
    creds_path = 'C:/Users/dwrek/.secrets/gmail_credentials.json'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def check_responses():
    """Check for responses to Notice of Default"""

    # Load sent list
    with open('GMAIL_SEND_RESULTS.json', 'r') as f:
        sent_data = json.load(f)

    sent_emails = [item['email'] for item in sent_data['sent']]

    print("=" * 60)
    print("JASON NOTICE RESPONSE TRACKER")
    print(f"Checking responses since: {sent_data['started']}")
    print("=" * 60)

    try:
        service = get_gmail_service()

        # Search for replies from sent recipients
        responses = []

        for email in sent_emails:
            query = f'from:{email} after:2025/12/27'
            results = service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])

            if messages:
                responses.append({
                    'from': email,
                    'count': len(messages),
                    'message_ids': [m['id'] for m in messages]
                })

        if responses:
            print(f"\nRESPONSES RECEIVED: {len(responses)}")
            print("-" * 40)
            for r in responses:
                print(f"  {r['from']}: {r['count']} message(s)")
        else:
            print("\nNo responses yet.")

        # Also check for auto-replies
        print("\n" + "-" * 40)
        print("Checking for auto-replies...")

        auto_query = 'subject:(auto OR automatic OR "out of office" OR delivery) after:2025/12/27'
        auto_results = service.users().messages().list(userId='me', q=auto_query).execute()
        auto_messages = auto_results.get('messages', [])

        if auto_messages:
            print(f"Found {len(auto_messages)} auto-reply/delivery notifications")
        else:
            print("No auto-replies detected")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"Error accessing Gmail: {e}")
        print("Make sure gmail_credentials.json and token are set up.")


def days_remaining():
    """Calculate days until 30-day deadline"""
    notice_date = datetime(2025, 12, 27)
    deadline = datetime(2026, 1, 26)
    today = datetime.now()

    remaining = (deadline - today).days
    elapsed = (today - notice_date).days

    print(f"\n30-DAY DEADLINE TRACKER")
    print(f"  Notice sent: December 27, 2025")
    print(f"  Deadline: January 26, 2026")
    print(f"  Days elapsed: {elapsed}")
    print(f"  Days remaining: {remaining}")

    if remaining <= 0:
        print("\n  *** DEADLINE PASSED - DEFAULT IN EFFECT ***")
    elif remaining <= 7:
        print("\n  *** FINAL WEEK - DEADLINE APPROACHING ***")


if __name__ == "__main__":
    days_remaining()
    print()
    check_responses()
