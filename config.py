import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 기본 설정
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # MongoDB 설정
    MONGO_URI = os.getenv("MONGO_URI", "MONGO_LOCALHOST_URI")

    # JWT 설정
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1시간
    JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 3600  # 30일

    # CORS 설정
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
