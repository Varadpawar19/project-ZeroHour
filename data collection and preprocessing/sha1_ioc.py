import requests
import base64
import json

# Your VirusTotal API key
API_KEY = '88d5aece2717697491737c84e1b33fc5da1ba55017c6a307a55ec8db420ff843'
BASE_URL = 'https://www.virustotal.com/api/v3/'

# Function to get a file report using its hash (SHA256, MD5, SHA1)
def get_file_report(file_hash):
    url = f'{BASE_URL}files/{file_hash}'
    headers = {'x-apikey': API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching file report for hash {file_hash}: {response.status_code}")
        print("Response:", response.text)  # Print response body for debugging
        return None

# Function to save combined data to a single JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Main function to scrape and save all reports in a single JSON file
def main():
    # The specific hash you want to query
    file_hash = "94488f214b165512d2fc0438a581f5c9e3bd4d4c"
    
    # Initialize a dictionary to hold all reports
    combined_reports = {}

    # Get file report and add to combined_reports dictionary
    file_report = get_file_report(file_hash)
    if file_report:
        combined_reports['file_report'] = file_report

    # Save all reports in a single JSON file
    save_to_json(combined_reports, 'combined_reports.json')
    print("All reports saved to 'combined_reports.json'")

# Execute the main function
if __name__ == "__main__":
    main()
