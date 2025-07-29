# app/graphql/resolvers/query_resolvers.py
from ariadne import QueryType
from bson import ObjectId
from db.db import get_db

query_resolvers = QueryType()

@query_resolvers.field("hello")
def resolve_hello(_, info):
    return "Hello from GraphQL!"

@query_resolvers.field("users")
def resolve_users(_, info):
    db = get_db()
    users = list(db.users.find())
    
    # ObjectId를 문자열로 변환
    for user in users:
        user['id'] = str(user['_id'])
        del user['_id']
    
    return users

@query_resolvers.field("user")
def resolve_user(_, info, id):
    db = get_db()
    
    try:
        user = db.users.find_one({"_id": ObjectId(id)})
        if user:
            user['id'] = str(user['_id'])
            del user['_id']
            return user
        return None
    except Exception as e:
        print(f"사용자 조회 오류: {e}")
        return None