# ItalySlotBot

A Python bot that monitors the Italy visa appointment website and sends email alerts when a slot becomes available.

## Features

- Checks for available slots every 5 minutes
- Sends an email alert instantly when a slot is found
- Daily heartbeat email to confirm the bot is still running
- Retries up to 3 times on network errors before skipping a cycle

## Setup

1. Clone the repo
2. Install dependencies: `pip install requests`
3. Set the following environment variables:
   - `GMAIL_USER` — your Gmail address
   - `GMAIL_APP_PASSWORD` — a Gmail App Password (generate at https://myaccount.google.com/apppasswords)

## Run

```bash
python scripts/src/hello.py
```

## Environment Variables

| Variable | Description |
|---|---|
| `GMAIL_USER` | Gmail address used to send emails |
| `GMAIL_APP_PASSWORD` | Gmail App Password (not your regular password) |
