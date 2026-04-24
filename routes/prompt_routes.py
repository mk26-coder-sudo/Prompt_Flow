from flask import Blueprint, request
from service.prompt_service import create_prompt

prompt_bp = Blueprint('prompt_bp', __name__)

@prompt_bp.route('/create-prompt', methods=['POST'])
def create():
    data = request.json

    project_id = data.get('project_id')
    title = data.get('title')
    description = data.get('description')
    user_id = data.get('user_id')
    content = data.get('content')

    if not project_id or not title or not user_id or not content:
        return {"status": "error", "message": "Missing required fields"}

    result = create_prompt(project_id, title, description, user_id, content)

    return result