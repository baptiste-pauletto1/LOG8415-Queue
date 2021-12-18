from botocore.client import logger
from botocore.exceptions import ClientError


class Lambda:

    def __init__(self, resource):
        self.lambda_resource = resource

    @staticmethod
    def generate_bytecode(path):
        """
        Transform a zipfile to bytecode understood by boto3 and AWS.

        :param path: Path to the zipped code for the lambda function
        :return: Code bytes that can be interpreted by AWS Lambda
        """
        with open(path, 'rb') as lambda_code:
            bytes_lambda = lambda_code.read()
        return bytes_lambda

    def create_function(self, name):
        """
        Create a new lambda function.
        Since we're only using a single type of lambda function for our analysis,
        most of the content is static.

        :param name: Lambda function name
        :return: The newly created lambda_function
        """

        try:
            lambda_function = self.lambda_resource.create_function(FunctionName=name,
                                                                   Description='Basic Lambda function to support tests',
                                                                   Runtime='python3.9',
                                                                   # Role created to allow Lambda to write on DynamoDB
                                                                   # and generate CloudWatch metrics
                                                                   Role='arn:aws:iam::866658200244:role/LambdaDynamoDB',
                                                                   Handler='lambda_function.lambda_handler',
                                                                   Publish=True,
                                                                   Code={
                                                                       'ZipFile': self.generate_bytecode('../lambda-code/my-deployment-package.zip')
                                                                   }
                                                                   )
            logger.info("Created lambda function %s with ARN %s.", name, lambda_function.get('FunctionArn'))
        except ClientError:
            logger.exception("Couldn't create the lambda function %s.", name)
            raise
        else:
            return lambda_function

    def add_trigger(self, source, function):
        """
        Add a mapping to allow SQS messages to be treated by our Lambda function

        :param source: the SQS queue that will provide messages
        :param function: the lambda function that will treat those messages
        :return: Mapping response.
        """
        try:
            mapping = self.lambda_resource.create_event_source_mapping(EventSourceArn=source.attributes.get('QueueArn'),
                                                                       FunctionName=function.get('FunctionArn'),
                                                                       Enabled=True,
                                                                       # Could be changed for further analysis (BS > 1).
                                                                       BatchSize=1
                                                                       )
            logger.info("Added trigger from %s to lambda : %s.", source.attributes.get('QueueArn'),
                        function.get('FunctionArn'))
        except ClientError:
            logger.exception("Couldn't add trigger from %s on lambda :%s.", source.attributes.get('QueueArn'),
                             function.get('FunctionArn'))
            raise
        else:
            return mapping

    def delete_trigger(self, trigger, function):
        """
        Deletes a trigger from a lambda function

        :param trigger: Trigger to be deleted
        :param function: Function concerned by the trigger
        """
        try:
            self.lambda_resource.delete_event_source_mapping(UUID=trigger.get('UUID'))
            logger.info("Deleted trigger from lambda : %s.", function.get('FunctionArn'))
        except ClientError:
            logger.exception("Couldn't delete trigger on lambda %s.", function.get('FunctionArn'))
            raise

    def delete_function(self, function):
        """
        Deletes a lambda function

        :param function : Function to be deleted
        """
        try:
            self.lambda_resource.delete_function(FunctionName=function.get('FunctionArn'))
            logger.info("Deleted Lambda function successfully.")
        except ClientError:
            logger.exception("Couldn't delete function %s.",  function.get('FunctionArn'))
            raise
