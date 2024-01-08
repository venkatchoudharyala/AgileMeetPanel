import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_password):
    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Use this line if you're using a secure connection (TLS)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())

# Example usage
subject = "Meeting Notes"
body = "Hello,\n\nHere are the meeting notes from our recent session.\n\nBest regards,\nYour Name"
to_email = "recipient@example.com"

# Set up your SMTP server details
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your_email@gmail.com"  # Replace with your Gmail email address
smtp_password = "your_password"  # Replace with your Gmail app password

# Send the email
send_email(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_password)
