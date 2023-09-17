from cs50 import SQL
import sqlite3

def authenticate(username, password):

    # Connect to the database
    conn = sqlite3.connect('database/users.db')

    # Create a cursor object
    cur = conn.cursor()

    # Execute a SQL query to select the user with the given username and password
    cur.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))

    # Fetch the results of the query
    result = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # If a user was found, return their ID. Otherwise, return False.
    if result is not None:
        return result[0]
    else:
        return 0