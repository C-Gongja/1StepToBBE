from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

mongo = PyMongo()

def init_db(app):
  print("🔄 init MongoDB...")
  mongo.init_app(app)

  with app.app_context():
    try:
      mongo.db.admin.comman("ping")
      print("Successfully connect to MongoDB")

      # 필요시 인덱스 생성 등 초기 설정
      # setup_indexes()

    except ConnectionFailure as e:
      print("Failed to connect MongoDB: {e}")


def get_db():
  if "db" not in g:
    g.db = mongo.db
  else:
    print(f"♻️ Reuse existing DB Instance")

  return g.db


db = LocalProxy(get_db)
