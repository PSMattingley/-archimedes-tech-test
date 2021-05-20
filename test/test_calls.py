from unittest import TestCase
from pydantic import ValidationError

from src.calls import Call
from src.util import load_data


class TestCalls(TestCase):

    @classmethod
    def setUpClass(cls):
        test_data = load_data('calls.json', test=True)
        cls.calls = [Call(**call_dict) for call_dict in test_data]

    def test_read_calls(self):
        self.assertEqual(len(self.calls), 2)

    def test_call_fields(self):
        exp_fields = ['type', 'id', 'attributes']
        for c in self.calls:
            attr = c.__fields__
            for field in exp_fields:
                self.assertTrue(field in attr)

    def test_type(self):
        for c in self.calls:
            self.assertEqual(c.type, "call")

    def test_id(self):
        self.assertEqual(self.calls[0].id, "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b")

    def test_attributes(self):
        attr = self.calls[0].attributes
        self.assertEqual(attr.date, "2020-10-12T07:20:50Z")
        self.assertEqual(attr.riskScore, 0.431513435443)
        self.assertEqual(attr.number, "+44123456789")
        self.assertTrue(attr.greenList)
        self.assertFalse(attr.redList)

    def test_invalid_risk_score(self):
        with self.assertRaises(ValidationError):
            Call(attributes={'riskScore': 1.5})

    def test_invalid_date(self):
        with self.assertRaises(ValidationError):
            Call(attributes={'date': "2020-10-12"})

    def test_final_risk_score_list(self):
        self.assertEqual(self.calls[0].get_final_risk_score(), 0)
        self.assertEqual(self.calls[1].get_final_risk_score(), 1)

    def test_final_risk_score_not_list(self):
        rs_call = Call(attributes={'riskScore': 0.123,
                                   'greenList': False,
                                   'redList': False})
        self.assertEqual(rs_call.get_final_risk_score(), 0.2)





