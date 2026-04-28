from db import get_db_connection
from service.activity_service import log_activity
from service.user_service import get_user_by_email


def create_prompt(project_id, title, description, user_id, content):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Insert into Prompts
        prompt_query = """
        INSERT INTO Prompts (project_id, title, description, created_by)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(prompt_query, (project_id, title, description, user_id))

        prompt_id = cursor.lastrowid

        # 2️⃣ Create Version 1
        version_query = """
        INSERT INTO Versions (prompt_id, version_number, content, contributor_id, is_best)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(version_query, (prompt_id, 1, content, user_id, True))

        conn.commit()

        # ✅ LOG HERE (CORRECT PLACE)
        log_activity(user_id, "CREATE_PROMPT", prompt_id)

        return {"status": "success", "message": "Prompt created with Version 1"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def get_prompts(project_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.prompt_id, p.title, p.description, v.content
    FROM Prompts p
    JOIN Versions v ON p.prompt_id = v.prompt_id
    WHERE v.is_best = TRUE AND p.project_id = %s
    """

    cursor.execute(query, (project_id,))
    prompts = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"status": "success", "data": prompts}
def share_prompt(prompt_id, shared_with_email, shared_by, permission):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔍 get user_id from email
        user = get_user_by_email(shared_with_email)

        if not user:
            return {"status": "error", "message": "User not found"}

        shared_with_user_id = user['user_id']

        # 🔒 prevent duplicate sharing
        cursor.execute("""
            SELECT * FROM Shares 
            WHERE prompt_id = %s AND shared_with_user_id = %s
        """, (prompt_id, shared_with_user_id))

        if cursor.fetchone():
            return {"status": "error", "message": "Already shared"}

        # ✅ insert share
        cursor.execute("""
            INSERT INTO Shares (prompt_id, shared_with_user_id, shared_by, permission)
            VALUES (%s, %s, %s, %s)
        """, (prompt_id, shared_with_user_id, shared_by, permission))

        conn.commit()
        log_activity(shared_by, "SHARE_PROMPT", prompt_id)

        return {"status": "success", "message": "Prompt shared successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()