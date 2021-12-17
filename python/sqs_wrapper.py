from botocore.client import logger
from botocore.exceptions import ClientError

class SimpleQueueService:

    def __init__(self, resource):
        self.sqs_resource = resource

    def create_queue(self, name, attributes):
        """
        Creates a SQS queue using the attributes passed by

        :param name: The name of the queue to create.
        :param attributes: The attributes of the queue (used for FIFO especially)
        :return: The newly created queue.
        """
        try:
            queue = self.sqs_resource.create_queue(QueueName=name, Attributes=attributes)
            logger.info("Created queue %s with ARN %s.", name, queue.attributes.get("QueueArn"))
        except ClientError:
            logger.exception("Couldn't create queue %s.", name)
            raise
        else:
            return queue

    @staticmethod
    def set_attributes(queue, attributes):
        """
        Add permissions to a queue (like receiving message).

        :param queue: The queue where permissions will be added
        :param name: Name of the permissions added
        :param topic_arn: topic allowed to publish to this queue
        :param actions: Actions added to the specified queue

        """
        try:
            queue.set_attributes(Attributes=attributes)
            logger.info("Setting attributes to queue %s : %s.", queue.attributes.get("QueueArn"), attributes)
        except ClientError:
            logger.exception("Couldn't set to queue %s attributes %s.",
                             queue.attributes.get("QueueArn"), attributes)
            raise

    @staticmethod
    def receive_messages(queue):
        """
        Receive a list of message for a specified queue

        :param queue: Queue
        :return: List of received messages
        """

        try:
            messages = queue.receive_messages(AttributeNames=['All'], WaitTimeSeconds=15)
        except ClientError:
            logger.exception("Couldn't retrieve message from queue %s.", queue.arn)
            raise
        else:
            return messages

    @staticmethod
    def purge_queue(queue):
        """
        Removes all message inside a queue.

        :param queue: Queue where all messages will be deleted
        """
        try:
            queue.purge()
            logger.info("Purged queue %s.", queue.arn)
        except ClientError:
            logger.exception("Couldn't purge queue %s.", queue.arn)
            raise

    @staticmethod
    def generate_policy(queue, topic):
        """
        Generate an appropriate policy document to allow our SQS to receive messages from SNS

        :param queue: Queue that will receive the right to get messages from the topic
        :param topic: Topic that will be allowed to send messages to the queue
        :return: Policy to allow the queue to receive messages from the topic
        """
        new_policy = """{{
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"MyPolicy",
              "Effect":"Allow",
              "Principal" : {{"AWS" : "*"}},
              "Action":"SQS:SendMessage",
              "Resource": "{}",
              "Condition":{{
                "ArnEquals":{{
                  "aws:SourceArn": "{}"
                }}
              }}
            }}
          ]
        }}""".format(queue.attributes.get("QueueArn"), topic.arn)

        return new_policy

    @staticmethod
    def delete_queue(queue):
        """
        Delete the specified queue.
        All messages in the queue will also be deleted

        :param queue: Queue to be deleted
        """
        try:
            queue.delete()
            logger.info("Deleted queue successfully.")
        except ClientError:
            logger.exception("Couldn't delete queue %s.", queue.attributes.get('QueueArn'))
            raise

