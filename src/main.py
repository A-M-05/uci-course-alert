import json
import os
from scraper import fetch_course
from parser import validate_course_data, is_open
from db import init_db, get_last_status, upsert_course, was_notified
from notifier import send_email

COURSES_CONFIG = os.path.join(os.path.dirname(__file__), "../config/courses.json")

def run():
    init_db()

    with open(COURSES_CONFIG) as f:
        courses = json.load(f)

    for course in courses:
        code = course["code"]
        name = course["name"]
        term = course["term"]

        print(f"\n[CHECK] {name} ({code})")

        data = fetch_course(term, code)

        if not validate_course_data(data):
            print(f"[SKIP] Invalid data for {code}")
            continue

        last_status = get_last_status(code)
        current_status = data["status"]

        print(f"  Last: {last_status or 'N/A'} → Now: {current_status}")
        print(f"  Enrolled: {data['enrolled']} | Waitlist: {data['waitlist']}")

        # Only notify if: course just opened AND we haven't notified yet
        status_changed = last_status != current_status
        if is_open(data) and status_changed and not was_notified(code):
            print(f"  [ALERT] {name} just opened! Sending notification...")
            send_email(name, code, current_status)
            upsert_course(data, name, notified=1)
        else:
            upsert_course(data, name, notified=0 if not is_open(data) else 1)
            print(f"  [NO CHANGE] No notification needed.")

if __name__ == "__main__":
    run()
