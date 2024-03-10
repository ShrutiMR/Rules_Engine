import json
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

class Customer:

    def meetsThresholdIncome(self, rule_name, income):
        csv_file_path = "rules_engine_db/RulesFile.csv"

        existing_rows = []
        with open(csv_file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_rows = list(csv_reader)

        req_condition = ''
        req_action = ''
        for row in existing_rows:
            if row[1] == rule_name:
                req_condition = row[2]
                req_action = row[3]
                break

        req_condition = req_condition.split(' ')
        operator = req_condition[1]
        threshold = int(req_condition[2])
        if operator == '>':
            if income > threshold:
                return req_action
            else:
                return 'Invalid'
        elif operator == '<':
            if income < threshold:
                return req_action
            else:
                return 'Invalid'
        elif operator == '==':
            if income == threshold:
                return req_action
            else:
                return 'Invalid'

        return 'Not found!'


customer = Customer()

@app.route('/rules-engine', methods=['GET'])
def evaluate_rule():
    input_data = request.get_json()
    format_input = json.loads(input_data)
    res = customer.meetsThresholdIncome(format_input['name'], int(format_input['income']))
    return jsonify({'status': 'ok', 'message': 'Rule engine success!', 'result': res}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)