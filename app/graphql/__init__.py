# app/graphql/__init__.py
from ariadne import make_executable_schema, load_schema_from_path, graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from app.graphql.resolvers.index import resolvers
from db.db import get_db


def setup_graphql(app):
  """GraphQL endpoint settings"""
  # schema road
  type_defs = load_schema_from_path("app/graphql/schema")
  schema = make_executable_schema(type_defs, *resolvers)

  explorer_html = ExplorerGraphiQL().html(None)

  """GraphQL req"""
  def graphql_view():
    if request.method == "GET":
      return explorer_html

    # JWT 토큰 검증 (선택적)
    current_user = None
    try:
      verify_jwt_in_request(optional=True)
      current_user = get_jwt_identity()
    except:
      pass  # 토큰이 없어도 공개 쿼리는 허용

    data = request.get_json()

    success, result = graphql_sync(
      schema,
      data,
      context_value={
        "request": request,
        "db": get_db(),
        "current_user": current_user,  # JWT 사용자 정보
      },
      debug=app.debug,
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

  app.add_url_rule("/graphql", view_func=graphql_view, methods=["GET", "POST"])


# 📊 요청 처리 흐름 예시:
"""
1. 클라이언트: POST /graphql { "query": "{ users { id name } }" }
2. Flask: graphql_view() 함수 실행
3. Ariadne: 쿼리 파싱 → 스키마 검증 → 리졸버 호출
4. 리졸버: resolve_users() 실행 → DB 조회
5. 결과: JSON 응답 반환
"""
