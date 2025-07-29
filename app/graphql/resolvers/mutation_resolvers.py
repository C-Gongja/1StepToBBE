from ariadne import MutationType
from bson import ObjectId
from datetime import datetime
from db.db import get_db

mutation_resolvers = MutationType()

@mutation_resolvers.field("createUser")
def resolve_create_user(_, info, name, email):
    db = get_db()
    
    # 이메일 중복 체크
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        raise Exception("이미 존재하는 이메일입니다.")
    
    user_data = {
        "name": name,
        "email": email,
        "createdAt": datetime.now().isoformat()
    }
    
    result = db.users.insert_one(user_data)
    user_data['id'] = str(result.inserted_id)
    
    return user_data

@mutation_resolvers.field("updateUser")
def resolve_update_user(_, info, id, **kwargs):
    db = get_db()
    
    try:
        update_data = {}
        if 'name' in kwargs and kwargs['name']:
            update_data['name'] = kwargs['name']
        if 'email' in kwargs and kwargs['email']:
            update_data['email'] = kwargs['email']
        
        if not update_data:
            raise Exception("업데이트할 데이터가 없습니다.")
        
        result = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise Exception("사용자를 찾을 수 없습니다.")
        
        # 업데이트된 사용자 반환
        user = db.users.find_one({"_id": ObjectId(id)})
        user['id'] = str(user['_id'])
        del user['_id']
        
        return user
    except Exception as e:
        print(f"사용자 업데이트 오류: {e}")
        raise Exception(f"사용자 업데이트 실패: {str(e)}")

@mutation_resolvers.field("deleteUser")
def resolve_delete_user(_, info, id):
    db = get_db()
    
    try:
        result = db.users.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"사용자 삭제 오류: {e}")
        return False