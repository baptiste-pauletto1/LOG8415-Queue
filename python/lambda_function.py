import json
import boto3


# Used to unpack data coming from SQS and SNS
def format_input(event):
    data = event['Records'][0]['body']
    data = data.replace("\n", "")
    clean_data = data.replace(" ", "")
    return json.loads(clean_data)


def lambda_handler(event, context):
    try:
        # Formatting input
        body = format_input(event)

        # Getting our event parameters
        table_name = body['MessageAttributes']['table']['Value']
        id_concert = int(body['MessageAttributes']['id_concert']['Value'])
        id_customer = int(body['MessageAttributes']['id_customer']['Value'])
        ticket_class = body['MessageAttributes']['ticket_class']['Value']
        date = body['MessageAttributes']['date']['Value']
        timestamp = body['Timestamp']

        # Getting the dynamoDB resource
        client = boto3.resource('dynamodb')

        # Getting the concerned table
        table = client.Table(table_name)

        # Adding the new entry
        table.put_item(Item={'id_concert': id_concert, 'id_customer': id_customer,
                             'ticket_class': ticket_class, 'date': date, 'timestamp': timestamp})

        return {
            'statusCode': 200,
            'body': json.dumps(f'Entry has conveniently been added to {table_name}')
        }

    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error ! Request was rejected')
        }
