import os
import csv
import time
import sys
import json
import threading
from datetime import datetime
import requests
from dotenv import load_dotenv

IP_ADDRESS = ''
PORT = ''
TERMINAL_ID = 'user'
USER_ID = 'user'


def find_eft_files(directory):
    """Retrieve .eft files from the specified directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.eft')]


def read_csv(filename):
    """Read CSV file and return list of dictionaries."""
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_file_content(file_path):
    """Load file content as bytes."""
    with open(file_path, 'rb') as file:
        return file.read()


def submit_job(nistBytes):
    # Submit job with NIST.
    submission_url = f'http://{IP_ADDRESS}:{PORT}/mbis-rest/v1/jobs/submit?terminalId={TERMINAL_ID}&userId={USER_ID}'
    headers = {'Content-Type': 'application/octet-stream'}
    params = {'terminalId': {TERMINAL_ID}, 'userId': {USER_ID}}
    response = requests.post(submission_url, headers=headers,
                             params=params, data=nistBytes)

    # log result
    if response.status_code == 200:
        job_id = response.json().get('jobId')

    log_results(log_folder, submission_summary, test_result, '')

    # return job_id or blank
    return job_id


def monitor_job(test_info, url, terminal_id, user_id):
    """Monitor the job state by periodically checking its status."""
    params = {'terminalId': terminal_id, 'userId': user_id}
    while True:
        response = requests.get(
            f"{url}/{test_info.job_id}/histories", params=params)
        if response.status_code == 200:
            data = response.json()
            # Update the test_info based on the status
            if data['status'] == 'Completed':
                test_info.update_status('Completed')
                print(test_info)
                break
            elif data['status'] == 'Failed':
                test_info.update_status('Failed')
                print(test_info)
                break
        else:
            test_info.update_status('Error checking status')
            print(test_info)
            break
        time.sleep(20)  # Check every 20 seconds


def thread_monitor_job(test_info, url, terminal_id, user_id):
    """Thread wrapper for monitor_job."""
    thread = threading.Thread(target=monitor_job, args=(
        test_info, url, terminal_id, user_id))
    thread.start()
    return thread


def append_api_call(log_folder, endpoint, response_code, additional_info=''):
    """Specifically log each API call for detailed tracking."""
    with open(os.path.join(log_folder, 'APICallsSummary.txt'), 'a') as file:
        log_entry = json.dumps({
            'endpoint': endpoint,
            'response_code': response_code,
            'additional_info': additional_info
        }, indent=4)
        file.write(log_entry + '\n')
        file.flush()  # Immediate update to log file


def main():
    curr_dir = os.getcwd()
    files_directory = f'{curr_dir}\\nist_files'
    csv_file = f'{curr_dir}\\test-cases.CSV'
    load_dotenv()

    ip_address = os.getenv('IP_ADDRESS')
    port = os.getenv('PORT')

    eft_files = find_eft_files(files_directory)
    csv_data = read_csv(csv_file)

    print("Loaded CSV data:", csv_data[:5])  # Print first 5 entries to check

    numEftFiles = len(eft_files)
    print(
        f"Submitting {numEftFiles} NISTS files for auto validation. Enter Y to proceed.")

    # Get user input
    user_input = input()

    # Check user input and proceed or exit
    if user_input.strip().upper() == 'Y':
        print("Proceeding with submission...")
        # Add your logic here to proceed with the submission
    else:
        print("Exiting program.")
        sys.exit()  # Exit the program if the user does not enter 'Y'

    # Set up logging structure
    startTimeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Register all test_case objects from cvs test cases/nist files

    #  Note: Only load one Nist into memory at a time.
    jobs = []

    for file_path in eft_files:

        file_content = load_file_content(file_path)
        response = submit_job(file_content)

    # Example setup, replace with your actual job submission and monitoring
    for i in range(5):  # Suppose you have 5 jobs
        file_content = load_file_content(f'path_to_file_{i}.eft')
        response = submit_job(file_content, submission_url)
        if response.status_code == 200:
            job_id = response.json().get('jobId')
            test_info = TestInfo(
                test_name=f"Test {i}", job_id=job_id, expected_result="No Errors")
            # Start monitoring this job in a separate thread
            job_thread = thread_monitor_job(test_info, submission_url, 'user', 'user')
            jobs.append(job_thread)

    # Wait for all threads to complete
    for job in jobs:
        job.join()


if __name__ == "__main__":
    main()
