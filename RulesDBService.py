import json
import csv
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

class RulesDBService:
    def __init__(self) -> None:
        pass

    def createRule(self, json_input):
        format_rule = json.loads(json_input)

        condition_rule = format_rule["condition"].split(' ')
        csv_file_path = "rules_engine_db\RulesFile.csv"

        existing_rows = []
        with open(csv_file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            existing_rows = list(csv_reader)
        csv_row = [len(existing_rows) + 1, format_rule["name"], format_rule["condition"], format_rule["action"]]

        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(csv_row)

        print(f"The rule has been appended to {csv_file_path}.")

    def updateRule(self, json_input):
        print('Update rule')

    def getRule(self, json_input):
        print('Get rule')

    def deleteRule(self, json_input):
        print('Delete rule')

rules_service = RulesDBService()

#API endpoint for health check
@app.route('/rules', methods=['GET'])
def check_api():
    # print('Health check Success!')
    return jsonify({'status': 'ok', 'message': 'Health check success!'}), 200

# API endpoint for creating a rule
@app.route('/rules/create', methods=['POST'])
def create_rule():
    try:
        rule_data = request.json
        rules_service.createRule(rule_data)
        return jsonify({'message': 'Rule created successfully'}), 201
    except Exception as e:
        traceback.print_exc() #to log for exception details
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9001)


