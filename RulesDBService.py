import json
import csv
from flask import Flask, request, jsonify
import traceback
from Utils import *

app = Flask(__name__)

class RulesDBService:
    def __init__(self, csv_file_path, utils) -> None:
        self.csv_file_path = csv_file_path
        self.utils = utils

    def createRule(self, json_input):
        try:
            format_rule = json.loads(json_input)
            existing_rows = self.utils.getExistingRows(self.csv_file_path)
            
            index_val = 1
            if len(existing_rows) > 1:
                index_val = int(existing_rows[-1][0]) + 1

            for row in existing_rows:
                if row[1] == format_rule["name"]:
                    raise ValueError(f"Rule with name '{format_rule['name']}' already exists.")
            
            csv_row = [index_val, format_rule["name"], format_rule["condition"], format_rule["action"]]

            with open(self.csv_file_path, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(csv_row)
                    
        except ValueError as ve:
            raise ValueError(str(ve))
        
        except Exception as e:
            raise Exception(str(e))

    def updateRule(self, rule_id, json_input):
        try:
            format_rule = json.loads(json_input)
            if rule_id == '0':
                raise ValueError(f"Wrong Rule id provided. Rule id starts from 1!!")
            existing_rows = self.utils.getExistingRows(self.csv_file_path)

            check_if_row_exists = False
            row_index = 0
            for i, row in enumerate(existing_rows):
                if row[0] == rule_id:
                    check_if_row_exists = True
                    row_index = i
                if row[0] != rule_id and row[1] == format_rule["name"]:
                    raise ValueError(f"Rule with name '{format_rule['name']}' already exists.")

            if not check_if_row_exists:
                raise ValueError(f"Rule id - {rule_id} does not exist!")

            existing_rows[row_index] = [rule_id, format_rule["name"], format_rule["condition"], format_rule["action"]]
            with open(self.csv_file_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(existing_rows)

        except ValueError as ve:
            raise ValueError(str(ve))
        
        except Exception as e:
            raise Exception(str(e))

    def getRule(self, rule_id):
        try:
            existing_rows = self.utils.getExistingRows(self.csv_file_path)
            if rule_id == '0':
                raise ValueError(f"Wrong Rule id provided. Rule id starts from 1!!")

            row_exists, req_row = self.utils.checkIfRuleExists(existing_rows, rule_id)
            if not row_exists:
                raise ValueError(f"Rule id - {rule_id} does not exist!")
            
            print(req_row)
            return existing_rows[req_row]
        
        except ValueError as ve:
            raise ValueError(str(ve))
        
        except Exception as e:
            raise Exception(str(e))

    def deleteRule(self, rule_id):
        try:
            existing_rows = self.utils.getExistingRows(self.csv_file_path)
            if rule_id == '0':
                raise ValueError(f"Wrong Rule id provided. Rule id starts from 1!!")

            row_exists, req_row = self.utils.checkIfRuleExists(existing_rows, rule_id)
            if not row_exists:
                raise ValueError(f"Rule id - {rule_id} does not exist!")

            del existing_rows[req_row]
            with open(self.csv_file_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(existing_rows)
        except ValueError as ve:
            raise ValueError(str(ve))
        
        except Exception as e:
            raise Exception(str(e))

rules_service = RulesDBService("rules_engine_db/RulesFile.csv", Utils())

#API endpoint for health check
@app.route('/rules', methods=['GET'])
def check_api():
    return jsonify({'status': 'ok', 'message': 'Health check success!'}), 200

# API endpoint for creating a rule
@app.route('/rules/create', methods=['POST'])
def create_rule():
    try:
        rule_insert_data = request.get_json()
        rules_service.createRule(rule_insert_data)
        return json.dumps({'message': 'Rule created successfully'}), 201
    except ValueError as ve:
        return json.dumps({'error': str(ve)}), 400
    except Exception as e:
        traceback.print_exc() #logs for exception details
        return json.dumps({'error': str(e)}), 500

# API endpoint for updating a rule
@app.route('/rules/update/<rule_id>', methods=['PUT'])
def update_rule(rule_id):
    try:
        rule_update_data = request.get_json()
        rules_service.updateRule(rule_id, rule_update_data)
        return json.dumps({'message': 'Rule updated successfully'}), 200
    except ValueError as ve:
        return json.dumps({'error': str(ve)}), 400
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

# API endpoint for getting a rule
@app.route('/rules/get/<rule_id>', methods=['GET'])
def get_rule(rule_id):
    try:
        rule = rules_service.getRule(rule_id)
        return json.dumps({'rule_id': rule[0], 'rule_name': rule[1], 'condition': rule[2], 'action': rule[3]}), 200
    except ValueError as ve:
        return json.dumps({'error': str(ve)}), 400
    except Exception as e:
        return json.dumps({'error': str(e)}), 500
    
# API endpoint for deleting a rule
@app.route('/rules/delete/<rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    try:
        rules_service.deleteRule(rule_id)
        return json.dumps({'message': 'Rule deleted successfully'}), 200
    except ValueError as ve:
        return json.dumps({'error': str(ve)}), 400
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9001)


