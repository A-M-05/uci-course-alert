# uci-course-alert

A Python automation tool that monitors UCI's course registration system (WebSoc) and sends an email notification the moment a course opens up.

Runs automatically every 30 minutes via GitHub Actions — no server or manual intervention required.

---

## How It Works

1. **GitHub Actions** triggers the workflow every 30 minutes
2. **Scraper** fires a POST request to UCI's WebSoc and parses the HTML response
3. **Parser** validates the scraped data before doing anything with it
4. **Database** compares the current status against the last known state stored in SQLite
5. **Notifier** sends an email via Gmail SMTP if the course just opened and you haven't been notified yet

---

## Project Structure

``` bash
uci-course-alert/
├── .github/
│   └── workflows/
│       └── check_courses.yml   # GitHub Actions scheduler
├── src/
│   ├── scraper.py              # Fetches and parses WebSoc HTML
│   ├── parser.py               # Validates scraped data
│   ├── db.py                   # SQLite state tracking
│   ├── notifier.py             # Gmail email notification
│   └── main.py                 # Orchestrator
├── data/
│   └── courses.db              # SQLite database (auto-created)
├── config/
│   └── courses.json            # Courses you want to track
├── tests/
│   └── test_parser.py          # Pytest unit tests
├── .env                        # Local credentials (never committed)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/uci-course-alert.git
cd uci-course-alert
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your courses

Edit `config/courses.json` with the courses you want to track:

```json
[
    {
        "code": "12345",
        "name": "ABCD 101 INTRO TO ALPHABET",
        "term": "2026-14"
    }
]
```

To find the 5-digit course code, search for your course on [UCI WebSoc](https://www.reg.uci.edu/perl/WebSoc). The term string follows the format `YYYY-XX` where the number matches WebSoc's internal term ID (e.g. `2026-14` for Spring Quarter 2026).

### 4. Set up environment variables

Create a `.env` file in the root directory:

``` plaintext
EMAIL_SENDER=yourgmail@gmail.com
EMAIL_PASSWORD=your16charapppassword
EMAIL_RECEIVER=yourgmail@gmail.com
```

`EMAIL_PASSWORD` must be a **Gmail App Password**, not your regular Gmail password. Generate one at [myaccount.google.com](https://myaccount.google.com) under **Security → App Passwords** (requires 2FA enabled).

### 5. Run locally

```bash
python -m src.main
```

---

## GitHub Actions (Automated)

The workflow runs every 30 minutes automatically. To enable it on your own fork:

1. Go to **Settings → Secrets and Variables → Actions**
2. Add three repository secrets:
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECEIVER`
3. Push your code — the workflow activates automatically

To manually trigger a run, go to the **Actions** tab and click **Run workflow**.

To pause it, go to **Actions → Check UCI Course Availability → Disable workflow**.

---

## Running Tests

```bash
pytest
```

Four tests cover the parser: valid open course, full course, missing field, and `None` input.

---

## Tech Stack

- **Python 3.11**
- **requests** — HTTP requests to WebSoc
- **BeautifulSoup4** — HTML parsing
- **sqlite3** — built-in state tracking across runs
- **smtplib** — built-in email via Gmail SMTP
- **python-dotenv** — local environment variable loading
- **pytest** — unit testing
- **GitHub Actions** — automated scheduling
