import ast
import csv


def write_data(array):
    csv_file_path = 'results/results.csv'

    parsed_data = [ast.literal_eval(item) if isinstance(item, str) else item for item in array]

    headers = parsed_data[0].keys()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(parsed_data)
