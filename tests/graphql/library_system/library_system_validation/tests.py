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
      shelf: Int!
      bookmark_set(filters: BookmarkFiltersInput): BookmarkList!
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
    
    input BookGetById2Input {
      Title: String!
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
    
    type Bookmark {
      id: Int!
      page: Int!
      book: Book!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input BookmarkCreateInput {
      page: Int!
      book_id: Int!
    }
    
    input BookmarkFiltersInput {
      id: Int
      id__exact: Int
      id__gt: Int
      id__gte: Int
      id__in: [Int!]
      id__isnull: Boolean
      id__lt: Int
      id__lte: Int
      page: Int
      page__exact: Int
      page__gt: Int
      page__gte: Int
      page__in: [Int!]
      page__isnull: Boolean
      page__lt: Int
      page__lte: Int
      book_id: Int
      book_id__exact: Int
      book_id__gt: Int
      book_id__gte: Int
      book_id__in: [Int!]
      book_id__isnull: Boolean
      book_id__lt: Int
      book_id__lte: Int
      ordering: [String!]
    }
    
    type BookmarkList {
      count: Int!
      data(limit: Int = 20, offset: Int = 0): [Bookmark!]!
    }
    
    input BookmarkUpdateInput {
      page: Int
      book_id: Int
    }
    
    scalar Duration
    
    type Mutation {
      BookCreate(data: BookCreateInput!): Book!
      BookUpdate(data: BookUpdateInput!, id: Int!): Book!
      BookDelete(id: Int!): Boolean!
      BookmarkCreate(data: BookmarkCreateInput!): Bookmark!
      BookmarkUpdate(data: BookmarkUpdateInput!, id: Int!): Bookmark!
      BookmarkDelete(id: Int!): Boolean!
    }
    
    type ObjectInfo {
      name: String!
      pk_field: String
      actions: [ActionInfo!]!
    }
    
    type Query {
      BookmarkDetail(id: Int!): Bookmark!
      BookmarkList(filters: BookmarkFiltersInput): BookmarkList!
      BookDetail(id: Int!): Book!
      BookList(filters: BookFiltersInput): BookList!
      BookGetById(id: Int!): Book!
      BookGetById2(id: Int!, data: BookGetById2Input!): Book!
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
                        },
                        {
                            "name": "BookGetById2",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "Bookmark",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "BookmarkList",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookmarkCreate",
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
          BookCreate(data: {author: "Eliška Šestáková", title: "Automaty a Gramatiky", ISBN: "1337", restricted: true, shelf: 8}) {
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
                    "shelf": 8
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
        resp = self.query("""query getByID2 {
          BookGetById2(id: 1, data: {Title: "Kapital test string"}) {
            id
            author
            title
          }
        }""")
        ret = {
            "data": {
                "BookGetById2": {
                    "id": 1,
                    "author": "Karl Marx",
                    "title": "Das Kapital"
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""query getByID2 {
                  BookGetById2(id: -1, data: {Title: "Kapital test string"}) {
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
                            "column": 19
                        }
                    ],
                    "path": [
                        "BookGetById2"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""query getByID2 {
                  BookGetById2(id: 1, data: {Title: "KO"}) {
                    id
                    author
                    title
                    shelf
                  }
                }""")
        ret = {
            "errors": [
                {
                    "message": "Search term must be at least 4 characters",
                    "locations": [
                        {
                            "line": 2,
                            "column": 19
                        }
                    ],
                    "path": [
                        "BookGetById2"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_bad_shelf_book {
          BookCreate(data: {author: "Eliška Šestáková", title: "Automaty a Gramatiky", ISBN: "1337", restricted: true, shelf: 7}) {
            author
            title
            ISBN
            restricted
            shelf
          }
        }""")
        ret = {
            "errors": [
                {
                    "message": "Django validator error",
                    "locations": [
                        {
                            "line": 2,
                            "column": 11
                        }
                    ],
                    "path": [
                        "BookCreate"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_bookmark {
          BookmarkCreate(data: {book_id: 4, page: 111}) {
            book {
              id
            }
          }
        }""")
        ret = {
            "errors": [
                {
                    "message": "Error: Referenced object doesn't exist",
                    "locations": [
                        {
                            "line": 2,
                            "column": 11
                        }
                    ],
                    "path": [
                        "BookmarkCreate"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_bookmark {
                  BookmarkCreate(data: {book_id: 1, page: 123}) {
                    page
                    book {
                      id
                      title
                      author
                    }
                  }
                }""")
        ret = {
            "data": {
                "BookmarkCreate": {
                    "page": 123,
                    "book": {
                        "id": 1,
                        "title": "Das Kapital",
                        "author": "Karl Marx"
                    }
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
