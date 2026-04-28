from flask import Blueprint, request
from db import get_db_connection

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/activity', methods=['GET'])
def get_activity():
    prompt_id = request.args.get("prompt_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        al.*, 
        u.username
    FROM Activity_Logs al
    JOIN Users u ON al.user_id = u.user_id
    WHERE al.prompt_id = %s
    ORDER BY al.timestamp DESC
    """

    cursor.execute(query, (prompt_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"status": "success", "data": data}