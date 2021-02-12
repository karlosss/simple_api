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
      shelf: Int!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input BookCreateInput {
      author: String!
      title: String!
      ISBN: String!
      restricted: Boolean!
      shelf: Int!
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
      shelf: Int
      shelf__exact: Int
      shelf__gt: Int
      shelf__gte: Int
      shelf__in: [Int!]
      shelf__isnull: Boolean
      shelf__lt: Int
      shelf__lte: Int
      ordering: [String!]
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
      shelf: Int
    }
    
    scalar Duration
    
    type Mutation {
      BookCreate(data: BookCreateInput!): Book!
      BookUpdate(data: BookUpdateInput!, id: Int!): Book!
      BookDelete(id: Int!): Boolean!
    }
    
    type ObjectInfo {
      name: String!
      pk_field: String
      actions: [ActionInfo!]!
    }
    
    type Query {
      BookDetail(id: Int!): Book!
      BookList(filters: BookFiltersInput): BookList!
      BookGetById(id: Int!): Book!
      __objects: [ObjectInfo!]!
      __actions: [ActionInfo!]!
    }"""

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
                        },
                        {
                            "name": "BookGetById",
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
        resp = self.query("""mutation add_unrestricted_book {
          BookCreate(data: {author: "Karl Marx", title: "Das Kapital", ISBN: "123456789", restricted: false, shelf: 6}) {
            author
            title
            ISBN
            restricted
            shelf
          }
        }""")
        ret = {
            "data": {
                "BookCreate": {
                    "author": "Karl Marx",
                    "title": "Das Kapital",
                    "ISBN": "123456789",
                    "restricted": False,
                    "shelf": 6
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_restricted_book {
          BookCreate(data: {author: "Eliška Šestáková", title: "Automaty a Gramatiky", ISBN: "1337", restricted: true, shelf: 6}) {
            author
            title
            ISBN
            restricted
            shelf
          }
        }""")
        ret = {
            "data": {
                "BookCreate": {
                    "author": "Eliška Šestáková",
                    "title": "Automaty a Gramatiky",
                    "ISBN": "1337",
                    "restricted": True,
                    "shelf": 6
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query getByID {
          BookGetById(id: -1) {
            id
            author
            title
            shelf
          }
        }""")
        ret = {
            "errors": [
                {
                    "message": "Validation failed in NotNegative",
                    "locations": [
                        {
                            "line": 2,
                            "column": 11
                        }
                    ],
                    "path": [
                        "BookGetById"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query getByID {
          BookGetById(id: 0) {
            id
            author
            title
            shelf
          }
        }""")
        ret = {
            "errors": [
                {
                    "message": "Validation failed in NotZero",
                    "locations": [
                        {
                            "line": 2,
                            "column": 11
                        }
                    ],
                    "path": [
                        "BookGetById"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query getByID {
                  BookGetById(id: 1) {
                    id
                    author
                    title
                    shelf
                  }
                }""")
        ret = {
            "data": {
                "BookGetById": {
                    "id": 1,
                    "author": "Karl Marx",
                    "title": "Das Kapital",
                    "shelf": 6
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query getByID {
                  BookGetById(id: 2) {
                    id
                    author
                    title
                    shelf
                  }
                }""")
        ret = {
            "errors": [
                {
                    "message": "Only not restricted books can be accessed",
                    "locations": [
                        {
                            "line": 2,
                            "column": 19
                        }
                    ],
                    "path": [
                        "BookGetById"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
