from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.actions import Action
from object.datatypes import ObjectType
from testcases.models import TestModelFKSource, TestModelFKTarget
from tests.graphql_test_utils import get_graphql_url, remove_ws


class FKSource(DjangoObject):
    model = TestModelFKSource


class FKTarget(DjangoObject):
    model = TestModelFKTarget


actions = {
    "a": Action(return_value=ObjectType(FKSource), exec_fn=1),
    "b": Action(return_value=ObjectType(FKTarget), exec_fn=1),
}

schema = generate(GraphQLAdapter, [FKSource, FKTarget], actions)


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
