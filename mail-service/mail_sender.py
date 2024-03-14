from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()


class Event:
    def __init__(self, recipient, subject, message):
        self.recipient = recipient
        self.subject = subject
        self.message = message


class MailService:
    def __init__(self, smtp_host, smtp_port, sender_email, sender_password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, event):
        # email message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = event.recipient
        msg['Subject'] = event.subject
        msg.attach(MIMEText(event.message, 'plain'))

        # SMTP connection
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, event.recipient, msg.as_string())
            print("Mail sent")
            server.quit()


HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
SENDER_ADDRESS = os.environ.get("EMAIL_SENDER")
SENDER_PASSWORD = os.environ.get("EMAIL_SENDER_PASSWORD")

RECIPIENT_ADDRESS = "kenmithibe@gmail.com"
SUBJECT = "Critical Event Alert"
MESSAGE = """
Hi there, A critical event has occurred
This is a test email
"""

# test usage
event = Event(RECIPIENT_ADDRESS, SUBJECT, MESSAGE)

mail_service = MailService(HOST, PORT, SENDER_ADDRESS, SENDER_PASSWORD)
mail_service.send_email(event)
