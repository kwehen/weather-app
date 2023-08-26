import requests
from requests import get
import json
import sensitive
import boto3
from botocore.exceptions import ClientError
import logging

email = input("Enter your email: ")
zip_code = input("Enter your zip code: ")
zip_url = "https://api.api-ninjas.com/v1/zipcode"


city = requests.get(f"{zip_url}?zip={zip_code}", headers={"X-Api-Key": sensitive.zip_api_key})
city = city.json()
area = city[0]['city']
pre_name = f"{area}_WeatherUpdates"
pre_name = pre_name.replace(" ", "_")
topic_name = pre_name
sns_client = boto3.client('sns')
logger = logging.getLogger()


def create_topic(name):
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info("Created topic %s with ARN %s.", name, topic)
        print(f"{name} created.")
    except ClientError:
        logger.exception("Couldn't create topic %s.", name)
        print(f"Couldn't create {name}")
        raise
    else:
        return topic
    
def subscribe(topic, protocol, endpoint):
    try:
        subscription = sns_client.subscribe(
        TopicArn=topic['TopicArn'], Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
        logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
        print("Please confirm subscribtion...")
    except ClientError:
        logger.exception(
            "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
        print("Couldn't subscribe!")
        raise

    else:
        return subscription

topicArn = create_topic(topic_name)
subscribe(topicArn, 'email', email)
while True:
    base_url = "https://api.weatherapi.com/v1/current.json"
    api_key = sensitive.api_key
    # email = input("Enter your email: ")
    # zip_code = input("Enter your zip code: ")
    # sns_client = boto3.client('sns')
    # logger = logging.getLogger()

    # def create_topic(name):
    #     try:
    #         topic = sns_client.create_topic(Name=name)
    #         logger.info("Created topic %s with ARN %s.", name, topic)
    #         print(f"{name} created.")
    #     except ClientError:
    #         logger.exception("Couldn't create topic %s.", name)
    #         print(f"Could not create {name}.")
    #         raise
    #     else:
    #         return topic
    
    # topicArn = create_topic(topic_name)

    # def subscribe(topic, protocol, endpoint):
    #     try:
    #         subscription = sns_client.subscribe(
    #         TopicArn=topic['TopicArn'], Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
    #         logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
    #         print("Please confirm subscribtion...")
    #     except ClientError:
    #         logger.exception(
    #             "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
    #         print("Couldn't subscribe!")
    #         raise

    #     else:
    #         return subscription

    # subscribe(topicArn, 'email', email)

    print("Has the subscription been confirmed? y/n")
    if input() == "y":
        print("Subscribed!")
        pass
    elif input() == "n":
        print("Please confirm subscribtion...")
        continue
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
            beginning = f"Right now in {area} it is cloudy"
        elif string2 in condition:
            beginning = f"Right now in {area} it is clear"
        elif string3 in condition:
            beginning = f"Right now in {area} it is raining"
        elif string4 in condition:
            beginning = f"Right now in {area} it is overcast"

        response = sns_client.publish(TopicArn=topicArn,Message=f"{beginning} and the temperature is {temperature} degrees Fahrenheit.")
        print("Message sent")
        break