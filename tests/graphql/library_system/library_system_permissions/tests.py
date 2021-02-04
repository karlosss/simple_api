import json

from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase
from django.contrib.auth.models import User


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
      BookRead(id: Int!): Book!
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
    # Anonymous
    REF_META_SCHEMA = {
        "data": {
            "__objects": [
                {
                    "name": "Book",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "BookList",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "BookCreate",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
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
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
                            "retry_in": None
                        },
                        {
                            "name": "SubscriptionCreate",
                            "permitted": False,
                            "deny_reason": "You do not have permission to access this.",
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

    def _prepare_books(self):
        admin = User.objects.create_user(username="bookMaker", email="bookMaker@example.com", is_staff=True)
        self._client.login(user=admin)
        resp = self.query("""
        mutation add_book {
            BookCreate(data: {author: "Karl Marx", title: "Das Kapital", ISBN: "123456789", restricted: false}) {
                author
                title
                ISBN
                restricted
              }
            }""")
        ret = {"data": {
            "BookCreate": {"author": "Karl Marx", "title": "Das Kapital", "ISBN": "123456789", "restricted": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                mutation add_book {
                    BookCreate(data: {author: "Ayn Rand", title: "Atlas shrugged", ISBN: "7734", restricted: true}) {
                        author
                        title
                        ISBN
                        restricted
                        borrowed
                      }
                    }""")
        ret = {"data": {
            "BookCreate": {"author": "Ayn Rand", "title": "Atlas shrugged", "ISBN": "7734", "restricted": True,
                           "borrowed": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        self._client.logout()


    def test_admin(self):
        admin = User.objects.create_user(username="admin", email="admin@example.com", is_staff=True)
        self._client.login(user=admin)
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
        ret = {
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
                                "permitted": True,
                                "deny_reason": None,
                                "retry_in": None
                            },
                            {
                                "name": "UserCreate",
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
        self.assertResponseNoErrors(resp)

        # ignore the order of the elements
        data = json.loads(resp.content)
        self.assertJSONEqualArraysShuffled(data, ret)
        self._client.logout()
        self._prepare_books()
        self._client.login(user=admin)

        resp = self.query("""
            mutation lend_book {
              BookLend(id: 1, data: {}) {
                id
                title
                author
                borrowed
              }
            }""")
        ret = {"data": {
            "BookLend": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": True}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""
            mutation lend_book {
              BookLend(id: 2, data: {}) {
                id
                title
                author
                borrowed
              }
            }""")
        ret = {"data": {
            "BookLend": {"id": 2, "title": "Atlas shrugged", "author": "Ayn Rand", "borrowed": True}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                    mutation lend_book {
                      BookLend(id: 1, data: {}) {
                        id
                        title
                        author
                        borrowed
                      }
                    }""")
        ret = {"data": {
            "BookLend": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""
                    mutation lend_book {
                      BookLend(id: 2, data: {}) {
                        id
                        title
                        author
                        borrowed
                      }
                    }""")
        ret = {"data": {
            "BookLend": {"id": 2, "title": "Atlas shrugged", "author": "Ayn Rand", "borrowed": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""
                            query read_book {
                              BookRead(id: 1) {
                                id
                                title
                                author
                                borrowed
                              }
                            }""")
        ret = {"data": {
            "BookRead": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                                    query read_book {
                                      BookRead(id: 2) {
                                        id
                                        title
                                        author
                                        borrowed
                                      }
                                    }""")
        ret = {"errors": [{"message": "Restricted books cannot be accessed.", "locations": [{"line": 3, "column": 39}],
                           "path": ["BookRead"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        self.client.logout()

    def test_notAdmin(self):
        self._prepare_books()
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
        ret = {
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
                                "permitted": False,
                                "deny_reason": "You do not have permission to access this.",
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
                                "permitted": False,
                                "deny_reason": "You do not have permission to access this.",
                                "retry_in": None
                            },
                            {
                                "name": "SubscriptionCreate",
                                "permitted": False,
                                "deny_reason": "You do not have permission to access this.",
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

        self.assertResponseNoErrors(resp)

        # ignore the order of the elements
        data = json.loads(resp.content)
        self.assertJSONEqualArraysShuffled(data, ret)

        resp = self.query("""
                    mutation lend_book {
                      BookLend(id: 1, data: {}) {
                        id
                        title
                        author
                        borrowed
                      }
                    }""")
        ret = {"data": {
            "BookLend": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": True}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""
                    mutation lend_book {
                      BookLend(id: 2, data: {}) {
                        id
                        title
                        author
                        borrowed
                      }
                    }""")
        ret = {"errors": [
            {"message": "You do not have permission to access this.", "locations": [{"line": 3, "column": 23}],
             "path": ["BookLend"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                                    query read_book {
                                      BookRead(id: 1) {
                                        id
                                        title
                                        author
                                        borrowed
                                      }
                                    }""")
        ret = {"data": {
            "BookRead": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": True}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query read_book {
                               BookRead(id: 2) {
                                 id
                                 title
                                 author
                                 borrowed
                               }
                            }""")
        ret = {"errors": [{"message": "Restricted books cannot be accessed.", "locations": [{"line": 2, "column": 32}],
                           "path": ["BookRead"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        self.client.logout()

    def test_anonymous(self):
        self._prepare_books()
        resp = self.query("""mutation lend_book {
                                      BookLend(id: 1, data: {}) {
                                        id
                                        title
                                        author
                                        borrowed
                                      }
                                    }""")
        ret = {"errors": [
            {"message": "You do not have permission to access this.", "locations": [{"line": 2, "column": 39}],
             "path": ["BookLend"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""mutation lend_book {
                                      BookLend(id: 2, data: {}) {
                                        id
                                        title
                                        author
                                        borrowed
                                      }
                                    }""")
        ret = {"errors": [
            {"message": "You do not have permission to access this.", "locations": [{"line": 2, "column": 39}],
             "path": ["BookLend"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                                                    query read_book {
                                                      BookRead(id: 1) {
                                                        id
                                                        title
                                                        author
                                                        borrowed
                                                      }
                                                    }""")
        ret = {"data": {
            "BookRead": {"id": 1, "title": "Das Kapital", "author": "Karl Marx", "borrowed": False}}
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query read_book {
                                               BookRead(id: 2) {
                                                 id
                                                 title
                                                 author
                                                 borrowed
                                               }
                                            }""")
        ret = {"errors": [{"message": "Restricted books cannot be accessed.", "locations": [{"line": 2, "column": 48}],
                           "path": ["BookRead"]}], "data": None}
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
