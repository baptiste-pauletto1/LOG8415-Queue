import json

def lambda_handler(event, context):
    # TODO implement
    print(f"Mon petit event : {event}")

    return {
        'statusCode': 200,
        'body': event
    }

