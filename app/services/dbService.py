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
    cursor.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, sent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (params["email"],' false', params["flat_type_val"], params["street_val"], params["blk_from_val"], params["blk_to_val"], 'null', 'false'))
    connection.commit()
    connection.close()

def get_emails():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    emails = [{'id': row[0], 'email': row[1]} for row in rows]

    connection.commit()
    connection.close()

    return emails