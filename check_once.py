import requests
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
NOTIFY_EMAIL = "gokuult8@gmail.com"
CHECK_URL = "https://appointment.theitalyvisa.com/Global/appointment/NewAppointment"
MAX_RETRIES = 3
RETRY_DELAY = 30

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = NOTIFY_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
    print(f"[{datetime.now()}] Email sent: {subject}")

import time

def check_slots():
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
                print(f"[{datetime.now()}] No slots yet.")
            return
        except Exception as e:
            print(f"[{datetime.now()}] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    print(f"[{datetime.now()}] All retries failed. Skipping.")

check_slots()
