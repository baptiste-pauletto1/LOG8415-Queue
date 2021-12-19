import logging
from datetime import datetime

import boto3
import time


def get_values(client, metric_name, namespace, dimensions, start_time, end_time, statistics):
    response = client.get_metric_statistics(
        MetricName=metric_name,
        Namespace=namespace,
        Dimensions=dimensions,
        Period=60,
        StartTime=start_time,
        EndTime=end_time,
        Statistics=statistics)
    return response


if __name__ == "__main__":
    cloudwatch = boto3.client('cloudwatch')

    dimensions_lambda = [
        {'Name': 'FunctionName', 'Value': 'lambdaSC2'}
    ]

    values = get_values(cloudwatch, 'Invocations', 'AWS/Lambda', dimensions_lambda,
                        datetime(2021, 12, 19, 00, 15), datetime(2021, 12, 19, 00, 25), ['Sum'])

    print(values)
