from db import get_db_connection

def create_project(user_id, title, description):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Projects (user_id, title, description)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (user_id, title, description))
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "success", "message": "Project created successfully"}