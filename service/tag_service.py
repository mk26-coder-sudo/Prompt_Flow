from db import get_db_connection

def add_tags_to_prompt(prompt_id, tag_list):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for tag in tag_list:
            # 1️⃣ Check if tag exists
            cursor.execute("SELECT tag_id FROM Tags WHERE tag_name = %s", (tag,))
            result = cursor.fetchone()

            if result:
                tag_id = result[0]
            else:
                # 2️⃣ Insert new tag
                cursor.execute("INSERT INTO Tags (tag_name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid

            # 3️⃣ Insert into mapping table
            cursor.execute("""
                INSERT IGNORE INTO Prompt_Tags (prompt_id, tag_id)
                VALUES (%s, %s)
            """, (prompt_id, tag_id))

        conn.commit()

        return {"status": "success", "message": "Tags added successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()