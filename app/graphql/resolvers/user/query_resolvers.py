from ariadne import QueryType
from bson import ObjectId
from db.db import get_db

query_resolvers = QueryType()


@query_resolvers.field("test")
def resolve_test(obj, info):
    return {
        "id": 0,
        "test": {"id": 0, "text": ["Testing GraphQL!", "Hello GraphQL!", "W GraphQL!"]},
    }


@query_resolvers.field("user")
def resolve_user(_, info, id):
    """⭐ 사용자 조회 - GraphQL로 처리하는 이유:
    - 필요한 필드만 선택적으로 가져올 수 있음
    - 관련 데이터를 한 번에 조회 가능 (N+1 문제 해결)
    - 복잡한 중첩 쿼리 지원
    """

    db = info.context["db"]

    try:
        user = db.users.find_one({"_id": ObjectId(id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            # 비밀번호 해시는 제외
            user.pop("password_hash", None)
            return user
        return None
    except Exception as e:
        raise Exception(f"사용자 조회 실패: {str(e)}")


# @query_resolvers.field("users")
# def resolve_users(_, info, limit=10, offset=0):
#     """⭐ 사용자 목록 조회 - GraphQL이 유리한 이유:
#     - 페이지네이션 + 필드 선택
#     - 복잡한 필터링 조건
#     - 관련 데이터와 조인
#     """

#     db = info.context["db"]

#     users = list(db.users.find().skip(offset).limit(limit))

#     for user in users:
#         user["id"] = str(user["_id"])
#         del user["_id"]
#         user.pop("password_hash", None)

#     return users


# @query_resolvers.field("userWithTodos")
# def resolve_user_with_todos(_, info, user_id):
#     """⭐ 사용자와 관련 데이터 함께 조회 - GraphQL의 핵심 장점!
#     REST API라면 여러 번 요청해야 하는 데이터를 한 번에 가져옴
#     """

#     db = info.context["db"]

#     # 사용자 기본 정보
#     user = db.users.find_one({"_id": ObjectId(user_id)})
#     if not user:
#         return None

#     user["id"] = str(user["_id"])
#     del user["_id"]
#     user.pop("password_hash", None)

#     # 사용자의 할일 목록도 함께 조회
#     todos = list(db.todos.find({"user_id": user_id}))
#     for todo in todos:
#         todo["id"] = str(todo["_id"])
#         del todo["_id"]

#     user["todos"] = todos
#     return user
