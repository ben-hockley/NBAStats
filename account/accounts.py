import sqlite3
import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed

def init_users_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Create a new SQLite database (or connect to an existing one)
    # Create a new table for users if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            following_teams TEXT,
            following_players TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_new_user(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # hash the password before storing it
    hashed_password = hash_password(password)
    # Check if the username already exists
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone() is not None:
        raise Exception("Username already exists")
    else:
        # Insert a new user into the users table
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Retrieve the user from the users table
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

def check_password(username, password):
    user = get_user(username)
    if user is None:
        return False
    # Check if the password matches the hashed password
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, user[2])