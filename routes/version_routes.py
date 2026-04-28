from flask import Blueprint, request
from service.version_service import add_version
from service.version_service import mark_best_version


version_bp = Blueprint('version_bp', __name__)


@version_bp.route('/add-version', methods=['POST'])
def add():
    data = request.json

    prompt_id = data.get('prompt_id')
    content = data.get('content')
    user_id = data.get('user_id')

    if not prompt_id or not content or not user_id:
        return {"status": "error", "message": "Missing required fields"}

    result = add_version(prompt_id, content, user_id)

    return result

@version_bp.route('/mark-best', methods=['POST'])
def mark_best():
    data = request.json
    version_id = data.get('version_id')
    user_id = data.get('user_id')

    if not version_id:
        return {"status": "error", "message": "version_id required"}

    result = mark_best_version(version_id, user_id)   
    return result

from service.version_service import get_versions

@version_bp.route('/get-versions', methods=['GET'])
def fetch_versions():
    prompt_id = request.args.get('prompt_id')

    if not prompt_id:
        return {"status": "error", "message": "prompt_id required"}

    return get_versions(prompt_id)