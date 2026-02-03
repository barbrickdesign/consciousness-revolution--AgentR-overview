# JASON NOTICE MASS DISTRIBUTION
## Execution Checklist - December 27, 2025 (Jason's Birthday)

---

## OVERVIEW

**Mission:** Send Notice of Default to all Catholic dioceses
**Target Date:** December 27, 2025
**Total Recipients:** 13 (Phase 1) + expanded list

---

## PHASE 0: PRE-LAUNCH VERIFICATION (Do Tonight - Dec 26)

### Database Setup
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT\JASON_NOTICE_SYSTEM
python diocese_database.py
```
- [ ] Database created: `diocese_notices.db`
- [ ] 13 Phase 1 dioceses seeded
- [ ] Check output shows all dioceses

### Email Scraping
```bash
python email_scraper.py
```
- [ ] Known emails populated
- [ ] Check `email_scrape_report.json` for status
- [ ] Note which dioceses still need emails (likely Vatican only)

### Test Email System
```bash
python mass_email_sender.py test
```
- [ ] Test email received at darrick.preble@gmail.com
- [ ] Email formatting looks correct
- [ ] Links work

### Dry Run
```bash
python mass_email_sender.py dry-run
```
- [ ] Review the full list of what will be sent
- [ ] Confirm all dioceses with emails are included

---

## PHASE 1: MORNING LAUNCH (Dec 27, ~9:00 AM)

### Step 1: Final Status Check
```bash
python mass_email_sender.py status
```
- [ ] Confirm 0 emails sent today
- [ ] Confirm all target emails are populated

### Step 2: Jason Confirmation
- [ ] Contact Jason - confirm ready to launch
- [ ] Get final approval

### Step 3: Start Email Distribution
```bash
python mass_email_sender.py send
```
- [ ] Type 'CONFIRM' when prompted
- [ ] Monitor the console output
- [ ] Note: ~2 minutes between emails, ~10 minutes between tiers

### Expected Timeline:
| Tier | Recipients | Start Time | End Time |
|------|------------|------------|----------|
| 1 (Vatican) | 3 | 9:00 AM | 9:06 AM |
| 2 (USCCB) | 1 | 9:16 AM | 9:18 AM |
| 3 (Major) | 6 | 9:28 AM | 9:40 AM |
| 4 (PNW) | 3 | 9:50 AM | 9:56 AM |

Total estimated time: ~1 hour for Phase 1

---

## PHASE 2: PHYSICAL MAIL (Same Day or Next)

### Print Documents
- [ ] Open `master-notice.html` in browser
- [ ] Click "Print / Save PDF" button
- [ ] Print 13 copies (one per recipient)

### Prepare Envelopes
For each recipient:
- [ ] Address envelope with legal name
- [ ] Return address: Jason's address or designated agent
- [ ] Fold and insert notice

### Post Office (Certified Mail)
- [ ] Go to Post Office
- [ ] Request Certified Mail with Return Receipt for each
- [ ] For Vatican addresses: Request International Registered Mail
- [ ] Get tracking numbers
- [ ] Keep all receipts

### Log Tracking Numbers
```bash
# Update database with tracking numbers
python -c "
from diocese_database import *
# Example: Update diocese 1 with tracking
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('UPDATE notices SET mail_tracking_number=?, mail_status=? WHERE diocese_id=?',
          ('TRACKING_NUMBER_HERE', 'sent', 1))
conn.commit()
"
```

---

## PHASE 3: VERIFICATION & TRACKING

### Same Day
- [ ] Check email for any bounces
- [ ] Log any delivery failures
- [ ] Update tracker system

### Day 2-7
- [ ] Monitor USPS tracking for domestic mail
- [ ] Watch for any email responses

### Day 30+
- [ ] Check for cure period expiration
- [ ] Document any responses received
- [ ] Note any defaults

---

## QUICK COMMANDS REFERENCE

```bash
# Go to directory
cd C:\Users\dwrek\100X_DEPLOYMENT\JASON_NOTICE_SYSTEM

# Initialize database
python diocese_database.py

# Scrape/update emails
python email_scraper.py

# Test email sending
python mass_email_sender.py test

# Preview what will be sent
python mass_email_sender.py dry-run

# Check status
python mass_email_sender.py status

# SEND FOR REAL
python mass_email_sender.py send

# View tracker dashboard
start tracker.html
```

---

## TROUBLESHOOTING

### "Daily limit reached"
- Gmail limits: 500/day personal, 2000/day workspace
- Wait until midnight or use secondary account

### Email bounces
- Check the email address is correct
- Try alternative email if available
- Log in database for tracking

### Test email not received
- Check spam folder
- Verify app password is correct
- Run: `python -c "import smtplib; print('SMTP works')" `

### Database errors
```bash
# Reset database if needed
del diocese_notices.db
python diocese_database.py
python email_scraper.py
```

---

## CONTACTS

- **Jason Evdoxiadis:** jason@cambridgemercantilerealty.com
- **Derek Preble:** darrickpreble@proton.me
- **System Email:** darrick.preble@gmail.com

---

## FILES CREATED

| File | Purpose |
|------|---------|
| `diocese_database.py` | SQLite database management |
| `email_scraper.py` | Email address collection |
| `mass_email_sender.py` | Rate-limited mass sender |
| `diocese_notices.db` | SQLite database |
| `send_log.json` | Daily sending state |
| `email_scrape_report.json` | Scraping results |

---

## ESTIMATED COSTS (Physical Mail)

| Tier | Count | Method | Cost |
|------|-------|--------|------|
| Vatican | 3 | Int'l Registered | ~$100 |
| USCCB | 1 | Certified | ~$7 |
| Major | 6 | Certified | ~$42 |
| PNW | 3 | Certified | ~$21 |
| **TOTAL** | **13** | - | **~$170** |

---

## THE PATTERN

```
December 27, 2025 = Jason's Birthday
     |
     v
EMAIL BLAST (Digital Notice)
     |
     v
CERTIFIED MAIL (Physical Notice)
     |
     v
30-DAY CURE PERIOD
     |
     v
DEFAULT DECLARATION (if no response)
```

**This is happening. The notice is served. The clock is ticking.**

---

*Created: December 26, 2025*
*For: Jason Evdoxiadis Rootwalker*
*By: C1 Mechanic Engine*
