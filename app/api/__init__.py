from flask import Blueprint
from app.api.auth.auth import auth_bp
from app.api.user.user import user_bp

# from app.api.todo import todo_bp
# from app.api.schedule import schedule_bp
# from app.api.streak import streak_bp


def setup_rest_api(app):
    """REST API 블루프린트 등록"""

    # API v1 메인 블루프린트
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    # 각 도메인별 블루프린트 등록
    api_v1.register_blueprint(auth_bp, url_prefix="/auth")  # /api/v1/auth/*
    api_v1.register_blueprint(user_bp, url_prefix="/users")
    # api_v1.register_blueprint(todo_bp, url_prefix="/todos")
    # api_v1.register_blueprint(schedule_bp, url_prefix="/schedule")
    # api_v1.register_blueprint(streak_bp, url_prefix="/streak")

    app.register_blueprint(api_v1)
