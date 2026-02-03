"""
DIOCESE DATABASE - Jason Notice Distribution System
====================================================
SQLite database for tracking notice distribution to Catholic dioceses.
Created: December 26, 2025
Target Launch: December 27, 2025 (Jason's Birthday)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "diocese_notices.db"

def init_database():
    """Create the database and tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Main dioceses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS dioceses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT DEFAULT 'diocese',  -- diocese, archdiocese, vatican, conference
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT DEFAULT 'USA',
            phone TEXT,
            email TEXT,
            website TEXT,
            bishop_name TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Notices tracking table
    c.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diocese_id INTEGER NOT NULL,
            notice_type TEXT DEFAULT 'master',  -- master, followup, final_demand
            method TEXT,  -- email, certified_mail, registered_mail, both
            email_sent_at TIMESTAMP,
            email_status TEXT DEFAULT 'pending',  -- pending, sent, delivered, bounced, opened
            mail_sent_at TIMESTAMP,
            mail_tracking_number TEXT,
            mail_status TEXT DEFAULT 'pending',  -- pending, sent, in_transit, delivered
            delivery_confirmed_at TIMESTAMP,
            cure_deadline DATE,  -- 30 days from delivery
            response_received_at TIMESTAMP,
            response_summary TEXT,
            status TEXT DEFAULT 'pending',  -- pending, sent, delivered, responded, defaulted
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (diocese_id) REFERENCES dioceses(id)
        )
    ''')

    # Email log for tracking individual sends
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diocese_id INTEGER NOT NULL,
            notice_id INTEGER,
            to_email TEXT NOT NULL,
            subject TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',  -- pending, sent, failed, bounced
            error_message TEXT,
            message_id TEXT,
            FOREIGN KEY (diocese_id) REFERENCES dioceses(id),
            FOREIGN KEY (notice_id) REFERENCES notices(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")
    return DB_PATH

def seed_initial_dioceses():
    """Seed the database with the 13 Phase 1 targets"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if already seeded
    c.execute("SELECT COUNT(*) FROM dioceses")
    if c.fetchone()[0] > 0:
        print("Database already seeded")
        conn.close()
        return

    # TIER 1: Vatican / Holy See
    tier1 = [
        (1, "His Holiness Pope Francis", "vatican", "Apostolic Palace", "Vatican City", None, "00120", "Vatican City", None, None, "www.vatican.va", "Pope Francis", "Do NOT add Italy to address"),
        (1, "Vatican Secretariat of State", "vatican", "Palazzo Apostolico Vaticano", "Vatican City", None, "00120", "Vatican City", "+39 06 698 83114", None, None, None, "Central administration"),
        (1, "Apostolic Nunciature (US Embassy)", "nunciature", "3339 Massachusetts Ave NW", "Washington", "DC", "20008", "USA", "(202) 333-7121", None, "www.nuntiususa.org", None, "Vatican's US representative"),
    ]

    # TIER 2: USCCB
    tier2 = [
        (2, "USCCB Headquarters", "conference", "3211 4th St NE", "Washington", "DC", "20017", "USA", "(202) 541-3000", None, "www.usccb.org", None, "National bishops conference"),
    ]

    # TIER 3: Major Archdioceses
    tier3 = [
        (3, "Archdiocese of Los Angeles", "archdiocese", "3424 Wilshire Blvd", "Los Angeles", "CA", "90010", "USA", "(213) 637-7000", None, "www.lacatholics.org", "Archbishop Jose Gomez", "Largest US diocese"),
        (3, "Archdiocese of New York", "archdiocese", "488 Madison Avenue", "New York", "NY", "10022", "USA", "(212) 371-1000", None, "www.archny.org", "Cardinal Timothy Dolan", "Recently moved from 1011 First Ave"),
        (3, "Archdiocese of Chicago", "archdiocese", "835 North Rush Street", "Chicago", "IL", "60611", "USA", "(312) 534-8200", None, "www.archchicago.org", "Cardinal Blase Cupich", None),
        (3, "Archdiocese of Philadelphia", "archdiocese", "222 North 17th Street", "Philadelphia", "PA", "19103", "USA", "(215) 587-3500", None, "www.archphila.org", "Archbishop Nelson Perez", None),
        (3, "Archdiocese of Boston", "archdiocese", "66 Brooks Drive", "Braintree", "MA", "02184", "USA", "(617) 254-0100", None, "www.bostoncatholic.org", "Cardinal Sean O'Malley", None),
        (3, "Archdiocese of San Francisco", "archdiocese", "1 Peter Yorke Way", "San Francisco", "CA", "94109", "USA", "(415) 614-5500", None, "www.sfarchdiocese.org", "Archbishop Salvatore Cordileone", None),
    ]

    # TIER 4: Pacific Northwest (Tsimshian Territory)
    tier4 = [
        (4, "Archdiocese of Seattle", "archdiocese", "710 9th Avenue", "Seattle", "WA", "98104", "USA", "(206) 382-4560", None, "www.seattlearchdiocese.org", "Archbishop Paul Etienne", "Primary PNW"),
        (4, "Archdiocese of Anchorage-Juneau", "archdiocese", "225 Cordova St, Building A", "Anchorage", "AK", "99501", "USA", "(907) 297-7700", None, "www.aoaj.org", "Archbishop Andrew Bellisario", "Alaska territory - merged diocese"),
        (4, "Archdiocese of Portland in Oregon", "archdiocese", "2838 E Burnside Street", "Portland", "OR", "97214", "USA", "(503) 234-5334", None, "www.archdpdx.org", "Archbishop Alexander Sample", "Oregon territory"),
    ]

    all_dioceses = tier1 + tier2 + tier3 + tier4

    for diocese in all_dioceses:
        c.execute('''
            INSERT INTO dioceses (tier, name, type, address, city, state, zip_code, country, phone, email, website, bishop_name, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', diocese)

    conn.commit()
    print(f"Seeded {len(all_dioceses)} dioceses")
    conn.close()

def get_all_dioceses():
    """Get all dioceses"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM dioceses ORDER BY tier, id")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_dioceses_by_tier(tier):
    """Get dioceses by tier"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM dioceses WHERE tier = ? ORDER BY id", (tier,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_dioceses_needing_email():
    """Get dioceses that have email addresses but haven't been emailed yet"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT d.* FROM dioceses d
        LEFT JOIN notices n ON d.id = n.diocese_id AND n.email_status != 'pending'
        WHERE d.email IS NOT NULL AND d.email != ''
        AND n.id IS NULL
        ORDER BY d.tier, d.id
    ''')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_diocese_email(diocese_id, email):
    """Update email for a diocese"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE dioceses SET email = ? WHERE id = ?", (email, diocese_id))
    conn.commit()
    conn.close()

def create_notice(diocese_id, method='email'):
    """Create a new notice record"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO notices (diocese_id, method)
        VALUES (?, ?)
    ''', (diocese_id, method))
    notice_id = c.lastrowid
    conn.commit()
    conn.close()
    return notice_id

def update_notice_email_status(notice_id, status, error=None):
    """Update email status for a notice"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status == 'sent':
        c.execute('''
            UPDATE notices
            SET email_status = ?, email_sent_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, notice_id))
    else:
        c.execute('''
            UPDATE notices
            SET email_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, notice_id))
    conn.commit()
    conn.close()

