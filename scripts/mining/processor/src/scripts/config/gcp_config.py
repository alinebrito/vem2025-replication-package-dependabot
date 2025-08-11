from googleapiclient.discovery import build
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import csv

SPREADSHEET_ID = "1vyi7A_MzXC1u1GVeW_TevKN4Xl59O5sPk4o9wHZcAtA"




def get_google_spreedshets_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '../gcp-credentials.json',
        'https://www.googleapis.com/auth/spreadsheets'
    )

    credential = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials,
        'https://www.googleapis.com/auth/spreadsheets'
    )

    if not credential or credential.invalid:
        print('Unable to authenticate using service account key.')
        return None

    http_auth = credential.authorize(httplib2.Http())
    service = build("sheets", "v4", http=http_auth)
    return service.spreadsheets()


sheets = get_google_spreedshets_service()


def upload_data_to_spreadsheet(csv_file, range, batch_upload=False):
    sheets.values().clear(spreadsheetId=SPREADSHEET_ID, range=range).execute()
    print('Cleared previous sheets values')

    if batch_upload:
        start_row = 1
        batch_size = 10000

        for batch in read_csv_in_batches(csv_file, batch_size):
            upload_batch_to_sheets(batch, range)
            start_row += batch_size
            print(f"Uploaded rows {start_row - batch_size} to {start_row - 1}")
    else:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            values = list(csv_reader)

        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            valueInputOption="RAW",
            body={
                'values': values
            }
        ).execute()


def read_csv_in_batches(file_path, batch_size):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        batch = []

        for row in csv_reader:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch


def upload_batch_to_sheets(current_batch, range):
    sheets.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={
            "values": current_batch
        }
    ).execute()
