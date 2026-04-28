from db import get_db_connection
from service.activity_service import log_activity


def add_version(prompt_id, content, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Get latest version number
        cursor.execute(
            "SELECT MAX(version_number) FROM Versions WHERE prompt_id = %s",
            (prompt_id,)
        )
        last_version = cursor.fetchone()[0]
        new_version = (last_version or 0) + 1

        # 2️⃣ 🔥 Reset previous best (IMPORTANT CHANGE)
        cursor.execute("""
            UPDATE Versions
            SET is_best = FALSE
            WHERE prompt_id = %s
        """, (prompt_id,))

        conn.commit()  # Prevent lock issues

        # 3️⃣ Insert new version as BEST
        cursor.execute("""
            INSERT INTO Versions (prompt_id, version_number, content, contributor_id, is_best)
            VALUES (%s, %s, %s, %s, TRUE)
        """, (prompt_id, new_version, content, user_id))

        conn.commit()
        version_id = cursor.lastrowid

        # 4️⃣ Log activity
        log_activity(user_id, "ADD_VERSION", prompt_id, version_id)

        return {
            "status": "success",
            "message": f"Version {new_version} created and set as best"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def mark_best_version(version_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Get prompt_id
        cursor.execute(
            "SELECT prompt_id FROM Versions WHERE version_id = %s",
            (version_id,)
        )
        result = cursor.fetchone()

        if not result:
            return {"status": "error", "message": "Version not found"}

        prompt_id = result[0]

        # 2️⃣ 🔥 ONLY reset current best (NOT ALL ROWS)
        cursor.execute("""
            UPDATE Versions
            SET is_best = FALSE
            WHERE prompt_id = %s AND is_best = TRUE
        """, (prompt_id,))

        conn.commit()  # 🔥 VERY IMPORTANT (prevents lock)

        # 3️⃣ Set new best
        cursor.execute("""
            UPDATE Versions
            SET is_best = TRUE
            WHERE version_id = %s
        """, (version_id,))

        # 4️⃣ Log activity
        log_activity(
            user_id=user_id,
            action_type="MARK_BEST",
            prompt_id=prompt_id,
            version_id=version_id
        )

        conn.commit()

        return {"status": "success"}

    except Exception as e:
        print("❌ MARK BEST ERROR:", e)
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

# ✅ GET VERSIONS (ORDERED + CLEAN)
def get_versions(prompt_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM Versions 
        WHERE prompt_id = %s
        ORDER BY is_best DESC, version_number DESC
        """

    cursor.execute(query, (prompt_id,))
    versions = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"status": "success", "data": versions}