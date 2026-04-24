from db import get_db_connection

def log_activity(user_id, action_type, prompt_id=None, version_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO Activity_Logs (user_id, action_type, prompt_id, version_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, action_type, prompt_id, version_id))

        conn.commit()

    except Exception as e:
        print("Log error:", e)

    finally:
        cursor.close()
        conn.close()