import boto3


def create_resources():

    return boto3.resource('sns'), boto3.resource('sqs')


def create_topic(sns_resource, topic_name, attributes):

    topic = sns_resource.create_topic(Name=topic_name, Attributes=attributes)

    return topic.attributes.get('TopicArn')


def create_queue(sqs_resource, queue_name, attributes):

    # Create the queue. This returns an SQS.Queue instance
    queue = sqs_resource.create_queue(QueueName=queue_name, Attributes=attributes)

    return queue.attributes.get('QueueArn')


if __name__ == "__main__":
    sns, sqs = create_resources()

    attributes_sns = {'FifoTopic': 'true', 'ContentBasedDeduplication': 'true'}
    attributes_sqs = {'FifoQueue': 'true', 'ContentBasedDeduplication': 'true'}

    topic_arn = create_topic(sns, "testTopic.fifo", attributes_sns)
    queue_arn = create_queue(sqs, "premiereQueueB.fifo", attributes_sqs)
    print(queue_arn)
