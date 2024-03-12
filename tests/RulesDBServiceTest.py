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
        rule_data = {
            "name":"incomeRule", 
            "condition":"income > 8000", 
            "action":"initial_state"
        }
        
        response = self.service.createRule(json.dumps(rule_data))
        resp_name = rule_data['name']
        expected_msg = f"Rule with name '{resp_name}' already exists."
        self.assertEqual(str(response), expected_msg)


    def testUpdateRuleDoesNotExist(self):
        rule_id = '4'
        rule_data = {
            "name":"incomeRule",
            "condition":"income < 10000",
            "action":"initial_state"
        }

        response = self.service.updateRule(rule_id, json.dumps(rule_data))
        expected_msg = f"Rule id - {rule_id} does not exist!"
        self.assertEqual(str(response), expected_msg)

    def testGetRule(self):
        rule_id = '1'
        
        response = self.service.getRule(rule_id)
        expected_msg = f"['1', 'ageRule', 'age < 100', 'initial_state']"
        self.assertEqual(str(response), expected_msg)

    def testDeleteRuleDoesNotExist(self):
        rule_id = '5'

        response = self.service.deleteRule(rule_id)
        expected_msg = f"Rule id - {rule_id} does not exist!"
        self.assertEqual(str(response), expected_msg)

if __name__ == '__main__':
    unittest.main()