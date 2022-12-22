import pytest
import docker
import requests
import random
import json
import time


@pytest.fixture(scope="class")
def container():
    """ A fixture for setting up a Docker container for testing.
        This fixture creates a Docker client,
        Starts a container in the background with the specified image and ports,
        And stores the container object. It also sleeps for 4 seconds to allow the container to start up. """
    client = docker.from_env()
    client.containers.run(
        "api_reverse_string",
        ports={5000: 5000},
        detach=True,
        name="api_reverse_string"
    )
    time.sleep(4)

@pytest.fixture(scope="class")
def global_value():
    """
    Returns a dictionary containing global values used in the application.
    """
    return {"base_url": "http://localhost:5000",
            "status_code_message": "Status code should be 200, but instead got:",
            "error_message_for_one_word": 'Please provid more than 1 word'
    }

@pytest.mark.usefixtures("container")
class TestReverseApi:

    @pytest.mark.parametrize('execution_number', range(5))
    def test_reverse_sanity(self, container, execution_number, global_value, record_property):
        """Test the reverse endpoint of an API for sainty.
        Args: 
            self (object): The object itself.
            container (list): A list containing the test results.
            execution_number (int): The execution number of the test.
            global_value (dict): A dictionary containing global values.
        Returns: None """
        random_list_of_words = self.choose_random_words()
        excepted_result = self.reverse_list_into_str(random_list_of_words)
        response = requests.get(f"{global_value.get('base_url')}/reverse?in={random_list_of_words[0]} {random_list_of_words[1]} {random_list_of_words[2]}", timeout=3)
        assert response.status_code, f"{global_value.get('status_code_message')} {response.status_code}"
        return_text = json.loads(response.text)
        assert return_text.get("result") == excepted_result, f"The API response should be {excepted_result} but actualy {return_text.get('result')}"

    def test_reverse_negative(self, container, global_value, record_property):
        """
        Test the reverse API endpoint with a string of one word, which should return an error.
        """
        response = requests.get(f"{global_value.get('base_url')}/reverse?in=justoneword", timeout=3)
        assert response.status_code, f"{global_value.get('status_code_message')} {response.status_code}"
        return_text = json.loads(response.text)
        assert return_text.get("error") == global_value.get('error_message_for_one_word')

    def test_restore(self, container, global_value):
        """ Use the reverse endpoint of an API to reverse a string or list.
            Then, use the restore endpoint of the same API to restore the original string or list.
            Check the status of both requests to ensure that they were successful.
            Finally, validate that the response from the reverse endpoint is equal to the response from the restore endpoint,
            indicating that the reversal and restoration processes were successful. """
        random_list_of_words = self.choose_random_words()
        result = self.reverse_list_into_str(random_list_of_words)
        response_of_reverse = requests.get(f"{global_value.get('base_url')}/reverse?in={random_list_of_words[0]} {random_list_of_words[1]} {random_list_of_words[2]}", timeout=3)
        assert response_of_reverse.status_code, f"{global_value.get('status_code_message')} {response_of_reverse.status_code}"
        response_of_restore = requests.get(f"{global_value.get('base_url')}/restore", timeout=3)
        assert response_of_restore.status_code, f"{global_value.get('status_code_message')} {response_of_restore.status_code}"
        response_of_reverse = json.loads(response_of_reverse.text)
        response_of_restore = json.loads(response_of_restore.text)
        assert response_of_reverse.get("result") == response_of_restore.get("result")

    @classmethod
    def teardown_class(cls):
        """ Tears down the class by stopping and removing the Docker container for the reverse string API."""
        client = docker.from_env()
        container = client.containers.get("api_reverse_string")
        container.stop()
        container.remove()

##################HELP METHOD#################################################

    def choose_random_words(self):
        """Returns a list of three randomly chosen words from a predefined list of words. """
        words = ['cat', 'dog', 'bat', 'rat', 'cow', 'pig', 'fox'] 
        return [random.choice(words) for _ in range(3)]

    def reverse_list_into_str(self, random_list_of_words)->list:
        """
        Reverses a list of words into a string.
        Parameters:
        random_list_of_words (list): The list of words to be reversed.
        Returns:
        str: The reversed list of words as a string.
        """
        my_string = ' '.join(random_list_of_words)
        split_str = my_string.split()
        return " ".join(reversed(split_str))
    

