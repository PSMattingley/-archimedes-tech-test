from unittest import TestCase
import pandas as pd
import os

from src.main import create_operator_lookup, create_calls_df, generate_report


class TestCalls(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report_file = 'report.csv'

    def test_op_lookup(self):
        op_lookup = create_operator_lookup(test=True)
        self.assertEqual(op_lookup['1000'], 'Vodafone')
        self.assertEqual(op_lookup['2000'], 'EE')

    def test_calls_df(self):
        calls_df = create_calls_df(test=True)
        self.assertEqual(len(calls_df), 2)
        self.assertEqual(calls_df.iloc[0]['date'], '2019-10-12')
        self.assertEqual(calls_df.iloc[-1]['riskScore'], 0)

    def test_report(self):
        generate_report(test=True)
        report = pd.read_csv('report.csv')
        self.assertEqual(len(report), 2)
        self.assertEqual(report.iloc[0]['operator'], 'Vodafone')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.report_file)
