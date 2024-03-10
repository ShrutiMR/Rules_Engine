from flask import Flask, request, jsonify, render_template
import requests
import logging

app = Flask(__name__)

rules_db_url = 'http://127.0.0.1:9001/rules'

@app.route('/process', methods=['GET'])
def home():
    return render_template('index.html')

def send_request_to_rules_db(json_input_data, user_input, rule_id=None):
    try:
        # Make HTTP POST request to RulesDBService
        print(user_input)
        print(json_input_data)
        if user_input == 'create':
            response = requests.post(f'{rules_db_url}/{user_input}', json=json_input_data)
        elif user_input == 'update':
            print('enter')
            response = requests.put(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)
        elif user_input == 'delete':
            response = requests.delete(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)
        elif user_input == 'get':
            response = requests.get(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)

        # Check the response status
        if response.ok:
            result = response.json()
            return result
        else:
            logging.error(f'Error calling RulesDBService. Status code: {response.status_code}')
            return {'error': 'Error calling RulesDBService.'}

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
        # response = requests.get(f'{rules_db_url}/{user_input}/{rule_id}', json=json_input_data)
        return jsonify({'status': 'ok', 'message': 'Health check success!'}), 200
        # return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)