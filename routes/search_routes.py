from flask import Blueprint, request
from service.search_service import search_prompts

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    tag = request.args.get('tag')
    project_id = request.args.get('project_id')

    result = search_prompts(keyword, tag, project_id)

    return result