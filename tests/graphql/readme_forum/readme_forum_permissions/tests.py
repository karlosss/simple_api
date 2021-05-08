import json

from django.contrib.auth.models import User

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
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type Mutation {
          UserCreate(data: UserCreateInput!): User!
          UserUpdate(data: UserUpdateInput!, id: Int!): User!
          UserDelete(id: Int!): Boolean!
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
          author: User!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input PostCreateInput {
          title: String!
          content: String!
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
          UserDetail(id: Int!): User!
          UserList(filters: UserFiltersInput): UserList!
          UserChangePassword(data: UserChangePasswordInput!): User!
          UserMyProfile: User!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
        
        type User {
          id: Int!
          username: String!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input UserChangePasswordInput {
          password: String!
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
          __str__: String!
        }
        
        input UserUpdateInput {
          username: String
        }
    """

    # anonymous user
    REF_META_SCHEMA = {
        "data": {
            "__types": [
                {
                    "typename": "UserFilters",
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
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "User",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "username",
                            "typename": "String!"
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
                            "typename": "User!"
                        }
                    ]
                }
            ],
            "__objects": [
                {
                    "name": "User",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "UserList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "UserFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[User]!",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "UserCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "username",
                                    "typename": "String!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "User!",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "UserChangePassword",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "password",
                                    "typename": "String!",
                                    "default": None
                                }
                            ],
                            "mutation": False,
                            "return_type": "User!",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "UserMyProfile",
                            "parameters": [],
                            "data": [],
                            "mutation": False,
                            "return_type": "User!",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
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
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
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
                                }
                            ],
                            "mutation": True,
                            "return_type": "Post!",
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

    def test_non_admin(self):
        user = User.objects.create_user(username="common", email="common@example.com")
        self._client.login(user=user)
        resp = self.query("""
        query{
          __objects{
            name
            pk_field
            actions{
              name
              permitted
              deny_reason
              retry_in
            }
          }
          __actions{
            name
            permitted
            deny_reason
            retry_in
          }
        }
        """)
        data = json.loads(resp.content)  # check what nonadmin can do with users
        for object in data["data"]["__objects"]:
            if object["name"] == "User":
                for action in object["actions"]:
                    if action["name"] == "UserList":
                        self.assertFalse(action["permitted"])
                    elif action["name"] == "UserCreate":
                        self.assertFalse(action["permitted"])
                    elif action["name"] == "UserChangePassword":
                        self.assertTrue(action["permitted"])
                    elif action["name"] == "UserMyProfile":
                        self.assertTrue(action["permitted"])
            if object["name"] == "Post":
                for action in object["actions"]:
                    if action["name"] == "PostList":
                        self.assertTrue(action["permitted"])
                    elif action["name"] == "PostCreate":
                        self.assertTrue(action["permitted"])

        self.query("""
        mutation post_create{
          PostCreate(data: {title: "A post", content: "Nothing here..."}){
            id
            title
            content
            author{
              username
            }
          }
        }
      """)

        resp = self.query("""
        query{
          PostList{
            data{
              id
              title
              author{
                username
              }
              content
              __actions{
                name
                permitted
              }
            }
          }
        }
      """)

        data = json.loads(resp.content)["data"]["PostList"]["data"]  # check what nonadmin can do with their posts
        for action in data[0]["__actions"]:
            self.assertTrue(action["permitted"])

        user2 = User.objects.create_user(username="common2", email="common2@example.com")
        self._client.login(user=user2)

        resp = self.query("""
        query{
          PostList{
            data{
              id
              title
              author{
                username
              }
              content
              __actions{
                name
                permitted
              }
            }
          }
        }
      """)

        data = json.loads(resp.content)["data"]["PostList"]["data"]  # check what nonadmin can do with not their posts
        for action in data[0]["__actions"]:
            if action["name"] == "PostDetail":
                self.assertTrue(action["permitted"])
            else:
                self.assertFalse(action["permitted"])

        resp = self.query("""
        query{
          UserMyProfile{
            id
            username
          }
        }
      """)

        exp = {"data": {"UserMyProfile": {"id": 2, "username": "common2"}}}

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_admin(self):
        admin = User.objects.create_user(username="admin", email="admin@example.com", is_staff=True)
        user = User.objects.create_user(username="common", email="common@example.com")

        # check if admin can delete someone else's post
        self._client.login(user=user)

        self.query("""
        mutation post_create{
          PostCreate(data: {title: "A post", content: "Nothing here..."}){
            id
            title
            content
            author{
              username
            }
          }
        }
      """)

        self._client.login(user=admin)

        resp = self.query("""
        query{
          PostList{
            data{
              id
              title
              author{
                username
              }
              content
              __actions{
                name
                permitted
              }
            }
          }
        }
      """)

        data = json.loads(resp.content)["data"]["PostList"]["data"]  # check what nonadmin can do with their posts
        for action in data[0]["__actions"]:
            self.assertTrue(action["permitted"])
