import json
import boto3
import pandas
import csv

def write_newline_to_csv(newline, filename, bucket):
    
    try:
        # Catching all variables from the incoming message
        bucket = event.get(bucket)
        key = event.get(key)
        id_customer = event.get(id_customer)
        id_ticket = event.get(id_ticket)
        time = event.get(time)
        
        # Get file from S3 using boto3
        s3 = boto3.client('s3')
        s3_object = s3_client.get_object(Bucket=BUCKET,
                                        Key=KEY)
        
        # Getting the CSV from the bucket
        csv_s3 = response["Body"]
        
        # Turning result into dataframe
        df_s3 = pd.read_csv(csv_s3, index_col = 0)
        
        # Adding the new row 
        df_s3.append([id_customer,id_ticket,time])
        
        # Putting back the csv file on S3
        
        
    except:
        
        return {
            'statusCode': 400,
            'body': 'Error, could not complete the request!'}

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

