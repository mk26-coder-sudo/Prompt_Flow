from flask import Blueprint
from db import get_db_connection

activity_bp = Blueprint('activity_bp', __name__)

@activity_bp.route('/activity/<int:user_id>', methods=['GET'])
def get_activity(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM Activity_Logs
    WHERE user_id = %s
    ORDER BY timestamp DESC
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"status": "success", "data": data}