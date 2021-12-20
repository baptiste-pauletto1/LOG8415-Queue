from datetime import datetime, timedelta
import boto3
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def structure_data_query(id_query, namespace, metric_name, dimensions, period, stat):
    query = {'Id': id_query, 'MetricStat': {
        'Metric': {
            'Namespace': namespace, 'MetricName': metric_name, 'Dimensions': dimensions},
        'Period': period, 'Stat': stat}}
    return query


def get_values(client, metric_queries, start_time, end_time):
    response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=start_time,
        EndTime=end_time)
    return response


if __name__ == "__main__":
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

    # Defining AWS namespace
    namespace_lambda = 'AWS/Lambda'

    # Metric names
    metric_duration = 'Duration'
    metric_invocation = 'Invocations'
    metric_concurrent = 'ConcurrentExecutions'

    # Stat types
    stat_duration = 'Average'
    stat_invocation = 'Sum'
    stat_concurrent = 'Average'

    # Period for the analysis
    period = 300

    # Metric dimensions (our three scenarios for each metric)
    dimensions_lambda_base = [
        {'Name': 'FunctionName', 'Value': 'lambdabase'}
    ]
    dimensions_lambda_SC1 = [
        {'Name': 'FunctionName', 'Value': 'lambdaSC1'}
    ]
    dimensions_lambda_SC2 = [
        {'Name': 'FunctionName', 'Value': 'lambdaSC2'}
    ]

    # Formatting queries into the shape required by AWS
    query_duration_base = structure_data_query("duration_query_base", namespace_lambda,
                                               metric_duration, dimensions_lambda_base, period, stat_duration)
    query_invocation_base = structure_data_query("invocation_query_base", namespace_lambda,
                                                 metric_invocation, dimensions_lambda_base, period, stat_invocation)
    query_concurrent_base = structure_data_query("concurrent_query_base", namespace_lambda,
                                                 metric_concurrent, dimensions_lambda_base, period, stat_concurrent)

    query_duration_SC1 = structure_data_query("duration_query_SC1", namespace_lambda,
                                              metric_duration, dimensions_lambda_SC1, period, stat_duration)
    query_invocation_SC1 = structure_data_query("invocation_query_SC1", namespace_lambda,
                                                metric_invocation, dimensions_lambda_SC1, period, stat_invocation)
    query_concurrent_SC1 = structure_data_query("concurrent_query_SC1", namespace_lambda,
                                                metric_concurrent, dimensions_lambda_SC1, period, stat_concurrent)

    query_duration_SC2 = structure_data_query("duration_query_SC2", namespace_lambda,
                                              metric_duration, dimensions_lambda_SC2, period, stat_duration)
    query_invocation_SC2 = structure_data_query("invocation_query_SC2", namespace_lambda,
                                                metric_invocation, dimensions_lambda_SC2, period, stat_invocation)
    query_concurrent_SC2 = structure_data_query("concurrent_query_SC2", namespace_lambda,
                                                metric_concurrent, dimensions_lambda_SC2, period, stat_concurrent)

    queries = [query_duration_base, query_invocation_base, query_concurrent_base,
               query_duration_SC1, query_invocation_SC1, query_concurrent_SC1,
               query_duration_SC2, query_invocation_SC2, query_concurrent_SC2]

    # Calling AWS Cloudwatch from now - 30 mins in the past.
    values = get_values(cloudwatch, queries, datetime.now(), datetime.now() - timedelta(hours=0, minutes=30))

    # Formatting values
    values_concurrent = [values['MetricDataResults'][2]['Values'][0], values['MetricDataResults'][5]['Values'][0],
                         values['MetricDataResults'][8]['Values'][0]]

    # Turning values to dataframe
    df_values_concurrent = pd.DataFrame([values_concurrent], columns=["Baseline", "Standard Queue", "FIFO Queue"])

    # Use SNS and matplotlib to save the graph
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(data=df_values_concurrent, palette='Blues_d')
    ax.set(xlabel='Scenario', ylabel='Number of concurrent executions (mean)')
    plt.savefig("../metrics_result/concurrent_comparison.png", bbox_inches='tight')

    # Formatting values
    values_duration = [values['MetricDataResults'][0]['Values'][0], values['MetricDataResults'][3]['Values'][0],
                       values['MetricDataResults'][6]['Values'][0]]

    # Turning values to dataframe
    df_values_duration = pd.DataFrame([values_duration], columns=["Baseline", "Standard Queue", "FIFO Queue"])

    # Use SNS and matplotlib to save the graph
    ax = sns.barplot(data=df_values_duration, palette='Blues_d')
    ax.set(xlabel='Scenario', ylabel='Duration (seconds) (mean)')
    plt.savefig("../metrics_result/duration_comparison.png", bbox_inches='tight')

    # Formatting values
    values_invocation = [values['MetricDataResults'][1]['Values'][0], values['MetricDataResults'][4]['Values'][0],
                         values['MetricDataResults'][7]['Values'][0]]

    # Turning values to dataframe
    df_values_invocation = pd.DataFrame([values_invocation], columns=["Baseline", "Standard Queue", "FIFO Queue"])

    # Use SNS and matplotlib to save the graph
    ax = sns.barplot(data=df_values_invocation, palette='Blues_d')
    ax.set(xlabel='Scenario', ylabel='Number of invocations (sum)')
    plt.savefig("../metrics_result/invocation_comparison.png", bbox_inches='tight')




