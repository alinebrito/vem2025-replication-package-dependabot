import boto3
import os
import time
import psutil

ecs_client = boto3.client('ecs', 'us-east-2')
dynamodb = boto3.resource('dynamodb', 'us-east-2')
s3 = boto3.client('s3')


def upload_to_s3(file, bucket_name):
    s3.upload_file(file, bucket_name, os.path.basename(file))


def fetch_all_data(table_name):
    process = psutil.Process()
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        start_time = time.time()
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        end_time = time.time()

        duration = end_time - start_time
        duration_formatted = f"{duration:.3f}"  # Format to 3 decimal places
        memory_usage = process.memory_info().rss / (1024 * 1024)

        data.extend(response['Items'])

        print(f"Fetched {len(data)} items so far [{duration_formatted}s] [{memory_usage:.2f} MB]")

    return data


def kill_running_mining_tasks(cluster_name):
    try:
        tasks = ecs_client.list_tasks(
            cluster=cluster_name,
            desiredStatus='RUNNING'
        )

        task_arns = tasks['taskArns']

        print(f"There are {len(task_arns)} running...")

        if not task_arns:
            print("No tasks running")
            return

        for task_arn in task_arns:
            ecs_client.stop_task(
                cluster=cluster_name,
                task=task_arn,
                reason="Scheduled stop by AWS Lambda function"
            )

            print(f"Stopped task: {task_arn}")

        print("Stopped all tasks")
    except Exception as e:
        print(f"Error when stopping tasks {str(e)}")
