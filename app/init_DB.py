import sqlite3
import os
import mysql.connector

databaseName = 'database'
port = '3307'
mySQLHost = 'mysql'
mySQLHost = os.environ.get('MYSQL_HOST')  # This should match the service name in Docker Compose
mySQLUser = os.environ.get('MYSQL_USER')
mySQLPassword = os.environ.get('MYSQL_PASSWORD') 
mySQLRootPassword = os.environ.get('MYSQL_ROOT_PASSWORD')

# config = {
#     'database': databaseName,
#     'port': port,
#     'user':mySQLUser,
#     'password':mySQLPassword,
#     'host':mySQLHost
#     }

config = {
    'host': 'mysql',  # This should match the service name in Docker Compose
    'port': '3307',   # This should match the exposed port on the host
    'user': 'user',
    'password': 'password',
    'database': 'db',
}

try:
    connection = mysql.connector.connect(**config)

    # connection = sqlite3.connect('database.db')


    with open('app/HDBResalePriceAlert.sql','r') as f:
        with connection.cursor() as cur:
            cur.execute(f.read(), multi=True)
        connection.commit()

    cur = connection.cursor()

    cur.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ('dummy@gmail.com',' True', '4-room', 'Ang Mo Kio Ave 3', '322', '328', 'null', 'null')
                )

    cur.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ('dummy@hotmail.com',' True', '5-room', 'Ang Mo Kio Ave 3', '322', '328', 'null', 'null')
                )

    connection.commit()
    connection.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")