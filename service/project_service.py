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
def get_projects(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ 1. OWN PROJECTS
    cursor.execute("""
        SELECT p.*, 'owner' AS role
        FROM Projects p
        WHERE p.user_id = %s
    """, (user_id,))
    owned = cursor.fetchall()

    # ✅ 2. SHARED PROJECTS (via prompts → shares)
    cursor.execute("""
        SELECT DISTINCT p.project_id, p.title, p.description, s.permission AS role
        FROM Shares s
        JOIN Prompts pr ON s.prompt_id = pr.prompt_id
        JOIN Projects p ON pr.project_id = p.project_id
        WHERE s.shared_with_user_id = %s
    """, (user_id,))
    shared = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "status": "success",
        "owned": owned,
        "shared": shared
    }