import unittest
from Utils import Utils
from RulesEngineService import *
from Customer import *

class RulesEngineServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.testing = True

    def setUp(self):
        # Create a mock for Utils
        self.utils_mock = Utils()
        self.service = RulesEngineService("rules_engine_db/RulesFile.csv", self.utils_mock)
        self.client = self.app.test_client()

    def testEvaluateRuleDoesNotExist(self):
        try:
            rule_name = 'assetsRule'
            rule_condition = 'income = 500'
            customer_info = Customer('John', 'initial_state')

            response = self.service.evaluateRule(rule_name, rule_condition, customer_info)
            expected_msg = f"Rule name - {rule_name} does not exist!"
            self.assertEqual(str(response), expected_msg)
        except ValueError as ve:
            expected_msg = f"Rule name - {rule_name} does not exist!"
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)

    def testEvaluateRuleExists(self):
        try:
            rule_name = 'incomeRule'
            rule_condition = 'income = 5000'
            customer_info = Customer('Caleb', 'initial_state')

            response = self.service.evaluateRule(rule_name, rule_condition, customer_info)
            expected_msg = "('Rule satisfied', 'State transition of Caleb: initial_state -> accept_state')"
            self.assertEqual(str(response), expected_msg)
        except ValueError as ve:
            self.assertEqual(str(ve), expected_msg)
        except Exception as e:
            self.assertEqual(str(e), expected_msg)

if __name__ == '__main__':
    unittest.main()