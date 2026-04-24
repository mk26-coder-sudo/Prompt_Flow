from flask import Blueprint, request
from service.tag_service import add_tags_to_prompt

tag_bp = Blueprint('tag_bp', __name__)

@tag_bp.route('/add-tags', methods=['POST'])
def add_tags():
    data = request.json

    prompt_id = data.get('prompt_id')
    tags = data.get('tags')   # list expected

    if not prompt_id or not tags:
        return {"status": "error", "message": "Missing data"}

    result = add_tags_to_prompt(prompt_id, tags)

    return result