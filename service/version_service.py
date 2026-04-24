from db import get_db_connection
from service.activity_service import log_activity

def add_version(prompt_id, content, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Get latest version number
        query = """
        SELECT MAX(version_number) FROM Versions WHERE prompt_id = %s
        """
        cursor.execute(query, (prompt_id,))
        last_version = cursor.fetchone()[0]

        new_version = (last_version or 0) + 1

        # 2️⃣ Set previous best to FALSE
        update_query = """
        UPDATE Versions SET is_best = FALSE WHERE prompt_id = %s
        """
        cursor.execute(update_query, (prompt_id,))

        # 3️⃣ Insert new version
        insert_query = """
        INSERT INTO Versions (prompt_id, version_number, content, contributor_id, is_best)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (prompt_id, new_version, content, user_id, True))

        conn.commit()
        version_id = cursor.lastrowid

        log_activity(user_id, "ADD_VERSION", prompt_id, version_id)
        return {
            "status": "success",
            "message": f"Version {new_version} created"
        }
        

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def mark_best_version(version_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Get prompt_id of that version
        cursor.execute("SELECT prompt_id FROM Versions WHERE version_id = %s", (version_id,))
        result = cursor.fetchone()

        if not result:
            return {"status": "error", "message": "Version not found"}

        prompt_id = result[0]

        # 2️⃣ Set all versions of this prompt to FALSE
        cursor.execute("""
            UPDATE Versions 
            SET is_best = FALSE 
            WHERE prompt_id = %s
        """, (prompt_id,))

        # 3️⃣ Set selected version as TRUE
        cursor.execute("""
            UPDATE Versions 
            SET is_best = TRUE 
            WHERE version_id = %s
        """, (version_id,))

        conn.commit()

        return {"status": "success", "message": "Best version updated"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()