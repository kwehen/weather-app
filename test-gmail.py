import smtplib, ssl
import sensitive
from email.mime.text import MIMEText

port = 465
password = sensitive.email_password
sender_email = sensitive.sender_email
reciever_email = sensitive.reciever_email
subject = "Weather Updates"
text = "test"
context = ssl.create_default_context()
message = f'Subject: {subject}\n\n This is a test email'.format(subject, text)


with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, reciever_email, message)