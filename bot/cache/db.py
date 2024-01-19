import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('bot/cache/code_explanations.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table as per requirement
cursor.execute('''CREATE TABLE IF NOT EXISTS explanations
                  (code TEXT PRIMARY KEY, explanation TEXT)''')

# Commit changes and close the connection
conn.commit()
conn.close()
