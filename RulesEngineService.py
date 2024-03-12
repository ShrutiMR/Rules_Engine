import json
import csv
from flask import Flask, request, jsonify
from Utils import *
from Customer import *


app = Flask(__name__)

class RulesEngine:

    def __init__(self, csv_file_path, utils):
        self.csv_file_path = csv_file_path
        self.utils = utils

    def formatInput(self, input_data):
        format_input = json.loads(input_data)
        customer_info = Customer(format_input['customer']['name'], format_input['customer']['state'])
        format_input_list = list(format_input.keys())
        return self.evaluateRule(format_input[format_input_list[0]], format_input[format_input_list[1]], customer_info)

    def performAction(self, req_action, rule_condition, customer_info):
        req_action_parts = req_action.split()
        req_action_type = req_action_parts[0]

        if req_action_type == 'initial_state':
            new_state = 'accept_state'
            customer_info.set_state(new_state)
            transition_msg = f"State transition: {customer_info.name} -> {new_state}"
            print(f"State transition: {customer_info.name} -> {new_state}")

    def evaluateRule(self, rule_name, rule_condition, customer_info):
        existing_rows = self.utils.getExistingRows(self.csv_file_path)
        rule_exists, req_row = self.utils.checkIfRuleExists(existing_rows, None, rule_name)

        print(rule_exists, req_row)
        if not rule_exists:
            raise ValueError(f"Rule name - {rule_name} does not exist!")

        req_condition = existing_rows[req_row][2]
        req_action = existing_rows[req_row][3]

        prev_state = customer_info.state
        if self.utils.checkConditions(rule_condition, req_condition):
            self.performAction(req_action, rule_condition, customer_info)
            msg = 'Rule satisfied'
            return msg, f"State transition of {customer_info.name}: {prev_state} -> {customer_info.state}"
        else:
            new_state = 'reject_state'
            customer_info.set_state(new_state)
            msg = 'Rule not satisfied'
            return msg, f"State transition of {customer_info.name}: {prev_state} -> {customer_info.state}"


rule_engine = RulesEngine("rules_engine_db/RulesFile.csv", Utils())

@app.route('/rules-engine', methods=['GET'])
def evaluate_rule():
    try:
        input_data = request.get_json()
        res, state_change_msg = rule_engine.formatInput(input_data)
        return json.dumps({'status': 'ok', 'message': 'Rule engine success!', 'result': res, 'customer info': state_change_msg}), 200

    except ValueError as ve:
        return json.dumps({'error': str(ve)}), 400

    except Exception as e:
        return json.dumps({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)