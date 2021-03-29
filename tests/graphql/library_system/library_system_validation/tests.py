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
      parameters: [FieldInfo!]!
      data: [FieldInfo!]!
      return_type: String!
      permitted: Boolean!
      deny_reason: String
      retry_in: Duration
      mutation: Boolean!
      __str__: String!
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
      __str__: String!
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
      __str__: String!
    }
    
    input BookmarkUpdateInput {
      page: Int
      book_id: Int
    }
    
    scalar Duration
    
    type FieldInfo {
      name: String!
      typename: String!
      default: String
      __str__: String!
    }
    
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
      __str__: String!
    }
    
    type Query {
      BookmarkDetail(id: Int!): Bookmark!
      BookmarkList(filters: BookmarkFiltersInput): BookmarkList!
      BookDetail(id: Int!): Book!
      BookList(filters: BookFiltersInput): BookList!
      BookGetById(id: Int!): Book!
      BookGetById2(id: Int!, data: BookGetById2Input!): Book!
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
                    "typename": "BookFilters",
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
                            "name": "author",
                            "typename": "String"
                        },
                        {
                            "name": "author__contains",
                            "typename": "String"
                        },
                        {
                            "name": "author__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "author__exact",
                            "typename": "String"
                        },
                        {
                            "name": "author__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "author__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "author__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "author__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "author__regex",
                            "typename": "String"
                        },
                        {
                            "name": "author__startswith",
                            "typename": "String"
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
                            "name": "ISBN",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__contains",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__endswith",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__exact",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__icontains",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__in",
                            "typename": "[String!]"
                        },
                        {
                            "name": "ISBN__iregex",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "ISBN__regex",
                            "typename": "String"
                        },
                        {
                            "name": "ISBN__startswith",
                            "typename": "String"
                        },
                        {
                            "name": "shelf",
                            "typename": "Integer"
                        },
                        {
                            "name": "shelf__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "shelf__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "shelf__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "shelf__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "shelf__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "shelf__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "shelf__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "Book",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "author",
                            "typename": "String!"
                        },
                        {
                            "name": "title",
                            "typename": "String!"
                        },
                        {
                            "name": "ISBN",
                            "typename": "String!"
                        },
                        {
                            "name": "restricted",
                            "typename": "Boolean!"
                        },
                        {
                            "name": "shelf",
                            "typename": "Integer!"
                        },
                        {
                            "name": "bookmark_set",
                            "typename": "Paginated[Bookmark]!"
                        }
                    ]
                },
                {
                    "typename": "BookmarkFilters",
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
                            "name": "page",
                            "typename": "Integer"
                        },
                        {
                            "name": "page__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "page__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "page__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "page__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "page__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "page__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "page__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "book_id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "book_id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "book_id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "Bookmark",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "page",
                            "typename": "Integer!"
                        },
                        {
                            "name": "book",
                            "typename": "Book!"
                        }
                    ]
                }
            ],
            "__objects": [
                {
                    "name": "Book",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "BookList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "BookFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[Book]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "author",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "title",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "ISBN",
                                    "typename": "String!",
                                    "default": None
                                },
                                {
                                    "name": "restricted",
                                    "typename": "Boolean!",
                                    "default": None
                                },
                                {
                                    "name": "shelf",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "Book!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookGetById",
                            "parameters": [
                                {
                                    "name": "id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Book!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookGetById2",
                            "parameters": [
                                {
                                    "name": "id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "data": [
                                {
                                    "name": "Title",
                                    "typename": "String!",
                                    "default": None
                                }
                            ],
                            "mutation": False,
                            "return_type": "Book!",
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
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "BookmarkFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[Bookmark]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "BookmarkCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "page",
                                    "typename": "Integer!",
                                    "default": None
                                },
                                {
                                    "name": "book_id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "Bookmark!",
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
                    "message": "Validation failed in LogicalConnector \"And\" on field \"id\"",
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
                    "message": "Validation failed in LogicalConnector \"And\" on field \"id\"",
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
