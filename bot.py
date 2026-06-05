import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
NOTIFY_EMAIL = "gokuult8@gmail.com"

CHECK_URL = "https://appointment.theitalyvisa.com/Global/appointment/NewAppointment"
CHECK_INTERVAL = 300   # 5 minutes
HEARTBEAT_INTERVAL = 86400  # 24 hours
MAX_RETRIES = 3
RETRY_DELAY = 30  # seconds between retries

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = NOTIFY_EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"[{datetime.now()}] Email sent: {subject}")
    except Exception as e:
        print(f"[{datetime.now()}] Email error: {e}")

def check_slots():
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(CHECK_URL, headers=headers, timeout=10)
            if "no slot" not in response.text.lower() and response.status_code == 200:
                send_email(
                    "✅ Italy Visa Slot AVAILABLE!",
                    f"A slot has opened up! Book immediately:\nhttps://appointment.theitalyvisa.com\n\nChecked at: {datetime.now()}"
                )
            else:
                print(f"[{datetime.now()}] No slots yet...")
            return  # success — exit retry loop
        except Exception as e:
            last_error = e
            print(f"[{datetime.now()}] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"[{datetime.now()}] Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

    print(f"[{datetime.now()}] All {MAX_RETRIES} attempts failed. Skipping this cycle.")

send_email(
    "🤖 Italy Visa Bot Started",
    f"The slot checker bot has started successfully.\n\nChecking every {CHECK_INTERVAL // 60} minutes.\nRetries on failure: up to {MAX_RETRIES} attempts ({RETRY_DELAY}s apart).\nDaily heartbeat emails every 24 hours.\n\nStarted at: {datetime.now()}"
)

last_heartbeat = time.time()

while True:
    check_slots()

    if time.time() - last_heartbeat >= HEARTBEAT_INTERVAL:
        send_email(
            "💓 Italy Visa Bot — Daily Heartbeat",
            f"The bot is alive and still checking for slots.\n\nChecking every {CHECK_INTERVAL // 60} minutes.\nRetries on failure: up to {MAX_RETRIES} attempts ({RETRY_DELAY}s apart).\nNext heartbeat in 24 hours.\n\nTimestamp: {datetime.now()}"
        )
        last_heartbeat = time.time()

    time.sleep(CHECK_INTERVAL)
