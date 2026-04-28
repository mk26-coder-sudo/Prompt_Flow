from service.project_service import create_project
from flask import Blueprint, request
from service.project_service import get_projects

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
@project_bp.route('/get-projects', methods=['GET'])
def fetch_projects():
    user_id = request.args.get('user_id')

    if not user_id:
        return {"status": "error", "message": "user_id required"}

    result = get_projects(user_id)
    return result