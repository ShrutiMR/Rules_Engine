import json
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

class Customer:
    pass

#API endpoint for health check
@app.route('/validate', methods=['GET'])
def check_api():
    return jsonify({'status': 'ok', 'message': 'Health check success!'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)