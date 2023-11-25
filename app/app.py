from flask import Flask, request, jsonify, render_template, send_from_directory
from services import hdbService
import yaml

app = Flask(__name__)
config_path = "app/config/config.yaml"

# Sample data storage (replace this with a database in a real application)
submitted_data = []
registered_emails = set("asd@asd.com")

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

        # hdbService.params_hdb['flatType_val'] = data['flatType']
        # hdbService.params_hdb['street_val'] = data['streetName']
        # hdbService.params_hdb['blk_from_val'] = data['blkNumberFrom']
        # hdbService.params_hdb['blk_to_val'] = data['blkNumberTo']

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

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email']

        # Check if the email is already registered
        if email in registered_emails:
            return jsonify({'error': 'Email is already registered'}), 400

        # Do something with the email (e.g., store it, process it)
        # For demonstration purposes, we are just adding it to a set
        registered_emails.add(email)

        return jsonify({'message': 'Registration successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)