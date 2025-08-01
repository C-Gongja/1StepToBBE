from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

mongo = PyMongo()
client = MongoClient("mongodb://root:example@localhost:27017/")


def init_db(app):
    print("🔄 init MongoDB...")
    mongo.init_app(app)

    try:
        client.admin.command("ping")
        print("MongoDB connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")

    # with app.app_context():
    #     try:
    #         mongo.db.command("ping")
    #         print("Successfully connect to MongoDB")

    #         # 필요시 인덱스 생성 등 초기 설정
    #         # setup_indexes()

    #     except ConnectionFailure as e:
    #         print("Failed to connect MongoDB: {e}")


def get_db():
    if "db" not in g:
        g.db = client.db
        print("♻️ Created new DB instance")
    else:
        print(f"♻️ Reuse existing DB Instance")

    return g.db


db = LocalProxy(get_db)
