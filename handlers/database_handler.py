import sqlite3
from cs50 import SQL
import os
import sqlite3

enckey = "95fb144ffdb4a1899ce187a015ec02a21a227018"


def __init__():
    if os.path.exists("database/users.db"):
        return "Error 301 occured, please contact EduCentral"
    else:
        """Should run the first time to build the sqlite3 database for the users"""
        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
    
        cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, authority_level TEXT, password TEXT);""")
        conn.commit()
        conn.close()

def if_fetch_name(user_id):

    # Connect to the database
    conn = sqlite3.connect('database/users.db')

    # Create a cursor object
    cur = conn.cursor()

    # Execute a SQL query to select the name of the user with the given ID
    cur.execute('SELECT name FROM users WHERE id = ?', (user_id,))

    # Fetch the results of the query
    result = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # If a user was found, return their name. Otherwise, return 0.
    if result is not None:
        return result[0]
    else:
        return 0
    
def learner_count():
    conn = sqlite3.connect('database/student_data.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM students;')
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]

def parent_count():
    conn = sqlite3.connect('database/student_data.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM parents;')
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]