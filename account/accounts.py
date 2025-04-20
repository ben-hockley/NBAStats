import sqlite3
import bcrypt

from data.nba import NBA_teams
from data.nba import get_team_by_id
from data.nba import Team

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

def follow_new_team(username, team_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Update the user's following_teams field to include the new team
    following = cur.execute("SELECT following_teams FROM users WHERE username=?", (username,)).fetchone()
    if following is None:
        new_following = str(team_id)
    else:
        following = following[0].split(",")
        following.append(str(team_id))
        new_following = ",".join(following)
    # Update the database with the new following_teams
    cur.execute("UPDATE users SET following_teams = ? WHERE username=?", (new_following, username))
    conn.commit()
    conn.close()

def get_following_teams(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Retrieve the user's following_teams field
    cur.execute("SELECT following_teams FROM users WHERE username=?", (username,))
    following = cur.fetchone()
    conn.close()
    if following is None:
        return []
    else:
        following = following[0].split(",")
        following = [int(team_id) for team_id in following if team_id.isdigit()]
        print(following)
        following_teams = []
        for team_id in following:
            team = get_team_by_id(team_id)
            following_teams.append(team)
        return following_teams
    
def get_following_teams_ids(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Retrieve the user's following_teams field
    cur.execute("SELECT following_teams FROM users WHERE username=?", (username,))
    following = cur.fetchone()
    conn.close()
    if following is None:
        return []
    else:
        following = following[0].split(",")
        following = [int(team_id) for team_id in following if team_id.isdigit()]
        return following