import os
from flask import Flask
from flask_cors import CORS
from ariadne import make_executable_schema, load_schema_from_path
from dotenv import load_dotenv
from app.graphql import graphql_server
from app.graphql.resolvers.index import resolvers
from app.graphql.schema import default_schema
from db.db import init_db

# Flask 앱 초기화 및 schema 등록
load_dotenv()

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	
	app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/myapp')
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
	app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

	CORS(app, origins=[os.getenv('LOCALHOST')])

	init_db(app)

	# GraphQL 스키마 로드
	try:
		type_defs = load_schema_from_path("schema")
		schema = make_executable_schema(type_defs, *resolvers)
		app.add_url_rule("/graphql", view_func=graphql_server(schema), methods=["POST"])
	except Exception as e:
		print(f"GraphQL 스키마 로드 오류: {e}")
		# 개발 중에는 기본 스키마를 사용
		app.add_url_rule("/graphql", view_func=graphql_server(default_schema), methods=["POST"])
	
	# 헬스체크 엔드포인트
	@app.route('/health')
	def health_check():
			return {'status': 'healthy', 'message': 'Server is running'}
	
	return app