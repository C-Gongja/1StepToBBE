import os
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

from db.db import init_db

from app.graphql import setup_graphql

from app.api import setup_rest_api

# Flask 앱 초기화 및 schema 등록
load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    CORS(app, origins=[os.getenv("LOCALHOST")])
    # JWTManager(app)

    init_db(app)

    # ⭐ GraphQL 설정 - 데이터 조회용
    setup_graphql(app)

    # ⭐ REST API 설정 - 인증, 데이터 변경용
    setup_rest_api(app)

    # 헬스체크 엔드포인트
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "message": "GraphQL + REST API Server is running",
            "endpoints": {"graphql": "/graphql", "rest_api": "/api/v1"},
        }

    return app
