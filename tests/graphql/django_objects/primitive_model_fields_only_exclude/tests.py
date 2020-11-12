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
        
        scalar Date
        
        scalar DateTime
        
        scalar Duration
        
        type Mutation {
          TestModelObjectAllFieldsCreate(data: TestModelObjectAllFieldsCreateInput!): TestModelObjectAllFields!
          TestModelObjectOnlyFieldsCreate(data: TestModelObjectOnlyFieldsCreateInput!): TestModelObjectOnlyFields!
          TestModelObjectExcludeFieldsCreate(data: TestModelObjectExcludeFieldsCreateInput!): TestModelObjectExcludeFields!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
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

    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "TestModelObjectAllFields",
            "pk_field": "id",
            "actions": [
              {
                "name": "TestModelObjectAllFieldsCreate",
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