import mysql.connector
from flask import g
import yaml
from model.User import User
from model.SubUser import SubUser
from typing import List
# from app import app
import os

databaseName = 'database'
port = '3306'
mySQLHost = 'mysql'
mySQLHost = os.environ.get('MYSQL_HOST')  # This should match the service name in Docker Compose
mySQLUser = os.environ.get('MYSQL_USER')
mySQLPassword = os.environ.get('MYSQL_PASSWORD') 
mySQLRootPassword = os.environ.get('MYSQL_ROOT_PASSWORD')

config = {
    'host': 'mysql',  # This should match the service name in Docker Compose
    'port': '3306',   # This should match the exposed port on the host
    'user': 'user',
    'password': 'password',
    'database': 'db',
}

config_path = "app/config/config.yaml"

with open(config_path, 'r') as yaml_file:
    configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

def create_tables():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    # Check if 'emails' table already exists
    cursor.execute("SHOW TABLES LIKE 'emails'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute(
            '''CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            email VARCHAR(255) NOT NULL,
            verified BOOLEAN NOT NULL,
            flatType VARCHAR(255) NOT NULL,
            streetName VARCHAR(255) NOT NULL,
            blkFrom INT NOT NULL,
            blkTo INT NOT NULL,
            lastSent TIMESTAMP,
            sent BOOLEAN
            ''')
        connection.commit()
        connection.close()

def add_email(new_user:SubUser):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                    (new_user.email,' false', new_user.flatType, new_user.streetName, new_user.blkFrom, new_user.blkTo, 'null', 'null'))
        connection.commit()
        connection.close()
    except Exception as ex:
        print(f"Unable to add email due to {ex}")

def get_emails() -> List[User]: 
    try:
        print("Entering Get emails method from dbservice")
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM emails")
        rows = cursor.fetchall()

    #     print(f"Rows from the database: {rows}")

    # #  # Convert ' True' and ' False' to True and False
    # #     cleaned_rows = [(item if not isinstance(item, str) else item.strip() == 'True') for row in rows for item in row]

        # emails = [User.from_dict(dict(row)) for row in rows]

        emails = []
        for row in rows:
            user = User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9])
            print(user)
            emails.append(user)

        emails = [User(row[0],row[1],row[2],row[3],
                   row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]

        connection.commit()
        connection.close()

        return emails
    except Exception as ex:
        print(f"Unable to retrieve all emails due to {ex}")

def get_email(email:str) -> User:
    print("Entering get email method")
    print(f"Email is {email}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails where email = (?)", (email,))
    rows = cursor.fetchone()

    print(f'Rows in get email : {rows}')

    emails = [User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]
    
    connection.commit()
    connection.close()

    return emails

def update_user_with_senddatetime(user:User, datetime:str):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE emails SET lastSent = (?)  where token == (?)", (datetime,user.token,))

    connection.commit()
    connection.close()

#   retrieves the email by the token
def get_email_by_token(token:str)-> User:

    print("Entering get email by token method")
    print(f"Token is {token}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails where token = (?)", (token,))
    rows = cursor.fetchall()

    assert len(rows) == 1
    print(f'Email found in database: {rows}')

    emails = [User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]
    
    connection.commit()
    connection.close()


    return emails[0]

def update_email_with_token(new_user:SubUser , token:str):

    print("Entering update email with token")
    print(f"Token is {token}")
    print(f"New user is {new_user}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    email = new_user.email
    flatType = new_user.flatType
    streetName = new_user.streetName 
    blkFrom = new_user.blkFrom
    blkTo = new_user.blkTo 
    
    cursor.execute("""
                   UPDATE emails SET token = (?)  
                   where email == (?) AND 
                   flatType == (?) AND
                   streetname == (?) AND
                   blkFrom == (?) AND
                   blkTo == (?) 
                   """  
                   , (token, email, flatType, streetName, blkFrom, blkTo))

    connection.commit()
    connection.close()

#   updates the row with verified 
def update_email_verified_true(email:str):

    print("Entering update email verified true method")
    print(f"Email is {email}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE emails set verified == true where email = (?)", (email,))

    connection.commit()
    connection.close()

def get_user_by_token(token:str) -> User:
    try:
        print("Entering get user by token")
        print(f"Token is {token}")
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * from emails where token == (?)", (token,))
        rows = cursor.fetchall()

        assert len(rows) == 1

        emails = [User(row[0],row[1],row[2],row[3],
                    row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]

        connection.commit()
        connection.close() 

        return emails[0]

    except Exception as ex:
        print(f"Unable to execute due to {ex}")

#   delete alert based on token
def remove_alert_based_on_token(user:User):
    try:
        print("Entering Remove alert based on token")
        print(f"user is {user}")
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("DELETE from emails where token == (?)", (user.token,))

        connection.commit()
        connection.close()
    except Exception as ex:
        print(f"Unable to execute due to {ex}")
