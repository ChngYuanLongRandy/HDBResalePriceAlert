import sqlite3

connection = sqlite3.connect('database.db')


with open('app/HDBResalePriceAlert.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, sent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('dummy@gmail.com',' True', '4-room', 'Ang Mo Kio Ave 3', '322', '328', 'null', 'false')
            )

cur.execute("INSERT INTO emails (email, verified, flatType, streetName, blkFrom, blkTo, lastSent, sent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ('dummy@hotmail.com',' True', '5-room', 'Ang Mo Kio Ave 3', '322', '328', 'null', 'false')
            )

connection.commit()
connection.close()