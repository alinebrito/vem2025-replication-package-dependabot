import requests
import time
import os

# dotenv_path = Path('../.env')
# load_dotenv(dotenv_path)
#
GITHUB_TOKEN = os.getenv('GITHUB_API_TOKEN')
GITHUB_API_URL = 'https://api.github.com/graphql'
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

max_retries = 4 # 6
retry_delay = 10 # 60
long_retry_delay = 30 # 300


def dispatch_request(query, variables):
    retries = 0

    while retries < max_retries:
        try:
            response = requests.post(
                GITHUB_API_URL,
                json={
                    "query": query,
                    "variables": variables
                },
                headers=GITHUB_HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                retries += 1
                time.sleep(retry_delay)
                continue

            retries = 0
            return response

        except requests.exceptions.Timeout as e:
            print(f"Timeout error, retrying after {retry_delay} seconds... Attempt {retries + 1}/{max_retries}")
            print(e)
            retries += 1
            time.sleep(retry_delay)

        except Exception as e:
            print(f"Error in request, retrying after 1 minute... Attempt {retries}/{max_retries}")
            print(e)
            retries += 1
            time.sleep(retry_delay)

        if retries == (max_retries - 1):
            print(f"Reached {max_retries} retries, waiting for {long_retry_delay} seconds before retrying...")
            time.sleep(long_retry_delay)

    print(f"Failed request after {max_retries} attempts")
    return None


def read_query(query_file):
    with open(query_file, 'r') as file:
        return file.read()


def run_query(query_file, variables, data_function):
    query = read_query(query_file)
    response = dispatch_request(query, variables)

    if response is None:
        return None
    else:
        data = response.json()
        data_function(data)
        return data
