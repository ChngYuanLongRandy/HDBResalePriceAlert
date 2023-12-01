import sqlite3
from flask import g
import yaml

config_path = "app/config/config.yaml"

with open(config_path, 'r') as yaml_file:
    configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

def create_tables():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute(
            '''CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            email TEXT NOT NULL,
            verified BOOLEAN NOT NULL,
            flatType TEXT NOT NULL,
            streetName TEXT NOT NULL,
            blkFrom INTEGER NOT NULL,
            blkTo INTEGER NOT NULL,
            lastSent TIMESTAMP,
            sent BOOLEAN
            ''')
        connection.commit()
        connection.close()

def add_email(params:dict):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (params["email"],' false', params["flat_type_val"], params["street_val"], params["blk_from_val"], params["blk_to_val"], 'null', 'null'))
    connection.commit()
    connection.close()

def get_emails():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    emails = [{'id': row[0],'created': row[1], 'email': row[2], 'verified': row[3],
               'flatType': row[4],'streetname': row[5],'blkFrom': row[6],'blkTo': row[7],
               'lastSent': row[8],'token': row[9]} for row in rows]

    connection.commit()
    connection.close()

    return emails

def get_email(email:str):
    print("Entering get email method")
    print(f"Email is {email}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails where email = (?)", (email,))
    rows = cursor.fetchall()

    print(f'Rows in get email : {rows}')

    emails = [{'id': row[0],'created': row[1], 'email': row[2], 'verified': row[3],
               'flatType': row[4],'streetname': row[5],'blkFrom': row[6],'blkTo': row[7],
               'lastSent': row[8],'token': row[9]} for row in rows]

    connection.commit()
    connection.close()

    return emails

def update_email_with_senddatetime(email:str, datetime:str):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE emails SET lastSent = (?)  where email == (?)", (datetime,email,))

    connection.commit()
    connection.close()

#   retrieves the email by the token
def get_email_by_token(token:str):

    print("Entering get email by token method")
    print(f"Token is {token}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails where token = (?)", (token,))
    rows = cursor.fetchall()

    print(f'Rows in get email : {rows}')

    emails = [{'id': row[0],'created': row[1], 'email': row[2], 'verified': row[3],
               'flatType': row[4],'streetname': row[5],'blkFrom': row[6],'blkTo': row[7],
               'lastSent': row[8],'token': row[9]} for row in rows]

    connection.commit()
    connection.close()


    return emails[0]

def update_email_with_token(params: dict , token:str):

    print("Entering update email with token")
    print(f"Token is {token}")
    print(f"Params is {[params]}")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    email = params["email"]
    flatType = params['flat_type_val']
    streetName = params["street_val"] 
    blkFrom = params["blk_from_val"]
    blkTo = params['blk_to_val'] 
    
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