from flask import Flask, request, jsonify, render_template
import requests
import logging

app = Flask(__name__)

rules_db_url = 'http://127.0.0.1:9001/rules'

@app.route('/process', methods=['GET'])
def home():
    return render_template('index.html')

def send_request_to_rules_db(json_input_data, user_input):
    try:
        # Make HTTP POST request to RulesDBService
        response = requests.post(f'{rules_db_url}/{user_input}', json=json_input_data)

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

        # Call the Front-End Service to process rules
        response = send_request_to_rules_db(json_input_data, user_input)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)