def log_email(diocese_id, to_email, subject, status='pending', notice_id=None, error=None, message_id=None):
    """Log an email send attempt"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO email_log (diocese_id, notice_id, to_email, subject, status, error_message, message_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (diocese_id, notice_id, to_email, subject, status, error, message_id))
    log_id = c.lastrowid
    conn.commit()
    conn.close()
    return log_id

def get_send_stats():
    """Get sending statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    stats = {}

    # Total dioceses
    c.execute("SELECT COUNT(*) FROM dioceses")
    stats['total_dioceses'] = c.fetchone()[0]

    # With email addresses
    c.execute("SELECT COUNT(*) FROM dioceses WHERE email IS NOT NULL AND email != ''")
    stats['with_email'] = c.fetchone()[0]

    # Emails sent today
    c.execute("SELECT COUNT(*) FROM email_log WHERE DATE(sent_at) = DATE('now') AND status = 'sent'")
    stats['sent_today'] = c.fetchone()[0]

    # By status
    c.execute("SELECT status, COUNT(*) FROM email_log GROUP BY status")
    stats['by_status'] = dict(c.fetchall())

    # By tier
    c.execute('''
        SELECT d.tier, COUNT(e.id)
        FROM dioceses d
        LEFT JOIN email_log e ON d.id = e.diocese_id AND e.status = 'sent'
        GROUP BY d.tier
    ''')
    stats['sent_by_tier'] = dict(c.fetchall())

    conn.close()
    return stats

def export_for_mailing():
    """Export addresses for physical mailing labels"""
    dioceses = get_all_dioceses()
    output = []
    for d in dioceses:
        addr = f"{d['name']}\n{d['address']}\n{d['city']}"
        if d['state']:
            addr += f", {d['state']}"
        if d['zip_code']:
            addr += f" {d['zip_code']}"
        if d['country'] and d['country'] != 'USA':
            addr += f"\n{d['country']}"
        output.append({
            'tier': d['tier'],
            'name': d['name'],
            'full_address': addr
        })
    return output

def print_status():
    """Print current database status"""
    dioceses = get_all_dioceses()
    stats = get_send_stats()

    print("\n" + "="*60)
    print("DIOCESE DATABASE STATUS")
    print("="*60)
    print(f"Total dioceses: {stats['total_dioceses']}")
    print(f"With email: {stats['with_email']}")
    print(f"Sent today: {stats['sent_today']}")
    print()

    for tier in [1, 2, 3, 4]:
        tier_dioceses = [d for d in dioceses if d['tier'] == tier]
        tier_names = {1: "Vatican/Holy See", 2: "USCCB", 3: "Major Archdioceses", 4: "Pacific Northwest"}
        print(f"TIER {tier}: {tier_names.get(tier, 'Other')} ({len(tier_dioceses)})")
        for d in tier_dioceses:
            email_status = "HAS EMAIL" if d['email'] else "NO EMAIL"
            print(f"  - {d['name']}: {email_status}")
        print()

if __name__ == "__main__":
    init_database()
    seed_initial_dioceses()
    print_status()

    # Show mailing addresses
    print("\nMAILING LABELS:")
    print("-"*40)
    for addr in export_for_mailing():
        print(f"\n[TIER {addr['tier']}]")
        print(addr['full_address'])
