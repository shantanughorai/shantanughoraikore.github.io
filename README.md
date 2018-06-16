# Data Driven API automation framework:

This framework is developed for automating the test cases for testing the typicode APIs. The framework is designed using Python3
and uses Requests, CSV and JSON modules.

# Setup:
1. Clone the repo in your local machine
2. Install Python3
3. Install requests module using command "pip install requests"

# Framework:
The framework takes "testCases.csv" file as input. The structure of the "testCases.csv" file is as follows:
1. 1st row contains the Methods/Verbs available in typicode viz: List, Show, Delete, Filter, Create, Update a resource
2. 2nd row contains the Resource name on which the desired operation needs to be done viz: Posts, Albums, Photos, Comments and ToDos

So for e.g. the entry Create,Posts tests whether a post can be created successfully or not using the create method listed by typicode.
Methods Filter, Update, Delete and Show expect the argument in the following format which can be space separated parameter in 2nd row:
Filter,<Resource> <FilterField> <Filter value>
Update,<Resource> <Resource id> <Update value> --- Update currently handles just updating "Title" of the "Posts". Other resources are currently not handled.
Delete,<Resource> <Resource id>
Show,<Resource><Resource id>

To execute the test cases from command prompt (in Windows) or terminal (in Mac or Linux) type in the command: python apiMain.py
Once the execution is complete, the test results are generated in Results.csv file and can be viewed which test cases passed and which ones failed.

# Deviations from REST principles
1. Typicode allows to update a resource using POST method when it actually should have thorwn protocol not suppoetd
2. Proper status codes are not sent if a resource is missing or if a resource is not found. It sends back 200 OK response code
3. If the content type is different from JSON, its just throws back entire error trace instead of proper message
