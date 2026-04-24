from flask import Blueprint, request
from service.share_service import share_prompt

share_bp = Blueprint('share_bp', __name__)

@share_bp.route('/share', methods=['POST'])
def share():
    data = request.json

    prompt_id = data.get('prompt_id')
    shared_with_user_id = data.get('shared_with_user_id')
    shared_by = data.get('shared_by')
    permission = data.get('permission', 'view')

    if not prompt_id or not shared_with_user_id or not shared_by:
        return {"status": "error", "message": "Missing required fields"}

    result = share_prompt(prompt_id, shared_with_user_id, shared_by, permission)

    return result