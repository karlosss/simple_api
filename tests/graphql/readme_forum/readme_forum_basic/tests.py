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
        
        type Mutation {
          CustomUserCreate(data: CustomUserCreateInput!): CustomUser!
          CustomUserUpdate(data: CustomUserUpdateInput!, id: Int!): CustomUser!
          CustomUserDelete(id: Int!): Boolean!
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
          author: CustomUser!
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
        }
        
        input PostUpdateInput {
          title: String
          content: String
          author_id: Int
        }
        
        type Query {
          PostDetail(id: Int!): Post!
          PostList(filters: PostFiltersInput): PostList!
          CustomUserDetail(id: Int!): CustomUser!
          CustomUserList(filters: CustomUserFiltersInput): CustomUserList!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "CustomUser",
            "pk_field": "id",
            "actions": [
              {
                "name": "CustomUserList",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "CustomUserCreate",
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
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "PostCreate",
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

    def test_requests(self):
      resp = self.query("""
      mutation create_user{
        CustomUserCreate(data: {
          email: "user1@example.com", 
          username: "adam", 
          first_name: "Adam", 
          last_name: "First", 
          password: "secret",
          bio: "Just an ordinary person...",
        }){
          id
          email
          username
          first_name
          last_name
          password
          bio
          is_admin
        }
      }
      """)
      exp = {
        "data": {
          "CustomUserCreate": {
            "id": 1,
            "email": "user1@example.com",
            "username": "adam",
            "first_name": "Adam",
            "last_name": "First",
            "password": "secret",
            "bio": "Just an ordinary person...",
            "is_admin": False
          }
        }
      }
      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      resp = self.query("""
      query detail_of_user{
        CustomUserDetail(id: 1){
          id
          email
          username
          first_name
          last_name
          password
          bio
          is_admin
        }
      }
      """)

      exp = {
          "data": {
            "CustomUserDetail": {
              "id": 1,
              "email": "user1@example.com",
              "username": "adam",
              "first_name": "Adam",
              "last_name": "First",
              "password": "secret",
              "bio": "Just an ordinary person...",
              "is_admin": False
            }
          }
      }
      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      self.query("""
      mutation create_another_user{
        CustomUserCreate(data: {
          email: "user2@example.com", 
          username: "bob", 
          first_name: "Bob", 
          last_name: "Second", 
          password: "secret",
          bio: "Just another ordinary person...",
        }){
          id
          email
          username
          first_name
          last_name
          password
          bio
          is_admin
        }
      }
      """)

      resp = self.query("""
      query list_users{
        CustomUserList{
          count
          data{
            id
            first_name
            last_name
          }
        }
      }
      """)

      exp = {
        "data": {
          "CustomUserList": {
            "count": 2,
            "data": [
              {
                "id": 1,
                "first_name": "Adam",
                "last_name": "First"
              },
              {
                "id": 2,
                "first_name": "Bob",
                "last_name": "Second"
              }
            ]
          }
        }
      }
      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      resp = self.query("""
      query list_filtered_users{
        CustomUserList(filters: {first_name__startswith: "A"}){
          count
          data{
            id
            first_name
            last_name
          }
        }
      }
      """)

      exp = {
        "data": {
          "CustomUserList": {
            "count": 1,
            "data": [
              {
                "id": 1,
                "first_name": "Adam",
                "last_name": "First"
              }
            ]
          }
        }
      }

      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      resp = self.query("""
        query list_ordering_users{
          CustomUserList(filters: {ordering: ["password","-id"]}){
            count
            data{
              id
              first_name
              last_name
            }
          }
        }
        """)

      exp = {
        "data": {
          "CustomUserList": {
            "count": 2,
            "data": [
              {
                "id": 2,
                "first_name": "Bob",
                "last_name": "Second"
              },
              {
                "id": 1,
                "first_name": "Adam",
                "last_name": "First"
              }
            ]
          }
        }
      }

      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      resp = self.query("""
      query list_paginate_users{
        CustomUserList{
          count
          data(offset: 1, limit: 1){
            id
            first_name
            last_name
          }
        }
      }
      """)

      exp = {
        "data": {
          "CustomUserList": {
            "count": 2,
            "data": [
              {
                "id": 2,
                "first_name": "Bob",
                "last_name": "Second"
              }
            ]
          }
        }
      }

      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)

      self.query("""
      mutation update_password{
        CustomUserUpdate(id: 1, data: {password: "moresecret"}){
          id
          password
        }
      }
      """)

      self.query("""
      mutation delete_user{
        CustomUserDelete(id: 2)
      }
      """)

      resp = self.query("""
      query list_users_with_password{
        CustomUserList{
          count
          data{
            id
            first_name
            last_name
            password
          }
        }
      }
      """)

      exp = {
        "data": {
          "CustomUserList": {
            "count": 1,
            "data": [
              {
                "id": 1,
                "first_name": "Adam",
                "last_name": "First",
                "password": "moresecret"
              }
            ]
          }
        }
      }

      self.assertResponseNoErrors(resp)
      self.assertJSONEqual(resp.content, exp)
