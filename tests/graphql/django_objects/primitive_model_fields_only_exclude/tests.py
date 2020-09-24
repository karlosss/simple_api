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
                  testModelObjectExcludeFieldsDetail(id: Int!): TestModelObjectExcludeFields!
                  testModelObjectOnlyFieldsDetail(id: Int!): TestModelObjectOnlyFields!
                  testModelObjectAllFieldsDetail(id: Int!): TestModelObjectAllFields!
                }

                type TestModelObjectAllFields {
                  id: Int!
                  intField: Int!
                  floatField: Float!
                  stringCharField: String!
                  stringTextField: String!
                  boolField: Boolean!
                  dateField: Date!
                  timeField: Time!
                  dateTimeField: DateTime!
                }

                type TestModelObjectExcludeFields {
                  id: Int!
                  intField: Int!
                  floatField: Float!
                  boolField: Boolean!
                  dateField: Date!
                  timeField: Time!
                  dateTimeField: DateTime!
                }

                type TestModelObjectOnlyFields {
                  intField: Int!
                  floatField: Float!
                }

                scalar Time

                """
            )
        )

    def test_all(self):
        resp = self.query(
            """
            query{
              testModelObjectAllFieldsDetail(id: 1){
                id
                intField
                floatField
                stringCharField
                stringTextField
                boolField
                dateField
                timeField
                dateTimeField
              }
            }
            """
        )

        exp = {
            "data": {
                "testModelObjectAllFieldsDetail": {
                    "id": 1,
                    "intField": 0,
                    "floatField": 1.5,
                    "stringCharField": "CharField holding a short text",
                    "stringTextField": "TextField holding a loooooooooooooooooong text",
                    "boolField": True,
                    "dateField": "2020-01-01",
                    "timeField": "12:34:56",
                    "dateTimeField": "2020-01-01T12:34:56+00:00"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
