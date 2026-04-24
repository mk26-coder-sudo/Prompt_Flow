from service.project_service import create_project
from flask import Blueprint, request

project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/create-project', methods=['POST'])
def create():
    data = request.json

    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')

    if not user_id or not title:
        return {"status": "error", "message": "Missing required fields"}

    result = create_project(user_id, title, description)

    return result