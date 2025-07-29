
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure

mongo = PyMongo()

def init_db(app):
	mongo.init_app(app)
	
	with app.app_context():
		try:
			mongo.db.admin.comman('ping')
			print("Successfully connect to MongoDB")
		except ConnectionFailure:
			print("Failed to connect MongoDB")
		
	
def get_db():
	if 'db' not in g:
		g.db = mongo.db
	return g.db

db = LocalProxy(get_db)

