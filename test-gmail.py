import smtplib, ssl
import sensitive
from email.mime.text import MIMEText

carrier_dict = {
    "AT&T": "txt.att.net",
    "T-Mobile": "tmomail.net",
    "Verizon": "vtext.com",
}

number = input("Enter your phone number: ")
carrier = input("Enter your carrier: ")

if carrier in carrier_dict:
    reciever_email = f"{number}@{carrier_dict[carrier]}"
port = 465
password = sensitive.email_password
sender_email = sensitive.sender_email
subject = "Weather Updates"
text = "test"
context = ssl.create_default_context()
message = f'Subject: {subject}\n\n This is a test email'.format(subject, text)


with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    try:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)
        print("Message sent!")
    except:
        print("Something went wrong")