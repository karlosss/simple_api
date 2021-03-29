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
      lease_set(filters: LeaseFiltersInput): LeaseList!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input BookCreateInput {
      author: String!
      title: String!
      ISBN: String!
      restricted: Boolean!
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
      can_return: Boolean!
      subscription_set(filters: SubscriptionFiltersInput): SubscriptionList!
      lease_set(filters: LeaseFiltersInput): LeaseList!
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
      can_return: Boolean = false
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
    
    input CustomUserUpdateInput {
      email: String
      username: String
      first_name: String
      last_name: String
      password: String
      bio: String
      is_admin: Boolean = false
      can_return: Boolean = false
    }
    
    scalar Date
    
    scalar Duration
    
    type FieldInfo {
      name: String!
      typename: String!
      default: String
      __str__: String!
    }
    
    type Lease {
      id: Int!
      start: Date!
      end: Date!
      book: Book!
      borrower: CustomUser!
      __str__: String!
      __actions: [ActionInfo!]!
    }
    
    input LeaseCreateInput {
      start: Date!
      end: Date!
      book_id: Int!
      borrower_id: Int!
    }
    
    input LeaseFiltersInput {
      id: Int
      id__exact: Int
      id__gt: Int
      id__gte: Int
      id__in: [Int!]
      id__isnull: Boolean
      id__lt: Int
      id__lte: Int
      book_id: Int
      book_id__exact: Int
      book_id__gt: Int
      book_id__gte: Int
      book_id__in: [Int!]
      book_id__isnull: Boolean
      book_id__lt: Int
      book_id__lte: Int
      borrower_id: Int
      borrower_id__exact: Int
      borrower_id__gt: Int
      borrower_id__gte: Int
      borrower_id__in: [Int!]
      borrower_id__isnull: Boolean
      borrower_id__lt: Int
      borrower_id__lte: Int
      ordering: [String!]
    }
    
    type LeaseList {
      count: Int!
      data(limit: Int = 20, offset: Int = 0): [Lease!]!
      __str__: String!
    }
    
    input LeaseUpdateInput {
      start: Date
      end: Date
      book_id: Int
      borrower_id: Int
    }
    
    type Mutation {
      CustomUserCreate(data: CustomUserCreateInput!): CustomUser!
      CustomUserUpdate(data: CustomUserUpdateInput!, id: Int!): CustomUser!
      CustomUserDelete(id: Int!): Boolean!
      BookCreate(data: BookCreateInput!): Book!
      BookUpdate(data: BookUpdateInput!, id: Int!): Book!
      BookDelete(id: Int!): Boolean!
      SubscriptionCreate(data: SubscriptionCreateInput!): Subscription!
      SubscriptionUpdate(data: SubscriptionUpdateInput!, id: Int!): Subscription!
      SubscriptionDelete(id: Int!): Boolean!
      LeaseCreate(data: LeaseCreateInput!): Lease!
      LeaseUpdate(data: LeaseUpdateInput!, id: Int!): Lease!
      LeaseDelete(id: Int!): Boolean!
    }
    
    type ObjectInfo {
      name: String!
      pk_field: String
      actions: [ActionInfo!]!
      __str__: String!
    }
    
    type Query {
      LeaseDetail(id: Int!): Lease!
      LeaseList(filters: LeaseFiltersInput): LeaseList!
      SubscriptionDetail(id: Int!): Subscription!
      SubscriptionList(filters: SubscriptionFiltersInput): SubscriptionList!
      BookDetail(id: Int!): Book!
      BookList(filters: BookFiltersInput): BookList!
      CustomUserDetail(id: Int!): CustomUser!
      CustomUserList(filters: CustomUserFiltersInput): CustomUserList!
      __types: [TypeInfo!]!
      __objects: [ObjectInfo!]!
      __actions: [ActionInfo!]!
    }
    
    type Subscription {
      id: Int!
      start: Date!
      end: Date!
      user: CustomUser!
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
      __str__: String!
    }
    
    input SubscriptionUpdateInput {
      start: Date
      end: Date
      user_id: Int
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
                            "name": "can_return",
                            "typename": "Boolean!"
                        },
                        {
                            "name": "subscription_set",
                            "typename": "Paginated[Subscription]!"
                        },
                        {
                            "name": "lease_set",
                            "typename": "Paginated[Lease]!"
                        }
                    ]
                },
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
                            "name": "lease_set",
                            "typename": "Paginated[Lease]!"
                        }
                    ]
                },
                {
                    "typename": "SubscriptionFilters",
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
                            "name": "user_id",
                            "typename": "Integer"
                        },
                        {
                            "name": "user_id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "user_id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "user_id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "user_id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "user_id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "user_id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "user_id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "Subscription",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "start",
                            "typename": "Date!"
                        },
                        {
                            "name": "end",
                            "typename": "Date!"
                        },
                        {
                            "name": "user",
                            "typename": "CustomUser!"
                        }
                    ]
                },
                {
                    "typename": "LeaseFilters",
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
                            "name": "borrower_id",
                            "typename": "Integer"
                        },
                        {
                            "name": "borrower_id__exact",
                            "typename": "Integer"
                        },
                        {
                            "name": "borrower_id__gt",
                            "typename": "Integer"
                        },
                        {
                            "name": "borrower_id__gte",
                            "typename": "Integer"
                        },
                        {
                            "name": "borrower_id__in",
                            "typename": "[Integer!]"
                        },
                        {
                            "name": "borrower_id__isnull",
                            "typename": "Boolean"
                        },
                        {
                            "name": "borrower_id__lt",
                            "typename": "Integer"
                        },
                        {
                            "name": "borrower_id__lte",
                            "typename": "Integer"
                        },
                        {
                            "name": "ordering",
                            "typename": "[String!]"
                        }
                    ]
                },
                {
                    "typename": "Lease",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "start",
                            "typename": "Date!"
                        },
                        {
                            "name": "end",
                            "typename": "Date!"
                        },
                        {
                            "name": "book",
                            "typename": "Book!"
                        },
                        {
                            "name": "borrower",
                            "typename": "CustomUser!"
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
                                },
                                {
                                    "name": "can_return",
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
                    "name": "Subscription",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "SubscriptionList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "SubscriptionFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[Subscription]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "SubscriptionCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "start",
                                    "typename": "Date!",
                                    "default": None
                                },
                                {
                                    "name": "end",
                                    "typename": "Date!",
                                    "default": None
                                },
                                {
                                    "name": "user_id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "Subscription!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                },
                {
                    "name": "Lease",
                    "pk_field": "id",
                    "actions": [
                        {
                            "name": "LeaseList",
                            "parameters": [
                                {
                                    "name": "filters",
                                    "typename": "LeaseFilters",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Paginated[Lease]!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "LeaseCreate",
                            "parameters": [],
                            "data": [
                                {
                                    "name": "start",
                                    "typename": "Date!",
                                    "default": None
                                },
                                {
                                    "name": "end",
                                    "typename": "Date!",
                                    "default": None
                                },
                                {
                                    "name": "book_id",
                                    "typename": "Integer!",
                                    "default": None
                                },
                                {
                                    "name": "borrower_id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "mutation": True,
                            "return_type": "Lease!",
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
                  bio: "ሰማይ አይታረስ ንጉሥ አይከሰስ።⡌⠁⠧⠑ ⠼⠁⠒  ⡍⠜⠇⠑⠹⠰⠎ ⡣⠕⠌"
                }){
                  id
                  email
                  username
                  first_name
                  last_name
                  password
                  bio
                  is_admin
                  can_return
                }
              }
              """)
        ret = {
            "data": {
                "CustomUserCreate": {
                    "id": 1,
                    "email": "user1@example.com",
                    "username": "adam",
                    "first_name": "Adam",
                    "last_name": "First",
                    "password": "secret",
                    "bio": "ሰማይ አይታረስ ንጉሥ አይከሰስ።⡌⠁⠧⠑ ⠼⠁⠒  ⡍⠜⠇⠑⠹⠰⠎ ⡣⠕⠌",
                    "is_admin": False,
                    "can_return": False
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
        query detail_of_user{
          CustomUserDetail(id: 1){
            id
            email
            username
            last_name
            first_name
            password
            bio
            can_return
          }
        }""")
        ret = {
            "data": {
                "CustomUserDetail": {
                    "id": 1,
                    "email": "user1@example.com",
                    "username": "adam",
                    "last_name": "First",
                    "first_name": "Adam",
                    "password": "secret",
                    "bio": "ሰማይ አይታረስ ንጉሥ አይከሰስ።⡌⠁⠧⠑ ⠼⠁⠒  ⡍⠜⠇⠑⠹⠰⠎ ⡣⠕⠌",
                    "can_return": False
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query detail_of_user{
                  CustomUserDetail(id: 42){
                    id
                    email
                    username
                    last_name
                    first_name
                    password
                    bio
                    can_return
                  }
                }""")
        ret = {
            "errors": [
                {
                    "message": "CustomUser matching query does not exist.",
                    "locations": [
                        {
                            "line": 2,
                            "column": 19
                        }
                    ],
                    "path": [
                        "CustomUserDetail"
                    ]
                }
            ],
            "data": None
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""query detail_of_user{
                          CustomUserDetail(id: 42){
                            id
                            email
                            usernae
                            last_name
                            first_name
                            password
                            bio
                            can_return
                          }
                        }""")
        ret = {
            "errors": [
                {
                    "message": "Cannot query field \"usernae\" on type \"CustomUser\". Did you mean \"username\"?",
                    "locations": [
                        {
                            "line": 5,
                            "column": 29
                        }
                    ]
                }
            ]
        }
        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
        mutation change_last_name {
          CustomUserUpdate(id: 1, data: {last_name: "Second"}) {
            id
            first_name
            last_name
          }
        }""")
        ret = {
            "data": {
                "CustomUserUpdate": {
                    "id": 1,
                    "first_name": "Adam",
                    "last_name": "Second"
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)

        resp = self.query("""
        query list_users_with_password {
          CustomUserList {
            count
            data {
              id
              first_name
              last_name
            }
          }
        }""")
        ret = {
            "data": {
                "CustomUserList": {
                    "count": 1,
                    "data": [
                        {
                            "id": 1,
                            "first_name": "Adam",
                            "last_name": "Second"
                        }
                    ]
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
        resp = self.query("""
        mutation create_user {
          CustomUserCreate(
          data:{
            email: "user2@example.com",
            username: "Bob",
            first_name: "Bob",
            last_name: "Third",
            password: "extrasecret",
            bio: ""}) 
          {
            id
            email
            username
            first_name
            last_name
            password
            bio
            is_admin
            can_return
          }
        }""")
        ret = {
            "data": {
                "CustomUserCreate": {
                    "id": 2,
                    "email": "user2@example.com",
                    "username": "Bob",
                    "first_name": "Bob",
                    "last_name": "Third",
                    "password": "extrasecret",
                    "bio": "",
                    "is_admin": False,
                    "can_return": False
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, ret)
