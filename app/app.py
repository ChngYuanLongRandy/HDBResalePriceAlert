from flask import Flask, request, jsonify, render_template
from services import hdbService

app = Flask(__name__)
config_path = "./config/config.yaml"

# Sample data storage (replace this with a database in a real application)
submitted_data = []
registered_emails = set("asd@asd.com")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        flat_type = data['flatType']
        street_name = data['streetName']
        resale_date = data['resaleDate']

        # Do something with the data (e.g., store it, process it)
        # For demonstration purposes, we are just appending it to a list
        submitted_data.append({'flatType': flat_type, 'streetName': street_name, 'resaleDate': resale_date})

        return jsonify({'message': 'Submission successful'}), 200

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