import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(query)

connection.commit()
connection.close()
