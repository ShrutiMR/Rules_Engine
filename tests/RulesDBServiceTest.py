import sys

from Utils import Utils
from RulesDBService import *
import unittest


class RulesDBServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.testing = True

    def setUp(self):
        # Create a mock for Utils
        self.utils_mock = Utils()
        self.service = RulesDBService("rules_engine_db/RulesFile.csv", self.utils_mock)
        self.client = self.app.test_client()

    def testCreateRuleAlreadyExists(self):
        try:
            rule_data = {
                    "name": "incomeRule", 
                    "condition": [
                        {
                        "key": "income",
                        "constraints": "<",
                        "value": 10000
                        }
                    ],
                    "action": "initial_state"
                }
            resp_name = rule_data["name"]
            response = self.service.createRule(json.dumps(rule_data))
            expected_msg = f"Rule with name '{resp_name}' already exists."
            self.assertEqual(str(response), expected_msg)
        except ValueError as ve:
            expected_msg = f"Rule with name '{resp_name}' already exists."
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)


    def testUpdateRuleDoesNotExist(self):
        try:
            rule_id = '4'
            rule_data = {
                    "name": "incomeRule", 
                    "condition": [
                        {
                        "key": "income",
                        "constraints": "<",
                        "value": 10000
                        }
                    ],
                    "action": "initial_state"
                }

            response = self.service.updateRule(rule_id, json.dumps(rule_data))
            expected_msg = f"Rule id - {rule_id} does not exist!"
            self.assertEqual(str(response), expected_msg)
        except ValueError as ve:
            expected_msg = f"Rule id - {rule_id} does not exist!"
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)

    def testGetRule(self):
        try:
            rule_id = '1'
            response = self.service.getRule(rule_id)
            expected_msg = ['1', 'ageRule', "[{'key': 'age', 'constraints': '<', 'value': 100}]", 'initial_state']
            self.assertEqual(response, expected_msg)
        except ValueError as ve:
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)

    def testDeleteRuleDoesNotExist(self):
        try:
            rule_id = '5'
            response = self.service.deleteRule(rule_id)
            expected_msg = f"Rule id - {rule_id} does not exist!"
            self.assertEqual(str(response), expected_msg)
        except ValueError as ve:
            expected_msg = f"Rule id - {rule_id} does not exist!"
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)

if __name__ == '__main__':
    unittest.main()