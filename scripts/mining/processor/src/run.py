import csv
import os
from datetime import datetime
from scripts.config import aws_config as aws
from scripts.config import gcp_config as gcp
from scripts.data import data_analyst

DATA_DUMP_BUCKET_NAME = 'margareth-data-dump'
GCP_BIG_QUERY_CONSUME_BUCKET_NAME = 'gcp-big-query-consume'
METRICS_BUCKET_NAME = 'margareth-metrics-storage'
TABLE_NAME = 'PullRequestDataTable'
ECS_CLUSTER_NAME = 'cluster'
GCP_CONSUME_FILE_NAME = '/tmp/raw_data.csv'


def create_csv(data):
    current_date = datetime.now().strftime("%d-%m-%Y")
    csv_file_name = f'/tmp/{current_date}.csv'

    with open(csv_file_name, mode='w', newline='', encoding="utf-8") as file:
        if len(data) > 0:
            csv_writer = csv.DictWriter(file, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)
    return csv_file_name


def execute_lambda():
    print(f"Started {datetime.now().time()}")

    # Kill ECS running task
    aws.kill_running_mining_tasks(ECS_CLUSTER_NAME)
    print("Cleared cluster tasks")

    # Fetch all data from Dynamo
    data = aws.fetch_all_data(TABLE_NAME)
    print(f"Fetched all {len(data)} pull requests")

    # Create CSV dump file
    csv_file = create_csv(data)
    print("Created csv file")

    # Calculate metrics file
    metrics_file = data_analyst.process_metrics(csv_file)
    print('Processed metrics file')

    # Upload metrics file to S3 metrics dump
    aws.upload_to_s3(metrics_file, METRICS_BUCKET_NAME)
    print("Uploaded metrics file file to S3")

    # Upload metrics data to Google spreadsheet
    gcp.upload_data_to_spreadsheet(metrics_file, 'Metrics Data')
    print('Uploaded calculated metrics to spreadsheets')

    # Upload dump to S3 dump bucket
    aws.upload_to_s3(csv_file, DATA_DUMP_BUCKET_NAME)
    print("Uploaded raw data dump file to S3")

    # Rename dump file to GCP pattern
    os.rename(csv_file, GCP_CONSUME_FILE_NAME)
    csv_file = GCP_CONSUME_FILE_NAME
    print("Renamed dump file to GCP consume format")

    # Upload dump to S3 GCP bucket
    aws.upload_to_s3(csv_file, GCP_BIG_QUERY_CONSUME_BUCKET_NAME)
    print("Uploaded raw data to GCP consume bucket")

    print(f"Finished {datetime.now().time()}")

execute_lambda()
