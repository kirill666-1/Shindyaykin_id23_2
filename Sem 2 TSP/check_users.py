import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()
cursor.execute("SELECT id, email, hashed_password FROM users")
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]}, Email: {user[1]}, Hashed Password: {user[2]}")

conn.close()