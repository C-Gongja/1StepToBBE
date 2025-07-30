from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from db.db import get_db

user_bp = Blueprint('user', __name__)

@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """⭐ 사용자 정보 수정 - REST API로 처리하는 이유:
    - 명확한 HTTP 동사 사용 (PUT)
    - 권한 확인 필요
    - 부분 업데이트 로직
    """
    
    current_user_id = get_jwt_identity()
    
    # 본인만 수정 가능
    if current_user_id != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    db = get_db()
    update_data = request.get_json()
    
    # 허용된 필드만 업데이트
    allowed_fields = ['name', 'bio', 'avatar_url']
    filtered_data = {k: v for k, v in update_data.items() if k in allowed_fields}
    
    if not filtered_data:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    result = db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': filtered_data}
    )
    
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'message': 'User updated successfully',
        'updated_fields': list(filtered_data.keys())
    })

@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """⭐ 사용자 삭제 - REST API가 적합한 이유:
    - 명확한 HTTP 동사 (DELETE)
    - 권한 확인
    - 관련 데이터 정리 필요
    """
    
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    db = get_db()
    
    # 트랜잭션으로 관련 데이터 함께 삭제
    with db.client.start_session() as session:
        with session.start_transaction():
            # 사용자 삭제
            user_result = db.users.delete_one({'_id': ObjectId(user_id)})
            
            # 관련 데이터 삭제
            db.todos.delete_many({'user_id': user_id})
            db.schedules.delete_many({'user_id': user_id})
            db.streaks.delete_many({'user_id': user_id})
    
    return jsonify({'message': 'User deleted successfully'}), 200