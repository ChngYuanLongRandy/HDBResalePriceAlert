from flask import Flask, request, jsonify, render_template, send_from_directory, redirect
from services import hdbService
from model.SubUser import SubUser
from services.emailService import *
from services.dbService import *
from datetime import datetime
import yaml
import secrets
import os

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
app.config['PORT'] = '3306'
app.config['EMAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
config_path = "app/config/config.yaml"

# Database configuration
app.config['MYSQL_HOST'] = "mysql"  # This should match the service name in Docker Compose
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_ROOT_PASSWORD'] = os.environ.get('MYSQL_ROOT_PASSWORD')
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

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
        new_user = SubUser(data['email'],data['flatType'],data['streetName'],data['blkNumberFrom'],data['blkNumberTo'])
        # input_params["email"] = data['email']
        # input_params['flat_type_val'] = data['flatType']
        # input_params["street_val"] = data['streetName']
        # input_params["blk_from_val"] = data['blkNumberFrom']
        # input_params['blk_to_val'] = data['blkNumberTo']

        users = get_emails()
        print("Printing all emails in db")
        for a_user in users:
            print(a_user.email)

        token = secrets.token_urlsafe() + secrets.token_urlsafe()

        # Check if the params are already in the database:
        print(f"new_user : {new_user}")
        for user in users:
            print(f"user : {user}")
            print(f"email: {new_user.email == user.email}")
            print(f"blkrom: {new_user.blkFrom == user.blkFrom}")
            print(f"blkto: {new_user.blkTo == user.blkTo}")
            print(f"flatype: {new_user.flatType == user.flatType}")
            print(f"streetname: {new_user.streetName == user.streetName}")
            
            if (new_user.email == user.email and
                new_user.blkFrom == user.blkFrom and
                new_user.blkTo == user.blkTo and
                new_user.streetName == user.streetName and
                new_user.flatType == user.flatType):
            # if (new_user == user)
                print("email exists, sending 400 response")
                return jsonify({'error': 'Email is already registered'}), 400

        add_email(new_user)
        print("attemping to add token ")
        update_email_with_token(new_user, token)
        confirmation_link = "/confirm/" + token
        send_confirmation_email(new_user, confirmation_link)
        print("confirmation email sent, sending 200 response")
        return jsonify({'message': 'Registration successful', 'data': new_user.email}), 200

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
        users= get_emails()
        print("Printing all verified emails in db")
        verified_users = []
        for user in users:
            if user.verified == True:
                print(user.email)
                verified_users.append(user)

        # sorted_emails = {}

        # # Sorts them into identical lists
        # for email in emails:
        print(f"Contents of verified_users : {verified_users}")

        for verified_user in verified_users:
            print(f"verified_user : {verified_user}")
            # email_params = get_email(email)
            # print(f'Email params : {email_params}')
            # print(f"email_params['flatType'] : {email_params['flatType']}")
            # print(f"params flat type val : {params['params']['flat_type_val']}")

            # params['params']['flat_type_val'] = email_params['flatType']
            # print('passed 1')
            # params['params']['street_val'] = email_params['streetname']
            # print('passed 2')
            # params['params']['blk_from_val'] = email_params['blkFrom']
            # print('passed 3')
            # params['params']['blk_to_val'] = email_params['blkTo']
            # print('passed 4')

            params['params']['flat_type_val'] = verified_user.flatType
            params['params']['street_val'] = verified_user.streetName
            params['params']['blk_from_val'] = verified_user.blkFrom
            params['params']['blk_to_val'] = verified_user.blkTo


            print(f"params : {params['params']}")
            df = hdbService.get_results(params['params'], params['headers_street'], 'df')
            print(f"Results in dataframe format : {df}")
            print(f"update datetime of email {verified_user.email}")
            update_user_with_senddatetime(verified_user, datetimeSent)
            print(f"Before sending email to {verified_user.email}")
            header = f"""Hi. This is the alert for {datetime.now().month} month, {datetime.now().year}"""
            footer = f"If you would like to unsubscribe to this alert, click this link : localhost:5000/unsub/{verified_user.token}"
            send_email_template(verified_user.email,header, footer,True, df)

        
        json_results = {
        'emails': [user.email for user in verified_users]
        }   

        return jsonify({'message': 'Emails sent', 'data': json_results}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/", code=302)

# confirms the token from the user and sets user's verified to true
@app.route('/confirm/<token>')
def confirm(token):
    try:
        user = get_email_by_token(token)

        print(f'Email found : {user.email}, setting verified == true')
        update_email_verified_true(user.email)
        return render_template('confirmationSuccess.html')
    except Exception as ex:
        print(f"Unable to confirm due to {ex}")
        return render_template('confirmationFailure.html')

# Unsub the alert tagged to the token
@app.route('/unsub/<token>')
def unsubscribeAlert(token):
    try:
        user = get_user_by_token(token)

        print(f'Email found : {user.email}, removing this alert in database')
        assert user.token == token
        remove_alert_based_on_token(user)
        return render_template('unsubAlert.html')
    except Exception as ex:
        print(f"Something wrong must have happened as the email was not found")
        return render_template('generic404.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
