import os
import json

PROJ_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJ_DIR, 'data')
TEST_DIR = os.path.join(PROJ_DIR, 'test', 'test_data')


def load_data(filename, test=False):
    """
    Loads json data from a given data file and returns data dictionary.

    By default loads from the /data directory. If test is set to true will load from test/test_data.

    :param filename: Name of the json file in the data directory
    :param test: Whether to load from the test data directory [default - false]

    :return: Data dictionary containing list of dicts
    """
    if test:
        file_dir = TEST_DIR
    else:
        file_dir = DATA_DIR
    test_file = os.path.join(file_dir, filename)
    with open(test_file) as tf:
        json_data = json.load(tf)
    return json_data['data']


def map_prefix_to_operator(prefix, operator_lookup):
    """
    Retrieves the operator name or 'Unknown' for the given prefix

    :param prefix: Operator prefix in call number e.g. 2000
    :param operator_lookup: Dictionary containing prefix -> operator map

    :return: Operator Name or Unknown
    """
    try:
        return operator_lookup[prefix]
    except KeyError:
        return 'Unknown'


