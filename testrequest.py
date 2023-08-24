import requests
from requests import get
import json
import sensitive
import boto3
from botocore.exceptions import ClientError
import logging

email = input("Enter your email: ")
zip_code = input("Enter your zip code: ")
# Subscribe an email address to a topic
while True:
    base_url = "https://api.weatherapi.com/v1/current.json"
    api_key = sensitive.api_key
    # email = input("Enter your email: ")
    # zip_code = input("Enter your zip code: ")
    client = boto3.client('sns')
    logger = logging.getLogger()

    def subscribe(topic, protocol, endpoint):
        try:
            subscription = client.subscribe(
            TopicArn=sensitive.sns_topic_arn, Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
            logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
            print("Please confirm subscribtion...")
        except ClientError:
            logger.exception(
                "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
            print("Couldn't subscribe!")
            raise
        
        else:
            return subscription

    subscribe(sensitive.sns_topic_arn, 'email', email)

    print("Has the subscription been confirmed? y/n")
    if input() == "y":
        print("Subscribed!")
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
                beginning = f"Right now in your area {zip_code} it is cloudy"
            elif string2 in condition:
                beginning = f"Right now in your area {zip_code} it is clear"
            elif string3 in condition:
                beginning = f"Right now in your area {zip_code} it is raining"
            elif string4 in condition:
                beginning = f"Right now in your area {zip_code} it is overcast"

            response = client.publish(TopicArn=sensitive.sns_topic_arn,Message=f"{beginning} and the temperature is {temperature} degrees Fahrenheit.")
            print("Message sent")
            break
    elif input() == "n":
        print("Please confirm subscribtion...")
        continue