from flask import Flask, request, jsonify, render_template
import requests
import logging

app = Flask(__name__)

rules_db_url = 'http://127.0.0.1:9001/rules'
rules_engine_url = 'http://127.0.0.1:9002/rules-engine'

@app.route('/process', methods=['GET'])
def home():
    return render_template('index.html')

def send_request_to_rules_db(json_input_data, user_input, rule_id=None):
    try:
        # Make HTTP POST request to RulesDBService
        if user_input == 'create':
            response = requests.post(f'{rules_db_url}/{user_input}', json=json_input_data)
        elif user_input == 'update':
            response = requests.put(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)
        elif user_input == 'delete':
            response = requests.delete(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)
        elif user_input == 'get':
            response = requests.get(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)

        result = response.json()
        return result

    except requests.RequestException as e:
        return {'error': str(e)}
    
def send_request_to_rules_engine(eval_data=None):
    try:
        response = requests.get(f'{rules_engine_url}', json=eval_data)
        result = response.json()
        print(result)
        return result

    except requests.RequestException as e:
        return {'error': str(e)}
    

@app.route('/process', methods=['POST'])
def process_rules():
    try:
        # Get input data from the form
        user_input = request.form.get('action', '').lower()
        json_input_data = request.form.get('rule_data', '')
        rule_id = None
        
        if user_input in ['update', 'delete', 'get']:
            rule_id = request.form.get('rule_id')

        # Call the Front-End Service to process rules
        response = send_request_to_rules_db(json_input_data, user_input, int(rule_id) if rule_id is not None else None)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/evaluate', methods=['POST'])
def evaluate_rules():
    try:
        eval_data = request.form.get('eval_data')
        print('eval_data -- ', eval_data)
        response = send_request_to_rules_engine(eval_data)
        print('response -- ', response)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)