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
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                }
                
                scalar Date
                
                scalar DateTime
                
                type Query {
                  TestModelObjectExcludeFieldsDetail(id: Int!): TestModelObjectExcludeFields!
                  TestModelObjectOnlyFieldsDetail(id: Int!): TestModelObjectOnlyFields!
                  TestModelObjectAllFieldsDetail(id: Int!): TestModelObjectAllFields!
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
                
                type TestModelObjectExcludeFields {
                  id: Int!
                  int_field: Int!
                  float_field: Float!
                  bool_field: Boolean!
                  date_field: Date!
                  time_field: Time!
                  date_time_field: DateTime!
                }
                
                type TestModelObjectOnlyFields {
                  int_field: Int!
                  float_field: Float!
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
