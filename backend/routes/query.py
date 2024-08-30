from flask import request, jsonify, Blueprint

from backend.models.person import Author

query = Blueprint('query', __name__)


@query.route('/authors', methods=['GET'])
def query_author():
    print("receive query")
    name = request.args.get('name')
    query_info = {}
    if name:
        query_info['name'] = name

    authors = Author.objects(**query_info)
    print(len(authors))
    print(authors[0].name)

    return jsonify("result"), 200
