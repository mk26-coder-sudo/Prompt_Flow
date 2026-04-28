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

        return {
            "status": "success",
            "message": "Activity logged"
        }

    except Exception as e:
        print("Log error:", e)
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        cursor.close()
        conn.close()


# ✅ FETCH ACTIVITY (NEW - IMPORTANT)
def log_activity(user_id, action_type, prompt_id=None, version_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("🔥 LOGGING CALLED:", user_id, action_type, prompt_id, version_id)

        query = """
        INSERT INTO Activity_Logs (user_id, action_type, prompt_id, version_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, action_type, prompt_id, version_id))

        conn.commit()
        print("✅ LOG INSERTED")

    except Exception as e:
        print("❌ Log error:", e)

    finally:
        cursor.close()
        conn.close()