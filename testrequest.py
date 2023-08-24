import requests
from requests import get
import json
import sensitive


while True:
    base_url = "https://api.weatherapi.com/v1/current.json"
    api_key = sensitive.api_key
    zip_code = input("Enter your zip code: ")

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

        if string in condition:
            beginning = "Right now it is cloudy"
        elif string2 in condition:
            beginning = "Right now it is clear"
        elif string3 in condition:
            beginning = "Right now it is raining"
        elif string4 in condition:
            beginning = "Right now it is overcast"

        print(f"{beginning} and the temperature is {temperature} degrees Fahrenheit.")
        break