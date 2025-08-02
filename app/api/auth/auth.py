from datetime import datetime
from bson import Binary
from uuid import uuid4
from flask import Blueprint, logging, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import Schema, fields, ValidationError, validates
from db.db import get_db
import re

auth_bp = Blueprint("auth", __name__)


# 요청 데이터 검증 스키마
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    name = fields.Str(required=True, validate=lambda x: len(x) >= 2)

    @validates("password")
    def validate_password(self, value, **kwargs):  # **kwargs 추가
        if not re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", value):
            raise ValidationError("Password must contain letters and numbers.")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value, **kwargs):  # **kwargs 추가
        if not re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", value):
            raise ValidationError("Password must contain letters and numbers.")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    ⭐ 사용자 회원가입 - REST API로 처리하는 이유:
    - 복잡한 유효성 검증 필요
    - 비밀번호 해싱 등 보안 처리
    - 이메일 인증 등 부가 기능 연동
    """

    try:
        data = RegisterSchema().load(request.get_json())
        print(f"data: {data}")
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    db = get_db()

    # 이메일 중복 확인
    if db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 409

    # 사용자 생성
    user_data = {
        "uuid": Binary.from_uuid(uuid4()),
        "email": data["email"],
        "name": data["name"],
        "password_hash": generate_password_hash(data["password"]),
        "is_verified": False,
        "created_at": datetime.now().isoformat(),
    }

    result = db.users.insert_one(user_data)

    # JWT 토큰 생성
    access_token = create_access_token(identity=str(result.inserted_id))
    refresh_token = create_refresh_token(identity=str(result.inserted_id))

    return (
        jsonify(
            {
                "message": "User created successfully",
                "user_id": str(result.inserted_id),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """⭐ 로그인 - REST API로 처리하는 이유:
    - 인증 로직이 복잡함
    - JWT 토큰 발급
    - 로그인 실패 처리 등
    """

    schema = LoginSchema()

    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "details": err.messages}), 400

    db = get_db()
    user = db.users.find_one({"email": data["email"]})

    if not user or not check_password_hash(user["password_hash"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # JWT 토큰 생성
    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return jsonify(
        {
            "message": "Login successful",
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": user_id, "name": user["name"], "email": user["email"]},
        }
    )


@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    """⭐ 이메일 인증 - REST API가 적합한 이유:
    - 외부 서비스 연동 (이메일 발송)
    - 상태 변경 작업
    """

    # 이메일 인증 로직 구현
    pass
