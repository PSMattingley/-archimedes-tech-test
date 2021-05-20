from unittest import TestCase

from src.operators import Operator
from test.util import load_test_data


class TestOperators(TestCase):

    @classmethod
    def setUpClass(cls):
        test_data = load_test_data('operators.json')
        cls.operators = [Operator(**op_dict) for op_dict in test_data]

    def test_read_operators(self):
        self.assertEqual(len(self.operators), 2)

    def test_operator_fields(self):
        exp_fields = ['type', 'id', 'attributes']
        for op in self.operators:
            attr = op.__fields__
            for field in exp_fields:
                self.assertTrue(field in attr)

    def test_type(self):
        for op in self.operators:
            self.assertEqual(op.type, "operator")

    def test_id(self):
        self.assertEqual(self.operators[0].id, "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b")

    def test_attributes(self):
        attr = self.operators[0].attributes
        self.assertEqual(attr.prefix, "1000")
        self.assertEqual(attr.operator, "Vodafone")










