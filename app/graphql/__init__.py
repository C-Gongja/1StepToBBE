# app/graphql/__init__.py
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphQL
from flask import request, jsonify

def graphql_server(schema):
    """GraphQL 서버 설정"""
    explorer_html = ExplorerGraphQL().html(None)
    
    def graphql_view():
        if request.method == "GET":
            return explorer_html
        
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request, "db": get_db()},
            debug=current_app.debug
        )
        
        status_code = 200 if success else 400
        return jsonify(result), status_code
    
    return graphql_view