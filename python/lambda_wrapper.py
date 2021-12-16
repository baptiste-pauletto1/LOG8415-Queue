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
        except ClientError:
            logger.exception("Couldn't create the lambda function.")
            raise
        else:
            return lambda_function

    @staticmethod
    def delete_function(function):
        """
        Deletes a lambda function

        :param function : Function to be deleted
        """
        try:
            function.delete()
            logger.info("Deleted function %s.", function.arn)
        except ClientError:
            logger.exception("Couldn't delete function %s.", function.arn)
            raise
