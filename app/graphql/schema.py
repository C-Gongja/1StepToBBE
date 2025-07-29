# app/graphql/schema.py
from ariadne import make_executable_schema
from app.graphql.resolvers.index import resolvers

# 기본 GraphQL 스키마 (schema 폴더가 없을 때 사용)
type_defs = """
    type Query {
        hello: String
        users: [User]
        user(id: ID!): User
    }
    
    type Mutation {
        createUser(name: String!, email: String!): User
        updateUser(id: ID!, name: String, email: String): User
        deleteUser(id: ID!): Boolean
    }
    
    type User {
        id: ID!
        name: String!
        email: String!
        createdAt: String
    }
"""

default_schema = make_executable_schema(type_defs, *resolvers)