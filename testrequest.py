import requests
from requests import get
import json
import sensitive


base_url = "https://api.weatherapi.com/v1/current.json"
api_key = sensitive.api_key
# ip = get('https://api.ipify.org').content.decode('utf8')
zip_code = input("Enter your zip code: ")

r = requests.get(f"{base_url}?key={api_key}&q={zip_code}")
r = r.json()
condition = r["current"]["condition"]["text"]
temperature = r["current"]["temp_f"]

string = "cloudy"
string2 = "clear"
string3 = "rain"

if string in condition:
    beginning = "Right now it is cloudy"
elif string2 in condition:
    beginning = "Right now it is clear"
elif string3 in condition:
    beginning = "Right now it is raining"


print(f"{beginning} and the temperature is {temperature} degrees Fahrenheit")