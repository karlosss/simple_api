from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


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
        
        scalar Duration
        
        type Mutation {
          ShortCustomUserCreate(data: ShortCustomUserCreateInput!): ShortCustomUser!
          ShortCustomUserUpdate(data: ShortCustomUserUpdateInput!, id: Int!): ShortCustomUser!
          ShortCustomUserDelete(id: Int!): Boolean!
          ShortPostCreate(data: ShortPostCreateInput!): ShortPost!
          ShortPostUpdate(data: ShortPostUpdateInput!, id: Int!): ShortPost!
          ShortPostDelete(id: Int!): Boolean!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          ShortPostDetail(id: Int!): ShortPost!
          ShortPostList(filters: ShortPostFiltersInput): ShortPostList!
          ShortCustomUserDetail(id: Int!): ShortCustomUser!
          ShortCustomUserList(filters: ShortCustomUserFiltersInput): ShortCustomUserList!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type ShortCustomUser {
          id: Int!
          first_name: String!
          last_name: String!
          full_name: String!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input ShortCustomUserCreateInput {
          first_name: String!
          last_name: String!
        }
        
        input ShortCustomUserFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          first_name: String
          first_name__contains: String
          first_name__endswith: String
          first_name__exact: String
          first_name__icontains: String
          first_name__in: [String!]
          first_name__iregex: String
          first_name__isnull: Boolean
          first_name__regex: String
          first_name__startswith: String
          last_name: String
          last_name__contains: String
          last_name__endswith: String
          last_name__exact: String
          last_name__icontains: String
          last_name__in: [String!]
          last_name__iregex: String
          last_name__isnull: Boolean
          last_name__regex: String
          last_name__startswith: String
          ordering: [String!]
        }
        
        type ShortCustomUserList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [ShortCustomUser!]!
        }
        
        input ShortCustomUserUpdateInput {
          first_name: String
          last_name: String
        }
        
        type ShortPost {
          id: Int!
          title: String!
          author: ShortCustomUser!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input ShortPostCreateInput {
          title: String!
          author_id: Int!
        }
        
        input ShortPostFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
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
          author_id: Int
          author_id__exact: Int
          author_id__gt: Int
          author_id__gte: Int
          author_id__in: [Int!]
          author_id__isnull: Boolean
          author_id__lt: Int
          author_id__lte: Int
          ordering: [String!]
        }
        
        type ShortPostList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [ShortPost!]!
        }
        
        input ShortPostUpdateInput {
          title: String
          author_id: Int
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "ShortCustomUser",
            "pk_field": "id",
            "actions": [
              {
                "name": "ShortCustomUserList",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "ShortCustomUserCreate",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              }
            ]
          },
          {
            "name": "ShortPost",
            "pk_field": "id",
            "actions": [
              {
                "name": "ShortPostList",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "ShortPostCreate",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              }
            ]
          }
        ],
        "__actions": []
      }
    }
