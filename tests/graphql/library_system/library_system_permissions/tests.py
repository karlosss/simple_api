from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
    schema {
      query: Query
      mutation: Mutation
    }
    
    type ActionInfo {
      name: String!
      permitted: Boolean!
      deny_reason: String
      retry_in: Duration
    }
    
    type Book {
      id: Int!
      author: String!
      title: String!
      ISBN: String!
      restricted: Boolean!
      borrowed: Boolean!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input BookCreateInput {
      author: String!
      title: String!
      ISBN: String!
      restricted: Boolean!
      borrowed: Boolean = false
    }
    
    input BookFiltersInput {
      id: Int
      id__exact: Int
      id__gt: Int
      id__gte: Int
      id__in: [Int!]
      id__isnull: Boolean
      id__lt: Int
      id__lte: Int
      author: String
      author__contains: String
      author__endswith: String
      author__exact: String
      author__icontains: String
      author__in: [String!]
      author__iregex: String
      author__isnull: Boolean
      author__regex: String
      author__startswith: String
      title: String
      title__contains: String
      title__endswith: String
      title__exact: String
      title__icontains: String
      title__in: [String!]
      title__iregex: String
      title__isnull: Boolean
      title__regex: String
      title__startswith: String
      ISBN: String
      ISBN__contains: String
      ISBN__endswith: String
      ISBN__exact: String
      ISBN__icontains: String
      ISBN__in: [String!]
      ISBN__iregex: String
      ISBN__isnull: Boolean
      ISBN__regex: String
      ISBN__startswith: String
      ordering: [String!]
    }
    
    input BookLendInput {
      author: String
      title: String
      ISBN: String
      restricted: Boolean
      borrowed: Boolean = false
    }
    
    type BookList {
      count: Int!
      data(limit: Int = 20, offset: Int = 0): [Book!]!
    }
    
    input BookUpdateInput {
      author: String
      title: String
      ISBN: String
      restricted: Boolean
      borrowed: Boolean = false
    }
    
    scalar Date
    
    scalar Duration
    
    type Mutation {
      BookCreate(data: BookCreateInput!): Book!
      BookUpdate(data: BookUpdateInput!, id: Int!): Book!
      BookDelete(id: Int!): Boolean!
      BookLend(data: BookLendInput!, id: Int!): Book!
      SubscriptionCreate(data: SubscriptionCreateInput!): Subscription!
      SubscriptionUpdate(data: SubscriptionUpdateInput!, id: Int!): Subscription!
      SubscriptionDelete(id: Int!): Boolean!
      UserCreate(data: UserCreateInput!): User!
      UserUpdate(data: UserUpdateInput!, id: Int!): User!
      UserDelete(id: Int!): Boolean!
    }
    
    type ObjectInfo {
      name: String!
      pk_field: String
      actions: [ActionInfo!]!
    }
    
    type Query {
      UserDetail(id: Int!): User!
      UserList(filters: UserFiltersInput): UserList!
      SubscriptionDetail(id: Int!): Subscription!
      SubscriptionList(filters: SubscriptionFiltersInput): SubscriptionList!
      BookDetail(id: Int!): Book!
      BookList(filters: BookFiltersInput): BookList!
      __objects: [ObjectInfo!]!
      __actions: [ActionInfo!]!
    }
    
    type Subscription {
      id: Int!
      start: Date!
      end: Date!
      user: User!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input SubscriptionCreateInput {
      start: Date!
      end: Date!
      user_id: Int!
    }
    
    input SubscriptionFiltersInput {
      id: Int
      id__exact: Int
      id__gt: Int
      id__gte: Int
      id__in: [Int!]
      id__isnull: Boolean
      id__lt: Int
      id__lte: Int
      user_id: Int
      user_id__exact: Int
      user_id__gt: Int
      user_id__gte: Int
      user_id__in: [Int!]
      user_id__isnull: Boolean
      user_id__lt: Int
      user_id__lte: Int
      ordering: [String!]
    }
    
    type SubscriptionList {
      count: Int!
      data(limit: Int = 20, offset: Int = 0): [Subscription!]!
    }
    
    input SubscriptionUpdateInput {
      start: Date
      end: Date
      user_id: Int
    }
    
    type User {
      id: Int!
      username: String!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input UserCreateInput {
      username: String!
    }
    
    input UserFiltersInput {
      id: Int
      id__exact: Int
      id__gt: Int
      id__gte: Int
      id__in: [Int!]
      id__isnull: Boolean
      id__lt: Int
      id__lte: Int
      username: String
      username__contains: String
      username__endswith: String
      username__exact: String
      username__icontains: String
      username__in: [String!]
      username__iregex: String
      username__isnull: Boolean
      username__regex: String
      username__startswith: String
      ordering: [String!]
    }
    
    type UserList {
      count: Int!
      data(limit: Int = 20, offset: Int = 0): [User!]!
    }
    
    input UserUpdateInput {
      username: String
    }
    """
    REF_META_SCHEMA = {
        "data": {
            "__objects": [
                {
                    "name": "Book",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "BookList",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookCreate",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "Subscription",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "SubscriptionList",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "SubscriptionCreate",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "User",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "UserList",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "UserCreate",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        }
                    ]
                }
            ],
            "__actions": []
        }
    }


