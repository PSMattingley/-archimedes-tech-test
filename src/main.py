from src.util import load_data, map_prefix_to_operator
from src.operators import Operator
from src.calls import Call

import pandas as pd


def create_operator_lookup(test=False):
    """
    Generates a lookup for operators based on prefix by reading from the supplied operators file.

    :param: Whether to run with test data

    :return: A dictionary of operator code to operator
    """
    operator_lookup = {'Unknown': 'Unknown'}
    operators = [Operator(**op_dict) for op_dict in load_data('operators.json', test=test)]
    for op in operators:
        operator_lookup[op.attributes.prefix] = op.attributes.operator
    return operator_lookup


def create_calls_df(test=False):
    """
    Creates a dataframe containing all the information from the calls input file required for the
    final report ordered by call date.

    :param: Whether to run with test data

    :return: Pandas dataframe containing id, short date, number, operator-prefix and processed risk score
    """
    calls_df = pd.DataFrame([Call(**call_dict).get_report_dict() for call_dict in load_data('calls.json', test=test)])
    return calls_df.sort_values(by='date')


def generate_report(report_name='report', test=False):
    """
    Main function used to generate the output report

    :param: Whether to run with test data

    :return: Void, outputs report to local csv
    """
    # Create a lookup for operator based on code
    operator_lookup = create_operator_lookup(test=test)

    # Create calls dataframe containing call data for the report
    calls_df = create_calls_df(test=test)

    # Map operator prefix to operator name
    calls_df['operator'] = calls_df['operator_prefix'].apply(lambda x: map_prefix_to_operator(x, operator_lookup))

    # Print main report to file
    calls_df = calls_df[['id', 'date', 'number', 'operator', 'riskScore']]
    calls_df.to_csv(f'{report_name}.csv', index=False)


if __name__ == "__main__":
    generate_report()

