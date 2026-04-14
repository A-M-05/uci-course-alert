import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms(course_name: str, course_code: str, status: str):
    """Sends an SMS notification via Twilio."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token  = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    to_number   = os.getenv("TWILIO_TO_NUMBER")

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=(
            f"🔔 UCI Course Alert!\n"
            f"{course_name} ({course_code})\n"
            f"Status changed to: {status}\n"
            f"Enroll now at webreg.uci.edu"
        ),
        from_=from_number,
        to=to_number
    )
    print(f"[SMS SENT] SID: {message.sid}")


def send_email(course_name: str, course_code: str, status: str):
    """Fallback: sends an email notification via Gmail SMTP."""
    import smtplib
    from email.mime.text import MIMEText

    sender   = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    body = (
        f"Course Alert: {course_name} ({course_code})\n"
        f"Status: {status}\n"
        f"Go enroll: https://webreg.uci.edu"
    )
    msg = MIMEText(body)
    msg["Subject"] = f"[UCI Notifier] {course_name} is now {status}"
    msg["From"]    = sender
    msg["To"]      = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
        print("[EMAIL SENT]")
