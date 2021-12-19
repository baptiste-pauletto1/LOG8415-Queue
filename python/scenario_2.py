import logging
import boto3
import time
import random
import multiprocessing

from lambda_wrapper import Lambda
from sns_wrapper import SimpleNotificationService
from sqs_wrapper import SimpleQueueService
from dynamodb_wrapper import DynamoDB

ACCOUNT_ID = ['866658200244']
logger = logging.getLogger(__name__)


def create_resources():
    return boto3.resource('sns'), boto3.resource('sqs'), boto3.resource('dynamodb'), boto3.client('lambda')


def send_messages(num_user):
    for id_topic in range(0, 2):
        sns.publish_message(topics[id_topic], "SC2_entry",
                            {"table": "DBSC2",
                             "id_concert": f"{id_topic}",
                             "id_customer": f"{num_user}",
                             "ticket_class": f"{random.choice(['classic', 'premium', 'gold'])}",
                             "date": "31/12/2021"}, 'T' + str(id_topic) + "_U" + str(num_user), str(num_user))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    sns_resource, sqs_resource, dynamodb_resource, lambda_resource = create_resources()

    attributes_sns = {'FifoTopic': 'true'}
    attributes_sqs = {'FifoQueue': 'true'}

    # Instantiating our wrappers
    sns = SimpleNotificationService(sns_resource)
    sqs = SimpleQueueService(sqs_resource)
    dynamodb = DynamoDB(dynamodb_resource)
    lambda_wrapper = Lambda(lambda_resource)  # has a special name cuz lambda word is reserved

    # Creating a standard SQS queue
    queue = sqs.create_queue("queueSC2.fifo", attributes_sqs)

    # Creating the Lambda function
    lambda_function = lambda_wrapper.create_function("lambdaSC2")

    topics = []

    # Generating topics
    for i in range(0, 2):
        topic = sns.create_topic(f"topicSC2_{i}.fifo", attributes_sns)
        topics.append(topic)

        # Subscribe the queue to the formerly created topic
        subscription = sns.subscribe(topic, queue)

    # Generating policy in order to let all topics publish to the SQS queue
    policy = sqs.generate_policy(queue, topics)

    # Editing policy to allow SNS to publish on SQS
    sqs.set_attributes(queue, {'Policy': policy})

    # Adding the trigger on SQS messages
    mapping = lambda_wrapper.add_trigger(queue, lambda_function)

    # Creating the DynamoDB table
    table = dynamodb.create_table("DBSC2")

    # Wait until everything is properly instantiated
    time.sleep(5)

    # Initializing pool for parallel execution
    pool_object = multiprocessing.Pool()
    pool_object.map(send_messages, range(0, 5))

    # Wait until everything has finished
    time.sleep(120)

    # Cleaning AWS components
    for topic in topics:
        sns.delete_topic(topic)
    sqs.delete_queue(queue)
    dynamodb.delete_table(table)
    lambda_wrapper.delete_trigger(mapping, lambda_function)
    lambda_wrapper.delete_function(lambda_function)
