from db import get_db_connection
import mysql.connector
from db import get_db_connection
from werkzeug.security import check_password_hash


def create_user(username, email, password_hash):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, email, password_hash))
        conn.commit()

        cursor.close()
        conn.close()

        return {"status": "success", "message": "User created successfully"}

    except mysql.connector.IntegrityError:
        return {"status": "error", "message": "Username already exists"}

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        if check_password_hash(user['password_hash'], password):
            return {
                "status": "success",
                "message": "Login successful",
                "user_id": user['user_id'],
                "username": user['username']
            }
        else:
            return {"status": "error", "message": "Incorrect password"}
    else:
        return {"status": "error", "message": "User not found"}

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT user_id, username FROM Users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user