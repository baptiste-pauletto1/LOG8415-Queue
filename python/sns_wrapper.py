from botocore.client import logger
from botocore.exceptions import ClientError


class SimpleNotificationService:

    def __init__(self, resource):
        self.sns_resource = resource

    def create_topic(self, name, attributes):
        """
        Creates a notification topic using the attributes passed by

        :param name: The name of the topic to create.
        :param attributes: The attributes of the topic (used for FIFO especially)
        :return: The newly created topic.
        """
        try:
            topic = self.sns_resource.create_topic(Name=name, Attributes=attributes)
            logger.info("Created topic %s with ARN %s.", name, topic.arn)
        except ClientError:
            logger.exception("Couldn't create topic %s.", name)
            raise
        else:
            return topic

    @staticmethod
    def subscribe(topic, queue_arn):
        """
        Subscribes an endpoint to the topic.
        We do not specify a particular protocol or endpoint since we will be only using
        SQS and Lambda functions to handle our experiments.

        :param topic: The topic to subscribe to.
        :param queue_arn: The ARN of the SQS queue that will receive the messages.
        :return: The newly added subscription.
        """
        try:
            subscription = topic.subscribe(
                Protocol='sqs', Endpoint=queue_arn, ReturnSubscriptionArn=True)
            logger.info("Subscribed the queue %s to topic %s.", queue_arn, topic.arn)
        except ClientError:
            logger.exception(
                "Couldn't subscribe the queue %s to topic %s.", queue_arn, topic.arn)
            raise
        else:
            return subscription

    @staticmethod
    def publish_message(topic, message, attributes):
        """
        Comment extracted from AWS SDK boto3 doc :
        Publishes a message, with attributes, to a topic. Subscriptions can be filtered
        based on message attributes so that a subscription receives messages only
        when specified attributes are present.

        :param topic: The topic to publish to.
        :param message: The message to publish.
        :param attributes: The key-value attributes to attach to the message. Values
                           must be either `str` or `bytes`.
        :return: The ID of the message.
        """
        try:
            att_dict = {}
            for key, value in attributes.items():
                if isinstance(value, str):
                    att_dict[key] = {'DataType': 'String', 'StringValue': value}
                elif isinstance(value, bytes):
                    att_dict[key] = {'DataType': 'Binary', 'BinaryValue': value}
            response = topic.publish(Message=message, MessageAttributes=att_dict)
            message_id = response['MessageId']
            logger.info(
                "Published message with attributes %s to topic %s.", attributes,
                topic.arn)
        except ClientError:
            logger.exception("Couldn't publish message to topic %s.", topic.arn)
            raise
        else:
            return message_id

    def list_topics(self):
        """
        Lists topics for the current account.

        :return: An iterator that yields the topics.
        """
        try:
            topics_iter = self.sns_resource.topics.all()
            logger.info("Got topics.")
        except ClientError:
            logger.exception("Couldn't get topics.")
            raise
        else:
            return topics_iter

    def list_subscriptions(self, topic=None):
        """
        Lists subscriptions for the current account, optionally limited to a
        specific topic.

        :param topic: When specified, only subscriptions to this topic are returned.
        :return: An iterator that yields the subscriptions.
        """
        try:
            if topic is None:
                subs_iter = self.sns_resource.subscriptions.all()
            else:
                subs_iter = topic.subscriptions.all()
            logger.info("Got subscriptions.")
        except ClientError:
            logger.exception("Couldn't get subscriptions.")
            raise
        else:
            return subs_iter

    @staticmethod
    def delete_topic(topic):
        """
        Deletes a topic. All subscriptions to the topic are also deleted.

        :param topic : Topic to be deleted
        """
        try:
            topic.delete()
            logger.info("Deleted topic %s.", topic.arn)
        except ClientError:
            logger.exception("Couldn't delete topic %s.", topic.arn)
            raise

