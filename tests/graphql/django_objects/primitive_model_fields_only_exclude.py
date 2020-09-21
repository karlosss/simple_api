from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.actions import Action
from object.datatypes import ObjectType
from testcases.models import TestModelPrimitiveFields
from tests.graphql_test_utils import get_graphql_url, remove_ws


class TestModelObjectAllFields(DjangoObject):
    model = TestModelPrimitiveFields


class TestModelObjectOnlyFields(DjangoObject):
    model = TestModelPrimitiveFields
    only_fields = ("int_field", "float_field")


class TestModelObjectExcludeFields(DjangoObject):
    model = TestModelPrimitiveFields
    exclude_fields = ("string_char_field", "string_text_field")


actions = {
    "a": Action(return_value=ObjectType(TestModelObjectAllFields)),
    "b": Action(return_value=ObjectType(TestModelObjectOnlyFields)),
    "c": Action(return_value=ObjectType(TestModelObjectExcludeFields)),
}


schema = generate(GraphQLAdapter,
                  [TestModelObjectAllFields, TestModelObjectOnlyFields, TestModelObjectExcludeFields],
                  actions)


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = get_graphql_url(__file__)

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
                  a: TestModelObjectAllFields!
                  b: TestModelObjectOnlyFields!
                  c: TestModelObjectExcludeFields!
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
