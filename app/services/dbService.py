import mysql.connector
from flask import g
import yaml
from model.User import User
from model.SubUser import SubUser
from typing import List
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

databaseName = os.environ.get('MYSQL_DATABASE')
mySQLHost = os.environ.get('MYSQL_HOST')
mySQLUser = os.environ.get('MYSQL_USER')
mySQLPassword = os.environ.get('MYSQL_PASSWORD') 
mySQLPort = int(os.environ.get('MYSQL_PORT'))

config = {
    'host': mySQLHost,  # This should match the service name in Docker Compose
    'port': mySQLPort,   # This should match the exposed port on the host
    'user': mySQLUser,
    'password': mySQLPassword,
    'database': databaseName,
}

config_path = "app/config/config.yaml"

with open(config_path, 'r') as yaml_file:
    configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

def create_tables():
    logger.info("Entering create tables method from dbservice")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        # Check if 'emails' table already exists
        cursor.execute("SHOW TABLES LIKE 'emails'")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute(
                '''
                CREATE TABLE emails (
                id INT PRIMARY KEY AUTO_INCREMENT,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                email VARCHAR(255) NOT NULL,
                verified BOOLEAN NOT NULL,
                flatType VARCHAR(255) NOT NULL,
                streetName VARCHAR(255) NOT NULL,
                blkFrom INT NOT NULL,
                blkTo INT NOT NULL,
                lastSent TIMESTAMP,
                token VARCHAR(255))
                ''')
            connection.commit()
            connection.close()
    except Exception as e:
        logger.error(f"Unable to create tables due to {e}")


def add_email(new_user:SubUser):
    try:
        logger.info("Entering Add email method from dbservice")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (new_user.email, False, new_user.flatType, new_user.streetName, new_user.blkFrom, new_user.blkTo, None, None))        
        connection.commit()
        connection.close()
    except Exception as ex:
        logger.error(f"Unable to add email due to {ex}")

def get_emails() -> List[User]: 
    try:
        logger.info("Entering Get emails method from dbservice")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM emails")
        rows = cursor.fetchall()

        emails = []
        for row in rows:
            user = User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9])
            logger.info(user)
            emails.append(user)

        emails = [User(row[0],row[1],row[2],row[3],
                   row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]

        connection.commit()
        connection.close()

        return emails
    except Exception as ex:
        logger.error(f"Unable to retrieve all emails due to {ex}")

def get_email(email:str) -> User:
    logger.info("Entering get email method")
    logger.info(f"Email is {email}")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails where email = %s", (email,))
    rows = cursor.fetchone()

    logger.info(f'Rows in get email : {rows}')

    emails = [User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]
    
    connection.commit()
    connection.close()

    return emails


def update_user_with_senddatetime(user:User, datetime:str):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("UPDATE emails SET lastSent = %s WHERE token = %s", (datetime,user.token))

    connection.commit()
    connection.close()

def get_email_by_token(token:str)-> User:
    logger.info("Entering get email by token method")
    logger.info(f"Token is {token}")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails WHERE token = %s", (token,))
    rows = cursor.fetchall()

    assert len(rows) == 1
    logger.info(f'Email found in database: {rows}')

    emails = [User(row[0],row[1],row[2],row[3],
                row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]
    
    connection.commit()
    connection.close()

    return emails[0]

def update_email_with_token(new_user:SubUser , token:str):
    logger.info("Entering update email with token")
    logger.info(f"Token is {token}")
    logger.info(f"New user is {new_user}")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    email = new_user.email
    flatType = new_user.flatType
    streetName = new_user.streetName 
    blkFrom = new_user.blkFrom
    blkTo = new_user.blkTo 
    
    cursor.execute("""
                   UPDATE emails SET token = %s  
                   WHERE email = %s AND 
                   flatType = %s AND
                   streetname = %s AND
                   blkFrom = %s AND
                   blkTo = %s 
                   """  
                   , (token, email, flatType, streetName, blkFrom, blkTo))

    connection.commit()
    connection.close()

def update_email_verified_true(email:str):
    logger.info("Entering update email verified true method")
    logger.info(f"Email is {email}")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("UPDATE emails SET verified = true WHERE email = %s", (email,))

    connection.commit()
    connection.close()

def get_user_by_token(token:str) -> User:
    try:
        logger.info("Entering get user by token")
        logger.info(f"Token is {token}")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM emails WHERE token = %s", (token,))
        rows = cursor.fetchall()

        assert len(rows) == 1

        emails = [User(row[0],row[1],row[2],row[3],
                    row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]

        connection.commit()
        connection.close() 

        return emails[0]

    except Exception as ex:
        logger.error(f"Unable to execute due to {ex}")

def remove_alert_based_on_token(user:User):
    try:
        logger.info("Entering Remove alert based on token")
        logger.info(f"user is {user}")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM emails WHERE token = %s", (user.token,))

        connection.commit()
        connection.close()
    except Exception as ex:
        logger.error(f"Unable to execute due to {ex}")