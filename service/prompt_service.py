from db import get_db_connection
from service.activity_service import log_activity

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