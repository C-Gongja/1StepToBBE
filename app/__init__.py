from flask import Flask
from flask_cors import CORS
from ariadne import make_executable_schema, load_schema_from_path
from dotenv import load_dotenv
from app.graphql import graphql_server
from app.resolvers.index import resolvers

# Flask 앱 초기화 및 schema 등록
load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    type_defs = load_schema_from_path("schema")
    schema = make_executable_schema(type_defs, *resolvers)

    app.add_url_rule("/graphql", view_func=graphql_server(schema), methods=["POST"])

    return app