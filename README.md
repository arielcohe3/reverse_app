# How to run the tests:

# Reverse String API Tests:
This project contains tests for the reverse string API. It uses the Pytest framework, the Docker library, and the Requests library to test the API's endpoints.
***
### Build the flask docker image:
`docker build -t api_reverse_string .`
***
### run the tests:
1. Create virtual env: `python3 -m venv venv`
2. Activate virtual env: `source venv/bin/activate`
3. Install dependencies: `pip3 install requests pytest docker`
4. run the test: `pytest --junitxml=result.xml`
***
### Test Details:

The tests in this project include:

1. test_reverse_sainty: This test sends a request to the /reverse endpoint with a string of 3 randomly chosen words. This test is run 5 times with different random strings.
2. test_reverse_negative: This test sends a request to the /reverse endpoint with a string of one word.
3. test_restore: This test sends a request to the /reverse endpoint with a string of 3 randomly chosen words. It then sends a request to the /restore endpoint. It checks that the response from the /reverse endpoint is equal to the response from the /restore endpoint, indicating that the reversal and restoration processes were successful.
***
### Notes:
* The tests use a fixture called container to start a Docker container in the background with the reverse_string_api image and the 5000 port.
* The tests use a fixture called global_value to store global values that are used throughout the tests, such as the base URL of the API and error messages.
