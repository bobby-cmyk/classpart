import csv

def validate_csv_headers(file_path, expected_headers):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        actual_headers = next(reader, None)  # Read the first row
        print(f"Actual headers: {actual_headers}")
        return actual_headers == expected_headers
