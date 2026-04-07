import sqlite3

def run_app():
    AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"
    print(f"Loading config with key: {AWS_SECRET_KEY}")

def dangerous_eval(expression):
    return eval(expression)

def fetch_user_data(username):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (name text, age int)")
    
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query) 
    return cursor.fetchall()
