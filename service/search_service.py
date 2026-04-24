from db import get_db_connection

def search_prompts(keyword=None, tag=None, project_id=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT DISTINCT p.prompt_id, p.title, p.description, pr.title AS project_name
        FROM Prompts p
        JOIN Projects pr ON p.project_id = pr.project_id
        LEFT JOIN Prompt_Tags pt ON p.prompt_id = pt.prompt_id
        LEFT JOIN Tags t ON pt.tag_id = t.tag_id
        WHERE 1=1
        """

        params = []

        if keyword:
            query += " AND (p.title LIKE %s OR p.description LIKE %s)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        if tag:
            query += " AND t.tag_name = %s"
            params.append(tag)

        if project_id:
            query += " AND p.project_id = %s"
            params.append(project_id)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        return {"status": "success", "data": results}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()