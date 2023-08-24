import requests
import json
import sensitive

base_url = "https://api.weatherapi.com/v1/current.json"
api_key = sensitive.api_key
zip_code = input("Enter your zip code: ")

r = requests.get(f"{base_url}?key={api_key}&q={zip_code}")
r = r.json()
condition = r["current"]["condition"]["text"]

string = "cloudy"

if string in condition:
    print("Right not it is cloudy")
else:
    print("Right now it is not cloudy")
