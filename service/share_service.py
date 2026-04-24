from db import get_db_connection

def share_prompt(prompt_id, shared_with_user_id, shared_by, permission):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO Shares (prompt_id, shared_with_user_id, shared_by, permission)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (prompt_id, shared_with_user_id, shared_by, permission))
        conn.commit()

        return {"status": "success", "message": "Prompt shared successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()