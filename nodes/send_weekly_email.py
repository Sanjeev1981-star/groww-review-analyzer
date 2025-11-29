"""
Node: Send Email
Node name: Send_Weekly_Email
Type: Email / Gmail / SMTP node (whatever Qoder provides)
Inputs: email_subject, email_body from Parse_Email_JSON
To: your email / alias
Subject: map from email_subject
Body: map from email_body
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_weekly_email(email_subject, email_body, to_email, smtp_server=None, smtp_port=None, 
                     sender_email=None, sender_password=None):
    """
    Send weekly email with review insights.
    
    Args:
        email_subject (str): Subject of the email
        email_body (str): Body content of the email
        to_email (str): Recipient email address
        smtp_server (str): SMTP server address (optional)
        smtp_port (int): SMTP server port (optional)
        sender_email (str): Sender email address (optional)
        sender_password (str): Sender email password (optional)
        
    Note: In a real implementation, you would use environment variables or a secure
    configuration system for credentials.
    """
    
    # Use default values if not provided (for demo purposes)
    if not smtp_server:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    if not smtp_port:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    if not sender_email:
        sender_email = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
    if not sender_password:
        sender_password = os.getenv("SENDER_PASSWORD", "your-app-password")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = email_subject
    
    # Add body to email
    msg.attach(MIMEText(email_body, 'plain'))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print("Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Example usage (commented out for safety)
if __name__ == "__main__":
    # Sample email data
    sample_subject = "Weekly App Review Pulse - 2025-11-17"
    sample_body = """Groww App – Weekly Review Pulse (Week of 2025-11-17)

• Executive summary
  - This week saw mixed feedback with performance issues being a key concern
  - Onboarding experience received positive feedback from new users
  - Payment-related features showed improvement compared to last week

• Top Themes
  1. App Performance & Bugs: Several users reported crashes and slow loading times.
  2. Onboarding & KYC: New users found the registration process smooth.
  3. Payments & SIP: Users appreciated the streamlined payment process.

[Action] Investigate and resolve app performance issues reported by multiple users
[Action] Enhance the payment confirmation flow based on user feedback
[Action] Optimize the onboarding flow for better conversion rates"""
    
    # Note: This won't actually send an email unless you provide valid credentials
    # send_weekly_email(sample_subject, sample_body, "recipient@example.com")
    
    print("Email sending function ready. Configure SMTP credentials to send emails.")