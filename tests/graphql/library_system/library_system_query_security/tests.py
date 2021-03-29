from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase

"""
Test expects django settings:
SIMPLE_API = {
    "SECURITY": {
        "LIST_LIMIT": 100,
        "DEPTH_LIMIT": 20,
        "WEIGHT_LIMIT": 20000
    }
}
"""


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
      shelf: Int!
      bookmark_set(filters: BookmarkFiltersInput): BookmarkList!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input BookCreateInput {
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
      __str__: String!
    }
    
    input BookUpdateInput {
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
      Heavy_Action: String!
      Light_Action: String!
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
            "__actions": [
                {
                    "name": "Heavy_Action",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "String!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "Light_Action",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "String!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                }
            ]
        }
    }

    def test_requests(self):
        resp = self.query("""mutation {
          BookCreate(data: {shelf: 6}) {
            shelf
          }
        }""")
        ret = {
            "data": {
                "BookCreate": {
                    "shelf": 6
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_bookmark {
                  BookmarkCreate(data: {book_id: 1, page: 123}) {
                    page
                  }
                }""")
        ret = {
            "data": {
                "BookmarkCreate": {
                    "page": 123,
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""mutation add_bookmark {
                          BookmarkCreate(data: {book_id: 1, page: 666}) {
                            page
                          }
                        }""")
        ret = {
            "data": {
                "BookmarkCreate": {
                    "page": 666,
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        # TEST DEPTH

        resp = self.query("""query depth {
                    BookDetail(id: 1) {
                        shelf
                        bookmark_set {
                            count
                            data(limit: 1) {
                                book {
                                    bookmark_set {
                                        count
                                        data(limit: 1) {
                                            book {
                                                bookmark_set {
                                                    data(limit: 1) {
                                                        book {
                                                            bookmark_set {
                                                                count
                                                                data(limit: 1) {
                                                                    book {
                                                                        bookmark_set {
                                                                            count
                                                                            data(limit: 1) {
                                                                                book {
                                                                                    bookmark_set {
                                                                                        data(limit: 1) {
                                                                                            book {
                                                                                                bookmark_set {
                                                                                                    data(limit: 1) {
                                                                                                        book {
                                                                                                            shelf
                                                                                                        }
                                                                                                    }
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                """)
        ret = {
            "errors": [
                {
                    "message": "Query depth limit exceeded"
                }
            ]
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
            query depthOK {
                BookDetail(id: 1) {
                    shelf
                    bookmark_set {
                        count
                        data(limit: 1) {
                            book {
                                bookmark_set {
                                    count
                                    data(limit: 1) {
                                        book {
                                            bookmark_set {
                                                data(limit: 1) {
                                                    book {
                                                        bookmark_set {
                                                            count
                                                            data(limit: 1) {
                                                                book {
                                                                    bookmark_set {
                                                                        count
                                                                        data(limit: 1) {
                                                                            book {
                                                                                shelf
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """)

        ret = {
            "data": {
                "BookDetail": {
                    "shelf": 6,
                    "bookmark_set": {
                        "count": 2,
                        "data": [
                            {
                                "book": {
                                    "bookmark_set": {
                                        "count": 2,
                                        "data": [
                                            {
                                                "book": {
                                                    "bookmark_set": {
                                                        "data": [
                                                            {
                                                                "book": {
                                                                    "bookmark_set": {
                                                                        "count": 2,
                                                                        "data": [
                                                                            {
                                                                                "book": {
                                                                                    "bookmark_set": {
                                                                                        "count": 2,
                                                                                        "data": [
                                                                                            {
                                                                                                "book": {
                                                                                                    "shelf": 6
                                                                                                }
                                                                                            }
                                                                                        ]
                                                                                    }
                                                                                }
                                                                            }
                                                                        ]
                                                                    }
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        # TEST LIST LIMITING
        resp = self.query("""
            query depthOK {
                BookDetail(id: 1) {
                    shelf
                    bookmark_set {
                        count
                        data{
                            page
                        }
                    }
                }
            }
        """)
        ret = {
            "errors": [
                {
                    "message": "Requests for paginated data require limit"
                }
            ]
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
            query depthOK {
                BookDetail(id: 1) {
                    shelf
                    bookmark_set {
                        count
                        data (limit:2) {
                            page
                        }
                    }
                }
            }
        """)
        ret = {
            "data": {
                "BookDetail": {
                    "shelf": 6,
                    "bookmark_set": {
                        "count": 2,
                        "data": [
                            {
                                "page": 123
                            },
                            {
                                "page": 666
                            }
                        ]
                    }
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        # Score Limit
        resp = self.query("""
        query score {
          first: Heavy_Action
          second: Heavy_Action
        }""")
        ret = {
            "errors": [
                {
                    "message": "Your query exceeds the maximum query weight allowed"
                }
            ]
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
                query scoreOK {
                  first: Heavy_Action
                  second: Light_Action
                }""")
        ret = {
            "data": {
                "first": "Action run",
                "second": "Action run"
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
