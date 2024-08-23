from flask import request, jsonify

from backend.app import api
from backend.models.person import Author


@api.route('/authors', methods=['GET'])
def query_author():
    print("receive query")
    name = request.args.get('name')
    query = {}
    if name:
        query['name'] = name

    authors = Author.objects(**query)
    print(len(authors))

    return jsonify("result"), 200

