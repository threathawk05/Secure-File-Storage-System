import sqlite3

# Initialize database
def initialize_db():
    conn = sqlite3.connect("storage.db")  # Creates or connects to the database
    cursor = conn.cursor()

    # Create users table (stores username and hashed password)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create files table (stores encrypted file data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_data BLOB NOT NULL,
            FOREIGN KEY (owner) REFERENCES users(username)
        )
    ''')

    conn.commit()
    conn.close()

# Run database initialization when this file is executed
if __name__ == "__main__":
    initialize_db()
    print("[✅] Database initialized successfully.")
