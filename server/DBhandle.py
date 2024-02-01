import sqlite3
import HashMD5 as md
import pandas as pd

def createDB():
    # Connect to the database (creates a new database if it doesn't exist)
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    # Create a table to store usernames, passwords, emails, and connection status if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            is_connected BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()[0]

    # Insert sample data if the table is empty
    if result == 0:
        cursor.execute("INSERT INTO users (username, password, email, is_connected) VALUES (?, ?, ?, ?)",
                       ("David", md.hash_pass("Lenovo"), "david@example.com", 1))
        cursor.execute("INSERT INTO users (username, password, email, is_connected) VALUES (?, ?, ?, ?)",
                       ("Moshe", md.hash_pass("Asus"), "moshe@example.com", 0))

    conn.commit()
    conn.close()

def showDB():
    # Connect to the database (creates a new database if it doesn't exist)
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    # Query all data from the users table
    query = 'SELECT id, username, SUBSTR(password, 1, 8) AS password, email, is_connected FROM users'
    df = pd.read_sql_query(query, conn)

    # Display the DataFrame
    print(df)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def username_exists(username):
    # Check if the username already exists in the database
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

def add_user(username, password, email, is_connected):
    # Check if the username already exists
    if username_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return

    # Connect to the database
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    # Insert a new user into the users table
    cursor.execute("INSERT INTO users (username, password, email, is_connected) VALUES (?, ?, ?, ?)",
                   (username, md.hash_pass(password), email, is_connected))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def login(username, password):
    # Connect to the database
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    # Close the database connection
    conn.close()

    return user

if __name__ == "__main__":
    createDB()
    add_user("i", "l", "il@example.com", 1)
    showDB()
