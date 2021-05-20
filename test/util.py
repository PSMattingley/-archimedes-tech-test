import os
import json

TEST_DIR = os.path.join(os.path.dirname(__file__), 'test_data')


def load_test_data(filename):
    """
    Loads json data from a given test file and returns data dictionary

    :param filename: Name of the test file in the test_data directory

    :return: Data dictionary containing list of dicts
    """
    test_file = os.path.join(TEST_DIR, filename)
    with open(test_file) as tf:
        json_data = json.load(tf)
    return json_data['data']
