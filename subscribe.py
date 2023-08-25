import boto3
import json
from botocore.exceptions import ClientError
import logging
import sensitive

logger = logging.getLogger()
sns_client=boto3.client('sns')
email = input("Enter your email: ")

# def subscribe(topic, protocol, endpoint):
#     try:
#         subscription = sns_client.subscribe(
#         TopicArn=sensitive.sns_topic_arn, Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
#         logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
#         print("Please confirm subscribtion...")
#     except ClientError:
#         logger.exception(
#             "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
#         print("Couldn't subscribe!")
#         raise
    
#     else:
#         return subscription

# subscribe(sensitive.sns_topic_arn, 'email', email)

def create_topic(name):
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info("Created topic %s with ARN %s.", name, topic)
        print(f"{name} created.")
    except ClientError:
        logger.exception("Couldn't create topic %s.", name)
        print(f"Could not create {name}.")
        raise
    else:
        return topic

topic_name = "WeatherUpdates"
topicArn = create_topic(topic_name)

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
    
subscribe(topicArn, 'email', email)