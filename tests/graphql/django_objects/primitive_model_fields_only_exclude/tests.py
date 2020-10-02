import datetime

from .objects import schema
from .models import TestModelPrimitiveFields
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        TestModelPrimitiveFields.objects.create(
            int_field=0,
            float_field=1.5,
            string_char_field="CharField holding a short text",
            string_text_field="TextField holding a loooooooooooooooooong text",
            bool_field=True,
            date_field=datetime.date(year=2020, month=1, day=1),
            time_field=datetime.time(hour=12, minute=34, second=56),
            date_time_field=datetime.datetime(year=2020, month=1, day=1, hour=12, minute=34, second=56)
        )

    def test_schema(self):
        print(self.GRAPHQL_SCHEMA)
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                  mutation: Mutation
                }
                
                scalar Date
                
                scalar DateTime
                
                type Mutation {
                  TestModelObjectAllFieldsCreate(data: TestModelObjectAllFieldsCreateInput!): TestModelObjectAllFields!
                  TestModelObjectAllFieldsUpdate(data: TestModelObjectAllFieldsUpdateInput!, id: Int!): TestModelObjectAllFields!
                  TestModelObjectAllFieldsDelete(id: Int!): Boolean!
                  TestModelObjectOnlyFieldsCreate(data: TestModelObjectOnlyFieldsCreateInput!): TestModelObjectOnlyFields!
                  TestModelObjectOnlyFieldsUpdate(data: TestModelObjectOnlyFieldsUpdateInput!, id: Int!): TestModelObjectOnlyFields!
                  TestModelObjectOnlyFieldsDelete(id: Int!): Boolean!
                  TestModelObjectExcludeFieldsCreate(data: TestModelObjectExcludeFieldsCreateInput!): TestModelObjectExcludeFields!
                  TestModelObjectExcludeFieldsUpdate(data: TestModelObjectExcludeFieldsUpdateInput!, id: Int!): TestModelObjectExcludeFields!
                  TestModelObjectExcludeFieldsDelete(id: Int!): Boolean!
                }
                
                type Query {
                  TestModelObjectExcludeFieldsDetail(id: Int!): TestModelObjectExcludeFields!
                  TestModelObjectExcludeFieldsList(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): TestModelObjectExcludeFieldsList!
                  TestModelObjectOnlyFieldsDetail(id: Int!): TestModelObjectOnlyFields!
                  TestModelObjectOnlyFieldsList(int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): TestModelObjectOnlyFieldsList!
                  TestModelObjectAllFieldsDetail(id: Int!): TestModelObjectAllFields!
                  TestModelObjectAllFieldsList(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, string_char_field__contains: String, string_char_field__endswith: String, string_char_field__icontains: String, string_char_field__in: [String!], string_char_field__iregex: String, string_char_field__isnull: Boolean, string_char_field__regex: String, string_char_field__startswith: String, string_text_field__contains: String, string_text_field__endswith: String, string_text_field__icontains: String, string_text_field__in: [String!], string_text_field__iregex: String, string_text_field__isnull: Boolean, string_text_field__regex: String, string_text_field__startswith: String, ordering: [String!]): TestModelObjectAllFieldsList!
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
                
                type TestModelObjectAllFieldsList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [TestModelObjectAllFields!]!
                }
                
                input TestModelObjectAllFieldsUpdateInput {
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
                }
                
                input TestModelObjectExcludeFieldsCreateInput {
                  int_field: Int!
                  float_field: Float!
                  string_char_field: String!
                  string_text_field: String!
                  bool_field: Boolean!
                  date_field: Date!
                  time_field: Time!
                  date_time_field: DateTime!
                }
                
                type TestModelObjectExcludeFieldsList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [TestModelObjectExcludeFields!]!
                }
                
                input TestModelObjectExcludeFieldsUpdateInput {
                  int_field: Int!
                  float_field: Float!
                  string_char_field: String!
                  string_text_field: String!
                  bool_field: Boolean!
                  date_field: Date!
                  time_field: Time!
                  date_time_field: DateTime!
                }
                
                type TestModelObjectOnlyFields {
                  int_field: Int!
                  float_field: Float!
                }
                
                input TestModelObjectOnlyFieldsCreateInput {
                  int_field: Int!
                  float_field: Float!
                  string_char_field: String!
                  string_text_field: String!
                  bool_field: Boolean!
                  date_field: Date!
                  time_field: Time!
                  date_time_field: DateTime!
                }
                
                type TestModelObjectOnlyFieldsList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [TestModelObjectOnlyFields!]!
                }
                
                input TestModelObjectOnlyFieldsUpdateInput {
                  int_field: Int!
                  float_field: Float!
                  string_char_field: String!
                  string_text_field: String!
                  bool_field: Boolean!
                  date_field: Date!
                  time_field: Time!
                  date_time_field: DateTime!
                }
                
                scalar Time

                """
            )
        )

    def test_all(self):
        resp = self.query(
            """
            query{
              TestModelObjectAllFieldsDetail(id: 1){
                id
                int_field
                float_field
                string_char_field
                string_text_field
                bool_field
                date_field
                time_field
                date_time_field
              }
            }
            """
        )

        exp = {
            "data": {
                "TestModelObjectAllFieldsDetail": {
                    "id": 1,
                    "int_field": 0,
                    "float_field": 1.5,
                    "string_char_field": "CharField holding a short text",
                    "string_text_field": "TextField holding a loooooooooooooooooong text",
                    "bool_field": True,
                    "date_field": "2020-01-01",
                    "time_field": "12:34:56",
                    "date_time_field": "2020-01-01T12:34:56+00:00"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
