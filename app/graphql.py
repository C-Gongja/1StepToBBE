from flask import request, jsonify
from ariadne import graphql_sync
from db.db import get_db


def graphql_server(schema):
    def handler():
        data = request.get_json()
        success, result = graphql_sync(
            schema, data, context_value={"request": request, "db": get_db()}, debug=True
        )
        return jsonify(result)

    return handler
