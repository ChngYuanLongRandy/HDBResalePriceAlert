from flask import Flask, request, jsonify, render_template, send_from_directory
from services import hdbService
from services.dbService import create_tables, add_email, get_emails
import yaml
import sqlite3


app = Flask(__name__)
app.config['DATABASE'] = 'HDBResaleAlertPriceEmails.db'
config_path = "app/config/config.yaml"


create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config/<path:filename>')
def serve_config(filename):
    return send_from_directory('config', filename)

@app.route('/submit', methods=['POST'])
def submit():

    print("Submit request sent")

    with open(config_path, 'r') as yaml_file:
        configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

    params = configData
    print(params["params"])

    try:
        data = request.get_json()

        print(f"data from user {request.get_json()}")

        print(f"flatType : {data['flatType']}")
        print(f"streetName : {data['streetName']}")
        print(f"blkNumberFrom : {data['blkNumberFrom']}")
        print(f"blkNumberTo : {data['blkNumberTo']}")

        params["params"]['flat_type_val'] = data['flatType']
        params["params"]['street_val'] = data['streetName']
        params["params"]['blk_from_val'] = data['blkNumberFrom']
        params["params"]['blk_to_val'] = data['blkNumberTo']

        print(f"Params {params["params"]} after retreiving from user")

        df = hdbService.get_results(params["params"], params["headers_street"], "df")
        print(f"Results in dataframe format : {df}")
        json_results = {
            'columns': df.columns.tolist(),  # Convert columns to a list
            'data': df.values.tolist(),      # Convert data to a nested list
        }

        return jsonify({'message': 'Submission successful', 'data': json_results['data'], 'columns': json_results['columns']}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to add a user
@app.route('/register', methods=['POST'])
def register():
    try:

        input_params = {}

        data = request.get_json()
        input_params["email"] = data['email']
        input_params['flat_type_val'] = data['flatType']
        input_params["street_val"] = data['streetName']
        input_params["blk_from_val"] = data['blkNumberFrom']
        input_params['blk_to_val'] = data['blkNumberTo']

        existingEmails= get_emails()
        print(existingEmails)

        # Check if the email is already registered
        if input_params["email"] in existingEmails:
            return jsonify({'error': 'Email is already registered'}), 400

        else:
            # Do something with the email (e.g., store it, process it)
            # For demonstration purposes, we are just adding it to a set
            add_email(input_params)

            return jsonify({'message': 'Registration successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)