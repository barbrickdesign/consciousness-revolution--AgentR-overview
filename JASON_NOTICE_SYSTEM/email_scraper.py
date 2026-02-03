"""
DIOCESE EMAIL SCRAPER - Jason Notice Distribution System
=========================================================
Scrapes email addresses from USCCB directory and Catholic hierarchy websites.
Created: December 26, 2025
Target Launch: December 27, 2025 (Jason's Birthday)

Sources:
- USCCB Diocese Directory: usccb.org/about/bishops-and-dioceses/all-dioceses
- Catholic-Hierarchy.org: catholic-hierarchy.org
- Individual archdiocese websites
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from pathlib import Path
import sqlite3

# Import our database module
from diocese_database import DB_PATH, update_diocese_email, get_all_dioceses

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def extract_emails_from_text(text):
    """Extract email addresses from text using regex"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    # Filter out common false positives
    filtered = []
    for email in emails:
        email_lower = email.lower()
        # Skip image files, common placeholders
        if not any(x in email_lower for x in ['.png', '.jpg', '.gif', 'example.com', 'email@']):
            filtered.append(email)
    return list(set(filtered))

def scrape_usccb_directory():
    """Scrape the USCCB diocese directory for contact information"""
    url = "https://www.usccb.org/about/bishops-and-dioceses/all-dioceses"
    print(f"Scraping USCCB directory: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        dioceses = []

        # Look for diocese links and info
        # The USCCB page lists dioceses with links to their individual pages
        links = soup.find_all('a', href=re.compile(r'/about/bishops-and-dioceses/dioceses/'))

        for link in links:
            diocese_name = link.get_text(strip=True)
            diocese_url = link.get('href')
            if diocese_url and not diocese_url.startswith('http'):
                diocese_url = f"https://www.usccb.org{diocese_url}"

            dioceses.append({
                'name': diocese_name,
                'usccb_url': diocese_url
            })

        print(f"Found {len(dioceses)} dioceses on USCCB directory")
        return dioceses

    except Exception as e:
        print(f"Error scraping USCCB: {e}")
        return []

def scrape_diocese_page(url):
    """Scrape individual diocese page for contact info"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text and find emails
        text = soup.get_text()
        emails = extract_emails_from_text(text)

        # Look for specific contact sections
        contact_info = {
            'emails': emails,
            'phones': [],
            'address': None,
            'website': None
        }

        # Find phone numbers
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info['phones'] = list(set(phones))[:3]  # Keep up to 3

        # Find external website links
        for link in soup.find_all('a', href=re.compile(r'^https?://')):
            href = link.get('href', '')
            if 'usccb.org' not in href and 'facebook' not in href and 'twitter' not in href:
                if any(x in href for x in ['diocese', 'archdiocese', 'catholic']):
                    contact_info['website'] = href
                    break

        return contact_info

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_archdiocese_website(url):
    """Scrape an archdiocese website directly for contact info"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for contact page link
        contact_links = soup.find_all('a', href=re.compile(r'contact', re.I))

        emails = []
        for link in contact_links[:3]:  # Check first 3 contact links
            contact_url = link.get('href')
            if contact_url:
                if not contact_url.startswith('http'):
                    contact_url = url.rstrip('/') + '/' + contact_url.lstrip('/')
                try:
                    contact_response = requests.get(contact_url, headers=HEADERS, timeout=30)
                    found_emails = extract_emails_from_text(contact_response.text)
                    emails.extend(found_emails)
                    time.sleep(1)  # Be nice
                except:
                    pass

        # Also check main page
        main_emails = extract_emails_from_text(response.text)
        emails.extend(main_emails)

        return list(set(emails))

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Known email addresses for major archdioceses (manually verified)
KNOWN_EMAILS = {
    "Archdiocese of Los Angeles": ["info@la-archdiocese.org", "communications@la-archdiocese.org"],
    "Archdiocese of New York": ["communications@archny.org"],
    "Archdiocese of Chicago": ["info@archchicago.org", "communications@archchicago.org"],
    "Archdiocese of Philadelphia": ["communications@archphila.org"],
    "Archdiocese of Boston": ["communications@rcab.org", "info@rcab.org"],
    "Archdiocese of San Francisco": ["info@sfarchdiocese.org"],
    "Archdiocese of Seattle": ["info@seattlearch.org", "communications@seattlearch.org"],
    "Archdiocese of Anchorage-Juneau": ["info@archdioceseofanchorage.org"],
    "Archdiocese of Portland in Oregon": ["info@archdpdx.org", "communications@archdpdx.org"],
    "USCCB Headquarters": ["communications@usccb.org", "media@usccb.org"],
    "Apostolic Nunciature (US Embassy)": ["nuntiususa@nuntiususa.org"],
}

def update_known_emails():
    """Update database with known email addresses"""
    dioceses = get_all_dioceses()

    for diocese in dioceses:
        name = diocese['name']
        if name in KNOWN_EMAILS:
            emails = KNOWN_EMAILS[name]
            primary_email = emails[0]
            update_diocese_email(diocese['id'], primary_email)
            print(f"Updated {name} with email: {primary_email}")

def scrape_all():
    """Run full scraping process"""
    print("="*60)
    print("DIOCESE EMAIL SCRAPER")
    print("="*60)

    # First, update with known emails
    print("\n1. Updating with known email addresses...")
    update_known_emails()

    # Then try to scrape for additional emails
    print("\n2. Scraping USCCB directory...")
    usccb_dioceses = scrape_usccb_directory()

    # Get our dioceses that still need emails
    dioceses = get_all_dioceses()
    need_email = [d for d in dioceses if not d['email']]

    if not need_email:
        print("\nAll dioceses have email addresses!")
        return

    print(f"\n3. {len(need_email)} dioceses still need email addresses")

    # Try to scrape from their websites
    for diocese in need_email:
        if diocese['website']:
            print(f"\nScraping {diocese['name']} website: {diocese['website']}")
            emails = scrape_archdiocese_website(diocese['website'])
            if emails:
                print(f"  Found: {emails}")
                update_diocese_email(diocese['id'], emails[0])
            time.sleep(2)  # Be respectful of rate limits

    print("\n" + "="*60)
    print("SCRAPING COMPLETE")
    print("="*60)

def generate_email_report():
    """Generate a report of all dioceses and their email status"""
    dioceses = get_all_dioceses()

    report = {
        'generated': str(datetime.now()) if 'datetime' in dir() else 'now',
        'total': len(dioceses),
        'with_email': len([d for d in dioceses if d['email']]),
        'without_email': len([d for d in dioceses if not d['email']]),
        'dioceses': []
    }

    for d in dioceses:
        report['dioceses'].append({
            'tier': d['tier'],
            'name': d['name'],
            'email': d['email'] or 'NEEDS EMAIL',
            'website': d['website']
        })

    return report

if __name__ == "__main__":
    from datetime import datetime

    # Run the scraper
    scrape_all()

    # Generate report
    print("\n" + "="*60)
    print("EMAIL STATUS REPORT")
    print("="*60)

    report = generate_email_report()
    print(f"Total dioceses: {report['total']}")
    print(f"With email: {report['with_email']}")
    print(f"Without email: {report['without_email']}")

    print("\nBy diocese:")
    for d in report['dioceses']:
        status = "OK" if d['email'] != 'NEEDS EMAIL' else "MISSING"
        print(f"  [{status}] Tier {d['tier']}: {d['name']}")
        if d['email'] != 'NEEDS EMAIL':
            print(f"         Email: {d['email']}")

    # Save report
    report_path = Path(__file__).parent / "email_scrape_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {report_path}")
