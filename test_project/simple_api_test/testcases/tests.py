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
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
        }
        
        scalar Duration
        
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
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
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
        }
        
        input UserUpdateInput {
          username: String
        }
    """

    # anonymous user
    REF_META_SCHEMA = {
      "data": {
        "__objects": [
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
              },
              {
                "name": "UserChangePassword",
                "permitted": False,
                "deny_reason": "You do not have permission to access this.",
                "retry_in": None
              },
              {
                "name": "UserMyProfile",
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
                "permitted": False,
                "deny_reason": "You do not have permission to access this.",
                "retry_in": None
              },
              {
                "name": "PostCreate",
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

      exp = {"data":{"UserMyProfile":{"id":2,"username":"common2"}}}

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
