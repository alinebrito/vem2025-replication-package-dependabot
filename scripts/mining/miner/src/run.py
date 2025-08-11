import time
import argparse
import uuid
from datetime import datetime
from scripts.data import data_retriever
from scripts.config import aws_config
from scripts.utils import lock_utils as lock

# Constants
PULL_REQUESTS_PER_PAGE = 20
REPROCESSING_MODE = False

CURRENT_CURSOR_ID = 'CurrentCursor'

# GraphQL Queries
pull_request_query = 'query/pull_request_query.graphql'
repository_query = 'query/repository_query.graphql'


def pull_requests_data_function(data):
    pull_requests = data['data']['repository']['pullRequests']['nodes']

    for pull_request in pull_requests:
        print(pull_request)

        if pull_request['author'] is not None:
            item = {
                'ObjectId': str(uuid.uuid4()),
                'RepositoryId': data['data']['repository']['id'],
                'RepositoryName': data['data']['repository']['name'],
                'OwnerName': data['data']['repository']['owner']['login'],
                'Author': pull_request['author']['login'],
                'State': pull_request['state'],
                'CreatedAt': str(pull_request['createdAt']),
                'ClosedAt': str(pull_request['closedAt']),
                'UpdatedAt': str(pull_request['updatedAt']),
                'PublishedAt': str(pull_request['publishedAt']),
                'MergedAt': str(pull_request['mergedAt']),
                'LastEditedAt': str(pull_request['lastEditedAt']),
                'ChangedFiles': str(pull_request['changedFiles']),
                'Deletions': str(pull_request['deletions']),
                'Additions': str(pull_request['additions']),
                'Title': str(pull_request['title']),
                'ParticipantsCount': pull_request['participants']['totalCount'],
                'CommitsCount': pull_request['commits']['totalCount'],
                'ReviewsCount': pull_request['reviews']['totalCount'],
                'StargazersCount': data['data']['repository']['stargazerCount'],
                'PullRequestsCount': data['data']['repository']['pullRequests']['totalCount'],
                'PrimaryLanguage': data['data']['repository']['primaryLanguage']['name'] if data['data']['repository'].get('primaryLanguage') else None,
            }

            aws_config.pull_request_table.put_item(Item=item)
            print(f"Saved pullRequest data for repository: {data['data']['repository']['name']}")


def fetch_current_cursor():
    try:
        return aws_config.current_cursor_table.get_item(
            Key={'CursorId': CURRENT_CURSOR_ID}
        ).get('Item')
    except Exception:
        print('Failed fetching last cursor id when bypassing')
        return None


def generate_query_variables(repository, bypass):
    if bypass is True:
        print('Bypassing to continue mining from where it left off')

        last_cursor = fetch_current_cursor()

        if last_cursor is not None:
            current_cursor = last_cursor['Cursor']
        else:
            print('Last cursor not found. Marking repository as Failed and moving on to next one')
            change_repository_status(repository['ObjectId'], repository['Index'], 'Failed')
            return None

        variables = {
            'repo_name': repository['Name'],
            'repo_owner': repository['Owner'],
            'pull_request_num': 20,
            'cursor': current_cursor
        }
    else:
        variables = {
            'repo_name': repository['name'],
            'repo_owner': repository['owner']['login'],
            'pull_request_num': 20,
            'cursor': ''
        }

    return variables


def mine_pull_requests(repository, unique_id, index, bypass=False):
    variables = generate_query_variables(repository, bypass)

    if variables is not None:
        while True:
            data = data_retriever.run_query(
                query_file=pull_request_query,
                variables=variables,
                data_function=pull_requests_data_function
            )

            if data is not None:
                variables['cursor'] = data['data']['repository']['pullRequests']['pageInfo']['endCursor']

                aws_config.current_cursor_table.put_item(
                    Item={
                        'CursorId': CURRENT_CURSOR_ID,
                        'Cursor': variables['cursor']
                    })

                if not data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
                    break
            else:
                print('Current repository cursor is broken. Marking repository as Failed and moving on to next one')
                change_repository_status(str(unique_id), index, 'Failed')
                return

        change_repository_status(str(unique_id), index, 'Finished')


def change_repository_status(object_id, index, status):
    aws_config.repository_table.update_item(
        Key={'ObjectId': str(object_id), 'Index': index},
        UpdateExpression="set MiningStatus = :c",
        ExpressionAttributeValues={
            ':c': status
        })


def get_last_repository_inserted():
    print("Fetching last repository inserted...")
    items = aws_config.repository_table.scan()['Items']
    last_item = max(items, key=lambda x: x['Index']) if items else None
    return last_item


def repository_data_function(data):
    for item in data['data']['search']['edges']:
        repository = item['node']

        last_repository = get_last_repository_inserted()
        index = (last_repository['Index'] + 1) if last_repository else 0

        object_id = uuid.uuid4()

        repository_info = {
            'ObjectId': str(object_id),
            'Index': index,
            'Name': repository['name'],
            'Owner': repository['owner']['login'],
            'Stargazers': repository['stargazerCount'],
            'PullRequestsCount': repository['pullRequests']['totalCount'],
            'NextPageCursor': data['data']['search']['pageInfo']['endCursor'],
            'CreatedAt': str(datetime.now()),
            'MiningStatus': 'Skipped' if repository['pullRequests']['totalCount'] > 10000 else 'Mining',
            'PrimaryLanguage': repository['primaryLanguage']['name'] if repository.get('primaryLanguage') else None,
        }

        aws_config.repository_table.put_item(
            Item=repository_info
        )

        if repository_info['MiningStatus'] == 'Mining':
            mine_pull_requests(repository, object_id, index)
        else:
            print('Repository pull requests count is bigger than 10k, skipping and marking as Failed')


def start_execution():
    last_repository = get_last_repository_inserted()

    if last_repository is not None:
        if last_repository['Index'] == 500:
            print("Already mined 500 repos, breaking loop")
            return

        if last_repository['MiningStatus'] == 'Mining':
            print(f"Last execution didnt finish well for repository {last_repository['Name']}")
            mine_pull_requests(last_repository, last_repository['ObjectId'], last_repository['Index'], bypass=True)

    print('Beginning to mine new repository...')

    cursor = last_repository['NextPageCursor'] if last_repository else ''

    variables = {
        'cursor': cursor,
        'num_repos': 1
    }

    data_retriever.run_query(
        query_file=repository_query,
        variables=variables,
        data_function=repository_data_function
    )


def lambda_handler():
    print("Starting lambda...")

    while True:
        if lock.acquire():
            try:
                start_execution()
            finally:
                lock.release()

        else:
            print("Lambda is already running, trying to run again in 1 minute")
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("reprocessing_mode", type=bool, nargs="?", default=False)
    args = parser.parse_args()

    REPROCESSING_MODE = args.reprocessing_mode

    lambda_handler()
