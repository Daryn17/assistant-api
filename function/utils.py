from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from email.message import EmailMessage

import smtplib
import os

_ = load_dotenv(find_dotenv())

APP_EMAIL_PASSWORD = os.environ["APP_EMAIL_PASSWORD"]
APP_EMAIL = os.environ["APP_EMAIL"]


def get_current_date_and_time():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    return f"The current date is {current_date}, and the time is {current_time}."


def send_email(client_email, agent_email, context):
    # Create the email message
    msg = EmailMessage()
    msg.set_content(context["body"])
    msg["Subject"] = context["subject"]
    msg["From"] = APP_EMAIL
    msg["To"] = f"{client_email}, {agent_email}"

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 465) as server:
        server.starttls()  # Upgrade the connection to secure
        server.login(APP_EMAIL, APP_EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()


# Usage
client_email = "your-email@example.com"


agent_email = "recipient@example.com"

context = {
    "body": "This is a test email from my Python function.",
    "subject": "Test Subject",
}

# Call the function
send_email(client_email, agent_email, context)
