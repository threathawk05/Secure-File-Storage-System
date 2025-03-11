import sqlite3
from argon2 import PasswordHasher

# Initialize Argon2 password hasher
ph = PasswordHasher()

# Function to connect to the database
def get_db_connection():
    return sqlite3.connect("storage.db")

# Function to initialize the database and create the users table if it doesn't exist
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Hash the password using Argon2
        hashed_password = ph.hash(password)
        
        # Insert user into database
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        
        return True, "[✅] User registered successfully!"
    
    except sqlite3.IntegrityError:
        conn.close()
        return False, "[❌] Username already exists. Please choose another one."

# Function to log in a user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()  # Close connection after retrieving the data

    if result:
        stored_hashed_password = result[0]
        try:
            # Verify password
            ph.verify(stored_hashed_password, password)
            return True, "[✅] Login successful!"
        except:
            return False, "[❌] Incorrect password."
    else:
        return False, "[❌] User not found."

# Initialize the database when the module is imported
initialize_db()
