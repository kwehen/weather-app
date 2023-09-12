import smtplib, ssl
import sensitive
from email.mime.text import MIMEText
import requests
from requests import get

carrier_dict = {
    "AT&T": "txt.att.net",
    "T-Mobile": "tmomail.net",
    "Verizon": "vtext.com",
}

number = input("Enter your phone number: ")
carrier = input("Enter your carrier: ")
zip_code = input("Enter your zip code: ")
zip_url = "https://api.api-ninjas.com/v1/zipcode"
city = requests.get(f"{zip_url}?zip={zip_code}", headers={"X-Api-Key": sensitive.zip_api_key})
city = city.json()
area = city[0]['city']
email_subject = f"{area} Weather Updates"

if carrier in carrier_dict:
    reciever_email = f"{number}@{carrier_dict[carrier]}"
else:
    reciever_email = input("No Carrier? Enter your email:")
port = 465
password = sensitive.email_password
sender_email = sensitive.sender_email
subject = email_subject
text = "test"
context = ssl.create_default_context()

base_url = "https://api.weatherapi.com/v1/current.json"
api_key = sensitive.api_key

r = requests.get(f"{base_url}?key={api_key}&q={zip_code}")
r = r.json()
if "error" in r:
    print(f"{zip_code} is not a valid zip code")
else:
    condition = r["current"]["condition"]["text"]
    temperature = r["current"]["temp_f"]

    string = "cloudy"
    string2 = "clear"
    string3 = "rain"
    string4 = "cast"
    string5 = "heavy"
    string6 = "thunder"
    string7 = "Mist"

    if string in condition:
        beginning = f"Right now in {area} it is cloudy"
    elif string2 in condition:
        beginning = f"Right now in {area} it is clear"
    elif string3 in condition:
        beginning = f"Right now in {area} it is raining"
    elif string4 in condition:
        beginning = f"Right now in {area} it is overcast"
    elif string7 in condition:
        beginning = f"Right now in {area} it is misty"
    elif string3 and string5 in condition:
        beginning = f"Right now in {area} it is raining heavily"
    elif string3 and string5 and string6 in condition:
        beginning = f"Right now in {area} it is raining heavily with thunder"
    else:
        beginning = f"Right now the condition in your area is {condition}, please add this to the conditions"

    response = f"{beginning} and the temperature is {temperature} degrees Fahrenheit."


message = f'Subject: {subject}\n\n {response}'.format(subject, text)
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    try:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)
        print("Message sent!")
    except:
        print("Something went wrong")