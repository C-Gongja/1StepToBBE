type User {
id: ID!
name: String!
email: String!
bio: String
avatar_url: String
is_verified: Boolean!
created_at: String!
}

type UserWithTodos {
id: ID!
name: String!
email: String!
todos: [Todo!]!
}

type Todo {
id: ID!
title: String!
description: String
status: TodoStatus!
user_id: ID!
created_at: String!
updated_at: String!
}

enum TodoStatus {
PENDING
IN_PROGRESS
COMPLETED
}

type Schedule {
id: ID!
title: String!
start_time: String!
end_time: String!
user_id: ID!
}
