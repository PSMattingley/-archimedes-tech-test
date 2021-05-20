from unittest import TestCase

from src.util import map_prefix_to_operator


class TestCalls(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.operator_lookup = {'Unknown': 'Unknown',
                               "1000": "Vodafone",
                               "2000": "EE"}

    def test_unknown_operator(self):
        self.assertEqual(map_prefix_to_operator('Unknown', self.operator_lookup), 'Unknown')

    def test_known_operator(self):
        self.assertEqual(map_prefix_to_operator('2000', self.operator_lookup), 'EE')

    def test_missing_operator(self):
        self.assertEqual(map_prefix_to_operator('3000', self.operator_lookup), 'Unknown')

