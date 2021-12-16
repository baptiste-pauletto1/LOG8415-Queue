import json
import boto3


def lambda_handler(event, context):
    try:
        # Getting our event parameters
        table_name = event.get('table')
        id = event.get('id')
        customer = event.get('customer')
        ticket = event.get('ticket')
        time = event.get('time')

        # Getting the dynamoDB resource
        client = boto3.resource('dynamodb')

        # Getting the concerned table
        table = client.Table(table_name)

        # Adding the new entry
        table.put_item(Item={'id': id, 'customer': customer, 'ticket': ticket, 'time': time})

        return {
            'statusCode': 200,
            'body': json.dumps(f'Entry has conveniently been added to {table_name}')
        }

    except:

        return {
            'statusCode': 400,
            'body': json.dumps('Error ! Request was rejected')
        }
