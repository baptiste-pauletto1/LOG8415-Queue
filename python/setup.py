import logging
import boto3
from python.sns_wrapper import SimpleNotificationService
from python.sqs_wrapper import SimpleQueueService


ACCOUNT_ID = ['866658200244']
logger = logging.getLogger(__name__)


def create_resources():

    return boto3.resource('sns'), boto3.resource('sqs')

## TODO : Faire une fonction setup et une fonction clean

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    sns_resource, sqs_resource = create_resources()

    # attributes_sns = {'FifoTopic': 'true', 'ContentBasedDeduplication': 'true'}
    # attributes_sqs = {'FifoQueue': 'true', 'ContentBasedDeduplication': 'true'}
    attributes_sns = {}
    attributes_sqs = {}

    # Instantiating our wrappers
    sns = SimpleNotificationService(sns_resource)
    sqs = SimpleQueueService(sqs_resource)

    topic = sns.create_topic("testWrapper", attributes_sns)
    topics = sns.list_topics()

    queue = sqs.create_queue("testWrapperQueue", attributes_sqs)
    policy = sqs.generate_policy(queue, topic)
    sqs.set_attributes(queue, {'Policy': policy})

    subscription = sns.subscribe(topic, queue.attributes.get("QueueArn"))

    sns.publish_message(topic, "salut", {"coucou": "1"})
    sns.publish_message(topic, "salut", {"coucou": "1"})
    sns.publish_message(topic, "salut", {"coucou": "1"})
    sns.publish_message(topic, "salut", {"coucou": "1"})
    sns.publish_message(topic, "salut", {"coucou": "1"})
    messages = sqs.receive_messages(queue)
    print(messages)

    sns.delete_topic(topic)
    sqs.delete_queue(queue)



