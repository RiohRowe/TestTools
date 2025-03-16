
I'm making a python program that will do the following to help us automated test cases. There will be hunderds of test cases we need to run and monitor:

Look in a specific folder for existing files with .eft
Read from a CSV file, searching for the filenames in the folder, and gather additional related data, such as descriptions and test expectations.
Loading those files as byte[] objects

Submitting those files to this POST API using a curl like command: http://x.x.x.x:8080/mbis-rest/v1/jobs/submit?terminalId=user&userId=user
It will not submit more than 5 per second.
This will submit a job (workflow) that I want to monitor

Keep track of what jobId (returned form the POST jobs/submit)
Monitor the submitted jobs every aproximately 20 seconds to check on the state using this API request:
http://x.x.x.x:8080/mbis-rest/v1/jobs/<jobID>/histories?terminalId=user&userId=user

if the job has reached a certain history, I want to run assertions on that history and then run additonal checks on results from this api call as well:
http://x.x.x.x:8080/mbis-rest/v1/jobs/<JobId>/params?terminalId=user&userId=user
Once the assertions are finished and the job has reached a certain state, then remove the job from the minitoring queue.


All the while I want to log the results in multiple files all within a certain generated folder structure

> test-run-<timestamp>
 - > SubmissionSummary - This is based on the CVS file and the files submitted
 - > testResultsSummary - This will print the description of the test pulled from the CSV file, the expected criteria for the job, and PASS/FAIL status.
 - > API calls summary - this will log all the API calls and the results of those API calls (e.g. 200, 500, etc, and some of the important data in the responses)


Please give me some boiler plate. Make the python code high quality and easy to maintain.