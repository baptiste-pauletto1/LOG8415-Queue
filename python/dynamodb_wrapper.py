from botocore.client import logger
from botocore.exceptions import ClientError


class DynamoDB:

    def __init__(self, resource):
        self.dynamodb_resource = resource

    def create_table(self, name):
        """
        This method creates the table that will support our analysis.
        The structure is stable and represents an example of what could
        be done in this type of project.

        :param name: Name of the table
        :return: The newly created table.
        """
        try:
            table = self.dynamodb_resource.create_table(TableName=name,
                                                        KeySchema=[
                                                            {
                                                                # Partition key (primary one)
                                                                'AttributeName': 'id_concert',
                                                                'KeyType': 'HASH'
                                                            },
                                                            {
                                                                # Sort key (by user)
                                                                'AttributeName': 'id_customer',
                                                                'KeyType': 'RANGE'
                                                            }
                                                        ],
                                                        AttributeDefinitions=[
                                                            {
                                                                # N as attribute type represents Number
                                                                'AttributeName': 'id_concert',
                                                                'AttributeType': 'N'
                                                            },
                                                            {
                                                                'AttributeName': 'id_customer',
                                                                'AttributeType': 'N'
                                                            }
                                                        ],
                                                        ProvisionedThroughput={
                                                            # Small value since we will not read a lot from the table
                                                            'ReadCapacityUnits': 2,
                                                            'WriteCapacityUnits': 10
                                                        }
                                                        )
            logger.info("Created table %s successfully.", name)
        except ClientError:
            logger.exception("Couldn't create table %s", name)
            raise
        else:
            return table

    @staticmethod
    def delete_table(table):
        """
        Delete the specified table.
        All entries in this table are also deleted.

        :param table : Table to be deleted
        """
        try:
            table.delete()
            logger.info("Deleted table %s.", table.name)
        except ClientError:
            logger.exception("Couldn't delete table %s.", table.name)
            raise
