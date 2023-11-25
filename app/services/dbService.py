import sqlite3
from flask import g
import yaml

config_path = "app/config/config.yaml"

with open(config_path, 'r') as yaml_file:
    configData = yaml.load(yaml_file, Loader=yaml.FullLoader)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('HDBResalePriceAlertEmail.db')  # Replace with your desired SQLite database file
    return db

def create_tables():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT)''')
        connection.commit()
    connection.close()

def add_email(email):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO emails (email) VALUES (?)", (email))
    connection.commit()
    connection.close()

def get_emails():
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM emails")
    rows = cursor.fetchall()

    emails = [{'id': row[0], 'email': row[1]} for row in rows]

    connection.commit()
    connection.close()

    return emails