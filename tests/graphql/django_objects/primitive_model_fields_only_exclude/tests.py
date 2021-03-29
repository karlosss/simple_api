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
      
      scalar Date
      
      scalar DateTime
      
      scalar Duration
      
      type FieldInfo {
        name: String!
        typename: String!
        default: String
        __str__: String!
      }
      
      type Mutation {
        TestModelObjectAllFieldsCreate(data: TestModelObjectAllFieldsCreateInput!): TestModelObjectAllFields!
        TestModelObjectOnlyFieldsCreate(data: TestModelObjectOnlyFieldsCreateInput!): TestModelObjectOnlyFields!
        TestModelObjectExcludeFieldsCreate(data: TestModelObjectExcludeFieldsCreateInput!): TestModelObjectExcludeFields!
      }
      
      type ObjectInfo {
        name: String!
        pk_field: String
        actions: [ActionInfo!]!
        __str__: String!
      }
      
      type Query {
        __types: [TypeInfo!]!
        __objects: [ObjectInfo!]!
        __actions: [ActionInfo!]!
      }
      
      type TestModelObjectAllFields {
        id: Int!
        int_field: Int!
        float_field: Float!
        string_char_field: String!
        string_text_field: String!
        bool_field: Boolean!
        date_field: Date!
        time_field: Time!
        date_time_field: DateTime!
        __str__: String!
        __actions: [ActionInfo!]!
      }
      
      input TestModelObjectAllFieldsCreateInput {
        int_field: Int!
        float_field: Float!
        string_char_field: String!
        string_text_field: String!
        bool_field: Boolean!
        date_field: Date!
        time_field: Time!
        date_time_field: DateTime!
      }
      
      type TestModelObjectExcludeFields {
        id: Int!
        int_field: Int!
        float_field: Float!
        bool_field: Boolean!
        date_field: Date!
        time_field: Time!
        date_time_field: DateTime!
        __str__: String!
        __actions: [ActionInfo!]!
      }
      
      input TestModelObjectExcludeFieldsCreateInput {
        int_field: Int!
        float_field: Float!
        bool_field: Boolean!
        date_field: Date!
        time_field: Time!
        date_time_field: DateTime!
      }
      
      type TestModelObjectOnlyFields {
        id: Int!
        int_field: Int!
        float_field: Float!
        __str__: String!
        __actions: [ActionInfo!]!
      }
      
      input TestModelObjectOnlyFieldsCreateInput {
        int_field: Int!
        float_field: Float!
      }
      
      scalar Time
      
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
        "typename": "TestModelObjectAllFieldsFilters",
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
            "name": "int_field",
            "typename": "Integer"
          },
          {
            "name": "int_field__exact",
            "typename": "Integer"
          },
          {
            "name": "int_field__gt",
            "typename": "Integer"
          },
          {
            "name": "int_field__gte",
            "typename": "Integer"
          },
          {
            "name": "int_field__in",
            "typename": "[Integer!]"
          },
          {
            "name": "int_field__isnull",
            "typename": "Boolean"
          },
          {
            "name": "int_field__lt",
            "typename": "Integer"
          },
          {
            "name": "int_field__lte",
            "typename": "Integer"
          },
          {
            "name": "string_char_field",
            "typename": "String"
          },
          {
            "name": "string_char_field__contains",
            "typename": "String"
          },
          {
            "name": "string_char_field__endswith",
            "typename": "String"
          },
          {
            "name": "string_char_field__exact",
            "typename": "String"
          },
          {
            "name": "string_char_field__icontains",
            "typename": "String"
          },
          {
            "name": "string_char_field__in",
            "typename": "[String!]"
          },
          {
            "name": "string_char_field__iregex",
            "typename": "String"
          },
          {
            "name": "string_char_field__isnull",
            "typename": "Boolean"
          },
          {
            "name": "string_char_field__regex",
            "typename": "String"
          },
          {
            "name": "string_char_field__startswith",
            "typename": "String"
          },
          {
            "name": "string_text_field",
            "typename": "String"
          },
          {
            "name": "string_text_field__contains",
            "typename": "String"
          },
          {
            "name": "string_text_field__endswith",
            "typename": "String"
          },
          {
            "name": "string_text_field__exact",
            "typename": "String"
          },
          {
            "name": "string_text_field__icontains",
            "typename": "String"
          },
          {
            "name": "string_text_field__in",
            "typename": "[String!]"
          },
          {
            "name": "string_text_field__iregex",
            "typename": "String"
          },
          {
            "name": "string_text_field__isnull",
            "typename": "Boolean"
          },
          {
            "name": "string_text_field__regex",
            "typename": "String"
          },
          {
            "name": "string_text_field__startswith",
            "typename": "String"
          },
          {
            "name": "ordering",
            "typename": "[String!]"
          }
        ]
      },
      {
        "typename": "TestModelObjectAllFields",
        "fields": [
          {
            "name": "id",
            "typename": "Integer!"
          },
          {
            "name": "int_field",
            "typename": "Integer!"
          },
          {
            "name": "float_field",
            "typename": "Float!"
          },
          {
            "name": "string_char_field",
            "typename": "String!"
          },
          {
            "name": "string_text_field",
            "typename": "String!"
          },
          {
            "name": "bool_field",
            "typename": "Boolean!"
          },
          {
            "name": "date_field",
            "typename": "Date!"
          },
          {
            "name": "time_field",
            "typename": "Time!"
          },
          {
            "name": "date_time_field",
            "typename": "DateTime!"
          }
        ]
      },
      {
        "typename": "TestModelObjectOnlyFieldsFilters",
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
            "name": "int_field",
            "typename": "Integer"
          },
          {
            "name": "int_field__exact",
            "typename": "Integer"
          },
          {
            "name": "int_field__gt",
            "typename": "Integer"
          },
          {
            "name": "int_field__gte",
            "typename": "Integer"
          },
          {
            "name": "int_field__in",
            "typename": "[Integer!]"
          },
          {
            "name": "int_field__isnull",
            "typename": "Boolean"
          },
          {
            "name": "int_field__lt",
            "typename": "Integer"
          },
          {
            "name": "int_field__lte",
            "typename": "Integer"
          },
          {
            "name": "ordering",
            "typename": "[String!]"
          }
        ]
      },
      {
        "typename": "TestModelObjectOnlyFields",
        "fields": [
          {
            "name": "id",
            "typename": "Integer!"
          },
          {
            "name": "int_field",
            "typename": "Integer!"
          },
          {
            "name": "float_field",
            "typename": "Float!"
          }
        ]
      },
      {
        "typename": "TestModelObjectExcludeFieldsFilters",
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
            "name": "int_field",
            "typename": "Integer"
          },
          {
            "name": "int_field__exact",
            "typename": "Integer"
          },
          {
            "name": "int_field__gt",
            "typename": "Integer"
          },
          {
            "name": "int_field__gte",
            "typename": "Integer"
          },
          {
            "name": "int_field__in",
            "typename": "[Integer!]"
          },
          {
            "name": "int_field__isnull",
            "typename": "Boolean"
          },
          {
            "name": "int_field__lt",
            "typename": "Integer"
          },
          {
            "name": "int_field__lte",
            "typename": "Integer"
          },
          {
            "name": "ordering",
            "typename": "[String!]"
          }
        ]
      },
      {
        "typename": "TestModelObjectExcludeFields",
        "fields": [
          {
            "name": "id",
            "typename": "Integer!"
          },
          {
            "name": "int_field",
            "typename": "Integer!"
          },
          {
            "name": "float_field",
            "typename": "Float!"
          },
          {
            "name": "bool_field",
            "typename": "Boolean!"
          },
          {
            "name": "date_field",
            "typename": "Date!"
          },
          {
            "name": "time_field",
            "typename": "Time!"
          },
          {
            "name": "date_time_field",
            "typename": "DateTime!"
          }
        ]
      }
    ],
    "__objects": [
      {
        "name": "TestModelObjectAllFields",
        "pk_field": "id",
        "actions": [
          {
            "name": "TestModelObjectAllFieldsCreate",
            "parameters": [],
            "data": [
              {
                "name": "int_field",
                "typename": "Integer!",
                "default": None
              },
              {
                "name": "float_field",
                "typename": "Float!",
                "default": None
              },
              {
                "name": "string_char_field",
                "typename": "String!",
                "default": None
              },
              {
                "name": "string_text_field",
                "typename": "String!",
                "default": None
              },
              {
                "name": "bool_field",
                "typename": "Boolean!",
                "default": None
              },
              {
                "name": "date_field",
                "typename": "Date!",
                "default": None
              },
              {
                "name": "time_field",
                "typename": "Time!",
                "default": None
              },
              {
                "name": "date_time_field",
                "typename": "DateTime!",
                "default": None
              }
            ],
            "mutation": True,
            "return_type": "TestModelObjectAllFields!",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          }
        ]
      },
      {
        "name": "TestModelObjectOnlyFields",
        "pk_field": "id",
        "actions": [
          {
            "name": "TestModelObjectOnlyFieldsCreate",
            "parameters": [],
            "data": [
              {
                "name": "int_field",
                "typename": "Integer!",
                "default": None
              },
              {
                "name": "float_field",
                "typename": "Float!",
                "default": None
              }
            ],
            "mutation": True,
            "return_type": "TestModelObjectOnlyFields!",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          }
        ]
      },
      {
        "name": "TestModelObjectExcludeFields",
        "pk_field": "id",
        "actions": [
          {
            "name": "TestModelObjectExcludeFieldsCreate",
            "parameters": [],
            "data": [
              {
                "name": "int_field",
                "typename": "Integer!",
                "default": None
              },
              {
                "name": "float_field",
                "typename": "Float!",
                "default": None
              },
              {
                "name": "bool_field",
                "typename": "Boolean!",
                "default": None
              },
              {
                "name": "date_field",
                "typename": "Date!",
                "default": None
              },
              {
                "name": "time_field",
                "typename": "Time!",
                "default": None
              },
              {
                "name": "date_time_field",
                "typename": "DateTime!",
                "default": None
              }
            ],
            "mutation": True,
            "return_type": "TestModelObjectExcludeFields!",
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