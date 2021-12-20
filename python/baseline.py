import logging
import boto3
import time
import random

from lambda_wrapper import Lambda
from sns_wrapper import SimpleNotificationService
from sqs_wrapper import SimpleQueueService
from dynamodb_wrapper import DynamoDB

ACCOUNT_ID = ['866658200244']
logger = logging.getLogger(__name__)


def create_resources():
    return boto3.resource('sns'), boto3.resource('sqs'), boto3.resource('dynamodb'), boto3.client('lambda')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    sns_resource, sqs_resource, dynamodb_resource, lambda_resource = create_resources()

    attributes_sns = {}
    attributes_sqs = {}

    # Instantiating our wrappers
    sns = SimpleNotificationService(sns_resource)
    sqs = SimpleQueueService(sqs_resource)
    dynamodb = DynamoDB(dynamodb_resource)
    lambda_wrapper = Lambda(lambda_resource)  # has a special name cuz lambda word is reserved

    # Creating our SNS topic
    topic = sns.create_topic("topicbase", attributes_sns)

    # Creating a standard SQS queue
    queue = sqs.create_queue("queuebase", attributes_sqs)
    policy = sqs.generate_policy(queue, [topic])
    # Editing policy to allow SNS to publish on SQS
    sqs.set_attributes(queue, {'Policy': policy})
    # Subscribe the queue to the formerly created topic
    subscription = sns.subscribe(topic, queue)

    # Creating the Lambda function
    lambda_function = lambda_wrapper.create_function("lambdabase")

    # Adding the trigger on SQS messages
    mapping = lambda_wrapper.add_trigger(queue, lambda_function)

    # Creating the DynamoDB table
    table = dynamodb.create_table("DBbase")

    # Wait until everything is properly instantiated
    time.sleep(5)

    # Test message
    for i in range(0, 500):
        sns.publish_message(topic, "DB_entry",
                            {"table": "DBbase",
                             "id_concert": f"{random.randrange(10)}",
                             "id_customer": f"{i}",
                             "ticket_class": f"{random.choice(['classic', 'premium', 'gold'])}",
                             "date": "19/12/2021"})

    # Wait until everything has finished
    time.sleep(60)

    # Cleaning AWS components
    sns.delete_topic(topic)
    sqs.delete_queue(queue)
    dynamodb.delete_table(table)
    lambda_wrapper.delete_trigger(mapping, lambda_function)
    lambda_wrapper.delete_function(lambda_function)
