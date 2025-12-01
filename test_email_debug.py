
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def test_email():
    sender_email = "rsanjeev525@gmail.com"
    sender_password = "dsnvaldmagfhyetr"
    recipient_email = "sanjeev-anil.reddy@capgemini.com"

    print(f"Attempting to send email...")
    print(f"From: {sender_email}")
    print(f"To: {recipient_email}")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Test Email from Debug Script"
    msg.attach(MIMEText("This is a test email to verify SMTP credentials.", 'plain'))

    try:
        print("Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        print("Starting TLS...")
        server.starttls()
        print("Logging in...")
        server.login(sender_email, sender_password)
        print("Sending mail...")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("SUCCESS: Email sent successfully!")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    test_email()
