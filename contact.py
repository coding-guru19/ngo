from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from datetime import datetime, timezone
import json
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. Try to load the .env file explicitly
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__, static_folder='.', static_url_path='')

MESSAGES_FILE = os.path.join(basedir, "messages.jsonl")

# 2. Retrieve environment variables
# FALLBACK: If .env fails, we use the values you provided directly
GMAIL_USER = os.getenv("GMAIL_USER") or "itu1nkoana@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD") or "kufefzsajhkelxhs"
TO_EMAIL = os.getenv("TO_EMAIL") or "itu9shabalala@gmail.com"

# --- Templates ---
THANK_YOU_HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thank you</title>
</head>
<body style="font-family: system-ui; padding: 40px; text-align: center;">
    <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h1 style="color: #0B1F3B;">✅ Message received</h1>
        <p>Thanks for reaching out! Check your email.</p>
        <p><a href="/" style="color: #C9A227; font-weight: bold;">← Back to home</a></p>
    </div>
</body>
</html>
"""

ERROR_HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Error</title></head>
<body style="font-family: system-ui; padding: 40px;">
    <h1>⚠️ Form error</h1>
    <p style="color: red; font-weight: bold;">{{ error }}</p>
    <p><a href="/">← Try again</a></p>
</body>
</html>
"""

def send_email(subject: str, body: str):
    # Debug print so you can see if the variables are actually loaded in the terminal
    print(f"DEBUG: Attempting to send from {GMAIL_USER} to {TO_EMAIL}")
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    try:
        # Use Port 587 (most reliable)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
            print("✅ SUCCESS: Email sent successfully.")
            return True
    except Exception as e:
        print(f"❌ SMTP ERROR: {e}")
        return False

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.post("/contact")
def handle_contact():
    full_name = (request.form.get("full_name") or "").strip()
    email = (request.form.get("email") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not full_name or not email or len(message) < 10:
        return render_template_string(ERROR_HTML, error="All fields are required (message min 10 chars)."), 400

    # Save logic
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"full_name": full_name, "email": email, "message": message, "timestamp": timestamp}

    try:
        with open(MESSAGES_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print(f"FILE ERROR: {e}")

    # Send the email
    subject = f"Website Contact: {full_name}"
    email_body = f"User Name: {full_name}\nUser Email: {email}\n\nMessage:\n{message}"
    send_email(subject, email_body)

    return redirect(url_for("thank_you"))

@app.get("/thank-you")
def thank_you():
    return render_template_string(THANK_YOU_HTML)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
