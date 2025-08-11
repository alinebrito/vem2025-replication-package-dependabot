import boto3

# Dynamo Tables
PULL_REQUEST_DATA_TABLE = 'PullRequestDataTable'
REPOSITORY_DATA_TABLE = 'RepositoryDataTable'
CURRENT_CURSOR_TABLE = 'CurrentCursorTable'
LOCK_TABLE = 'LockTable'

# Init DynamoDB
dynamodb = boto3.resource('dynamodb', 'us-east-2')

pull_request_table = dynamodb.Table(PULL_REQUEST_DATA_TABLE)
repository_table = dynamodb.Table(REPOSITORY_DATA_TABLE)
current_cursor_table = dynamodb.Table(CURRENT_CURSOR_TABLE)
lock_table = dynamodb.Table(LOCK_TABLE)