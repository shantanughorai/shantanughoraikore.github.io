# UI Automation using Selenium Webdriver and Python
There are 6 test cases developed for this exercise:
1. To validate the title of the home page of www.wikipedia.org
2. Search an article for which we get the suggestion and verify if "Did you mean" text is present
3. Click the link which comes up for "Did you mean"
4. Verify 20 search results are present on the search result page when the link in TC 3 is clicked
5. Click the first link in TC 4 and validate if article title is present
6. Click the first link in TC 4 and validate if table of contents is present

# Setup
The framework is developed using pytest. In order to runt he tests install the following:
1. Python 3.6
2. Pytest (one can use the follwing command to install pytest: pip install pytest)

# Execution
In order to execute, do the following:
1. Download or clone the repo
2. Open command prompt or terminal
3. Navigate to the directory where the code has been downloaded
4. run the command: pytest -n 6 (6 since we have 6 test cases)

The above command will execute the tests in parallel.
