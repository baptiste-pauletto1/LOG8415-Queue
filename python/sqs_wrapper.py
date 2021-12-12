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
            logger.info("Created topic %s with ARN %s.", name, queue.arn)
        except ClientError:
            logger.exception("Couldn't create topic %s.", name)
            raise
        else:
            return queue

    @staticmethod
    def receive_messages(queue):
        """
        Receive a list of message for a specified queue

        :param queue: Queue
        :return: List of received messages
        """

        try:
            messages = queue.receive_messages(AttributeNames=['All'])
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
    def delete_queue(queue):
        """
        Delete the specified queue.
        All messages in the queue will also be deleted

        :param queue: Queue to be deleted
        """
        try:
            queue.delete()
            logger.info("Deleted queue %s.", queue.arn)
        except ClientError:
            logger.exception("Couldn't delete queue %s.", queue.arn)
            raise

