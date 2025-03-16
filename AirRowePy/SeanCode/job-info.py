
class JobInfo:
    def __init__(self, test_name, job_id, expected_result):
        self.test_name = test_name
        self.job_id = job_id
        self.expected_result = expected_result
        self.current_status = "Submitted"  # Initial status

    def update_status(self, new_status):
        self.current_status = new_status

    def __str__(self):
        return (f"Test Name: {self.test_name}\n"
                f"Job ID: {self.job_id}\n"
                f"Expected Result: {self.expected_result}\n"
                f"Current Status: {self.current_status}")