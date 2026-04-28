from flask import Blueprint, request
from service.prompt_service import create_prompt
from service.prompt_service import get_prompts
from service.prompt_service import share_prompt


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
@prompt_bp.route('/get-prompts', methods=['GET'])
def fetch_prompts():
    project_id = request.args.get('project_id')

    if not project_id:
        return {"status": "error", "message": "project_id required"}

    result = get_prompts(project_id)
    return result
@prompt_bp.route('/share-prompt', methods=['POST'])
def share():
    data = request.json

    prompt_id = data.get('prompt_id')
    email = data.get('email')
    shared_by = data.get('user_id')
    permission = data.get('permission', 'view')

    if not prompt_id or not email or not shared_by:
        return {"status": "error", "message": "Missing fields"}

    return share_prompt(prompt_id, email, shared_by, permission)