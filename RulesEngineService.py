import json
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

class RuleEngine:

    def __init__(self, csv_file_path):
        self.csv_file_path = "rules_engine_db/RulesFile.csv"

    def format_input(self, input_data):
        format_input = json.loads(input_data)
        customer_info = Customer(format_input['customer']['name'], format_input['customer']['state'])
        if 'income' in format_input:
            return self.evaluate_rule(format_input['name'], format_input['income'], customer_info)
        elif 'age' in format_input:
            return self.evaluate_rule(format_input['name'], format_input['age'], customer_info)

    def check_conditions(self, rule_condition, req_condition):
        req_condition = req_condition.split(' ')
        operator = req_condition[1]
        threshold = int(req_condition[2])

        if operator == '>':
            if rule_condition > threshold:
                return True
            else:
                return False
        elif operator == '<':
            if rule_condition < threshold:
                return True
            else:
                return False
        elif operator == '==':
            if rule_condition == threshold:
                return True
            else:
                return False
        
        return False
    
    def perform_action(self, req_action, rule_condition, customer_info):
        req_action_parts = req_action.split()
        req_action_type = req_action_parts[0]

        if req_action_type == 'initial_state':
            new_state = 'transition_state'
            customer_info.set_state(new_state)
            transition_msg = f"State transition: {customer_info.name} -> {new_state}"
            print(f"State transition: {customer_info.name} -> {new_state}")


    def evaluate_rule(self, rule_name, rule_condition, customer_info):
        existing_rows = []
        with open(self.csv_file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_rows = list(csv_reader)

        req_condition = ''
        req_action = ''
        for row in existing_rows:
            if row[1] == rule_name:
                req_condition = row[2]
                req_action = row[3]
                break
        
        prev_state = customer_info.state
        if self.check_conditions(rule_condition, req_condition):
            self.perform_action(req_action, rule_condition, customer_info)
            return 'Rule satisfied', f"State transition of {customer_info.name}: {prev_state} -> {customer_info.state}"
        else:
            return 'Rule not satisfied', f"State transition of {customer_info.name}: {prev_state} -> {customer_info.state}"

class Customer:
    def __init__(self, name, state='new_state') -> None:
        self.name = name
        self.state = state

    def set_state(self, new_state):
        self.state = new_state

rule_engine = RuleEngine("rules_engine_db/RulesFile.csv")

@app.route('/rules-engine', methods=['GET'])
def evaluate_rule():
    input_data = request.get_json()
    res, transition_msg = rule_engine.format_input(input_data)
    return jsonify({'status': 'ok', 'message': 'Rule engine success!', 'result': res, 'transition': transition_msg}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)