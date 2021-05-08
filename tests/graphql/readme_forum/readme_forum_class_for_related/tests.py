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
          parameters: [FieldInfo!]!
          data: [FieldInfo!]!
          return_type: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
          mutation: Boolean!
          __str__: String!
        }
        
        type CustomUser {
          id: Int!
          email: String!
          username: String!
          first_name: String!
          last_name: String!
          password: String!
          bio: String!
          is_admin: Boolean!
          post_set(filters: PostFiltersInput): PostList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input CustomUserCreateInput {
          email: String!
          username: String!
          first_name: String!
          last_name: String!
          password: String!
          bio: String!
          is_admin: Boolean = false
        }
        
        input CustomUserFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          email: String
          email__contains: String
          email__endswith: String
          email__exact: String
          email__icontains: String
          email__in: [String!]
          email__iregex: String
          email__isnull: Boolean
          email__regex: String
          email__startswith: String
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
          password: String
          password__contains: String
          password__endswith: String
          password__exact: String
          password__icontains: String
          password__in: [String!]
          password__iregex: String
          password__isnull: Boolean
          password__regex: String
          password__startswith: String
          bio: String
          bio__contains: String
          bio__endswith: String
          bio__exact: String
          bio__icontains: String
          bio__in: [String!]
          bio__iregex: String
          bio__isnull: Boolean
          bio__regex: String
          bio__startswith: String
          ordering: [String!]
        }
        
        type CustomUserList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [CustomUser!]!
          __str__: String!
        }
        
        type CustomUserPublic {
          id: Int!
          username: String!
          first_name: String!
          last_name: String!
          bio: String!
          is_admin: Boolean!
          post_set(filters: PostFiltersInput): PostList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input CustomUserPublicCreateInput {
          username: String!
          first_name: String!
          last_name: String!
          bio: String!
          is_admin: Boolean = false
        }
        
        input CustomUserPublicFiltersInput {
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
          bio: String
          bio__contains: String
          bio__endswith: String
          bio__exact: String
          bio__icontains: String
          bio__in: [String!]
          bio__iregex: String
          bio__isnull: Boolean
          bio__regex: String
          bio__startswith: String
          ordering: [String!]
        }
        
        type CustomUserPublicList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [CustomUserPublic!]!
          __str__: String!
        }
        
        input CustomUserPublicUpdateInput {
          username: String
          first_name: String
          last_name: String
          bio: String
          is_admin: Boolean = false
        }
        
        input CustomUserUpdateInput {
          email: String
          username: String
          first_name: String
          last_name: String
          password: String
          bio: String
          is_admin: Boolean = false
        }
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type Mutation {
          CustomUserCreate(data: CustomUserCreateInput!): CustomUser!
          CustomUserUpdate(data: CustomUserUpdateInput!, id: Int!): CustomUser!
          CustomUserDelete(id: Int!): Boolean!
          CustomUserPublicCreate(data: CustomUserPublicCreateInput!): CustomUserPublic!
          CustomUserPublicUpdate(data: CustomUserPublicUpdateInput!, id: Int!): CustomUserPublic!
          CustomUserPublicDelete(id: Int!): Boolean!
          PostCreate(data: PostCreateInput!): Post!
          PostUpdate(data: PostUpdateInput!, id: Int!): Post!
          PostDelete(id: Int!): Boolean!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Post {
          id: Int!
          title: String!
          content: String!
          author: CustomUserPublic!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input PostCreateInput {
          title: String!
          content: String!
          author_id: Int!
        }
        
        input PostFiltersInput {
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
          content: String
          content__contains: String
          content__endswith: String
          content__exact: String
          content__icontains: String
          content__in: [String!]
          content__iregex: String
          content__isnull: Boolean
          content__regex: String
          content__startswith: String
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
        
        type PostList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [Post!]!
          __str__: String!
        }
        
        input PostUpdateInput {
          title: String
          content: String
          author_id: Int
        }
        
        type Query {
          PostDetail(id: Int!): Post!
          PostList(filters: PostFiltersInput): PostList!
          CustomUserPublicDetail(id: Int!): CustomUserPublic!
          CustomUserPublicList(filters: CustomUserPublicFiltersInput): CustomUserPublicList!
          CustomUserDetail(id: Int!): CustomUser!
          CustomUserList(filters: CustomUserFiltersInput): CustomUserList!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
    """

    REF_META_SCHEMA = {
        "data": {
            "__types": [
                {
                    "typename": "CustomUserFilters",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "email",
                            "typename": "String"
                        },
                        {
                            "name": "email__contains",
                            "typename": "String"
                        },
                        {
                            "name": "email__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "email__exact",
                            "typename": "String"
                        },
                        {
                            "name": "email__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "email__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "email__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "email__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "email__regex",
                            "typename": "String"
                        },
                        {
                            "name": "email__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "username",
                            "typename": "String"
                        },
                        {
                            "name": "username__contains",
                            "typename": "String"
                        },
                        {
                            "name": "username__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "username__exact",
                            "typename": "String"
                        },
                        {
                            "name": "username__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "username__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "username__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "username__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "username__regex",
                            "typename": "String"
                        },
                        {
                            "name": "username__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "first_name",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__contains",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__exact",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "first_name__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "first_name__regex",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "last_name",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__contains",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__exact",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "last_name__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "last_name__regex",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "password",
                            "typename": "String"
                        },
                        {
                            "name": "password__contains",
                            "typename": "String"
                        },
                        {
                            "name": "password__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "password__exact",
                            "typename": "String"
                        },
                        {
                            "name": "password__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "password__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "password__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "password__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "password__regex",
                            "typename": "String"
                        },
                        {
                            "name": "password__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "bio",
                            "typename": "String"
                        },
                        {
                            "name": "bio__contains",
                            "typename": "String"
                        },
                        {
                            "name": "bio__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "bio__exact",
                            "typename": "String"
                        },
                        {
                            "name": "bio__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "bio__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "bio__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "bio__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "bio__regex",
                            "typename": "String"
                        },
                        {
                            "name": "bio__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "CustomUser",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "email",
                            "typename": "String!"
                        },
                        {
                            "name": "username",
                            "typename": "String!"
                        },
                        {
                            "name": "first_name",
                            "typename": "String!"
                        },
                        {
                            "name": "last_name",
                            "typename": "String!"
                        },
                        {
                            "name": "password",
                            "typename": "String!"
                        },
                        {
                            "name": "bio",
                            "typename": "String!"
                        },
                        {
                            "name": "is_admin",
                            "typename": "Boolean!"
                        },
                        {
                            "name": "post_set",
                            "typename": "Paginated[Post]!"
                        }
                    ]
                },
                {
                    "typename": "CustomUserPublicFilters",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "username",
                            "typename": "String"
                        },
                        {
                            "name": "username__contains",
                            "typename": "String"
                        },
                        {
                            "name": "username__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "username__exact",
                            "typename": "String"
                        },
                        {
                            "name": "username__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "username__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "username__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "username__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "username__regex",
                            "typename": "String"
                        },
                        {
                            "name": "username__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "first_name",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__contains",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__exact",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "first_name__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "first_name__regex",
                            "typename": "String"
                        },
                        {
                            "name": "first_name__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "last_name",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__contains",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__exact",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "last_name__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "last_name__regex",
                            "typename": "String"
                        },
                        {
                            "name": "last_name__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "bio",
                            "typename": "String"
                        },
                        {
                            "name": "bio__contains",
                            "typename": "String"
                        },
                        {
                            "name": "bio__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "bio__exact",
                            "typename": "String"
                        },
                        {
                            "name": "bio__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "bio__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "bio__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "bio__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "bio__regex",
                            "typename": "String"
                        },
                        {
                            "name": "bio__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "CustomUserPublic",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "username",
                            "typename": "String!"
                        },
                        {
                            "name": "first_name",
                            "typename": "String!"
                        },
                        {
                            "name": "last_name",
                            "typename": "String!"
                        },
                        {
                            "name": "bio",
                            "typename": "String!"
                        },
                        {
                            "name": "is_admin",
                            "typename": "Boolean!"
                        },
                        {
                            "name": "post_set",
                            "typename": "Paginated[Post]!"
                        }
                    ]
                },
                {
                    "typename": "PostFilters",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "title",
                            "typename": "String"
                        },
                        {
                            "name": "title__contains",
                            "typename": "String"
                        },
                        {
                            "name": "title__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "title__exact",
                            "typename": "String"
                        },
                        {
                            "name": "title__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "title__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "title__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "title__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "title__regex",
                            "typename": "String"
                        },
                        {
                            "name": "title__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "content",
                            "typename": "String"
                        },
                        {
                            "name": "content__contains",
                            "typename": "String"
                        },
                        {
                            "name": "content__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "content__exact",
                            "typename": "String"
                        },
                        {
                            "name": "content__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "content__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "content__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "content__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "content__regex",
                            "typename": "String"
                        },
                        {
                            "name": "content__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "author_id",
                            "typename": "Integer"
                        },
                        {
                            "name": "author_id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "author_id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "author_id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "author_id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "author_id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "author_id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "author_id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "Post",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "title",
                            "typename": "String!"
                        },
                        {
                            "name": "content",
                            "typename": "String!"
                        },
                        {
                            "name": "author",
                            "typename": "CustomUserPublic!"
                        }
                    ]
                }
            ],
            "__objects": [
                {
                    "name": "CustomUser",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "CustomUserList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "CustomUserFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[CustomUser]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "CustomUserCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "email",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "username",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "first_name",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "last_name",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "password",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "bio",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "is_admin",
                                    "typename": "Boolean!",
                                    "default": "false"
                                }
                            ],
                            "mutation": True,
                            "return_type": "CustomUser!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "CustomUserPublic",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "CustomUserPublicList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "CustomUserPublicFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[CustomUserPublic]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "CustomUserPublicCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "username",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "first_name",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "last_name",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "bio",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "is_admin",
                                    "typename": "Boolean!",
                                    "default": "false"
                                }
                            ],
                            "mutation": True,
                            "return_type": "CustomUserPublic!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "Post",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "PostList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "PostFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[Post]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "PostCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "title",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "content",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "author_id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "Post!",
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
