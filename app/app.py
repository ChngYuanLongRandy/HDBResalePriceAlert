from flask import Flask, request, jsonify, render_template, send_from_directory
from services import hdbService
from services.emailService import *
from services.dbService import *
from datetime import datetime
import yaml
import secrets


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

        print(f"Params {params['params']} after retreiving from user")

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
        print("Entering register method")

        input_params = {}

        data = request.get_json()
        input_params["email"] = data['email']
        input_params['flat_type_val'] = data['flatType']
        input_params["street_val"] = data['streetName']
        input_params["blk_from_val"] = data['blkNumberFrom']
        input_params['blk_to_val'] = data['blkNumberTo']

        db= get_emails()
        print("Printing all emails in db")
        emails = []
        for entry in db:
            print(entry["email"])
            emails.append(entry["email"])

        token = secrets.token_urlsafe() + secrets.token_urlsafe()

        # Check if the email is already registered
        if input_params["email"] in emails:
            print("email exists, sending 400 response")
            return jsonify({'error': 'Email is already registered'}), 400

        else:
            add_email(input_params)
            print("attemping to add token ")
            update_email_with_token(input_params, token)
            confirmation_link = "/confirm/" + token
            send_confirmation_email(input_params["email"], confirmation_link)
            print("confirmation email sent, sending 200 response")
            return jsonify({'message': 'Registration successful', 'data': input_params['email']}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Takes all of the email that has been verified and sends them according to what they have specified
@app.route('/testSendEmail', methods=['POST'])
def testSendEmail():
    try:
        print("Entering send email method")

        with open(config_path, 'r') as yaml_file:
            configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

        params = configData
        print(params["params"])

        data = request.get_json()
        datetimeSent = data['formattedTimestamp']
        print(f"datetimeSent is {datetimeSent}")


        # Gathers a list of verified emails
        db= get_emails()
        print("Printing all verified emails in db")
        emails = []
        for entry in db:
            if entry["verified"] == True:
                print(entry["email"])
                emails.append(entry["email"])

        # sorted_emails = {}

        # # Sorts them into identical lists
        # for email in emails:
        print(f"Contents of emails : {emails}")

        for email in emails:
            print(f"Email : {email}")
            email_params = get_email(email)[0] # should only be one result since I'm doing a test
            print(f'Email params : {email_params}')
            print(f"email_params['flatType'] : {email_params['flatType']}")
            print(f"params flat type val : {params['params']['flat_type_val']}")

            params['params']['flat_type_val'] = email_params['flatType']
            print('passed 1')
            params['params']['street_val'] = email_params['streetname']
            print('passed 2')
            params['params']['blk_from_val'] = email_params['blkFrom']
            print('passed 3')
            params['params']['blk_to_val'] = email_params['blkTo']
            print('passed 4')
            print(f"params : {params['params']}")
            df = hdbService.get_results(params['params'], params['headers_street'], 'df')
            print(f"Results in dataframe format : {df}")
            print(f"update datetime of email {email}")
            update_email_with_senddatetime(email, datetimeSent)
            print(f"Before sending email to {email}")
            content = f"Hi. This is the alert for {datetime.now().month}"
            send_email_template(email,content,True, df)

        
        json_results = {
        'emails': emails
        }   

        return jsonify({'message': 'Emails sent', 'data': json_results['emails']}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# confirms the token from the user and sets user's verified to true
@app.route('/confirm/<token>')
def confirm(token):
    try:
        email = get_email_by_token(token)

        print(f'Email found : {email}, setting verified == true')
        update_email_verified_true(email['email'])
        return render_template('confirmationSuccess.html')
    except Exception as ex:
        print(f"Something wrong must have happened as the email was not found")
        return jsonify({'message': str(ex)}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
