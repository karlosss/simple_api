from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.actions import DetailAction
from django_object.django_object import DjangoObject
from object.actions import Action
from object.datatypes import ObjectType, IntegerType
from object.object import Object
from testcases.models import TestModelM2MSource, TestModelM2MTarget
from tests.graphql_test_utils import get_graphql_url, remove_ws


class M2MSource(DjangoObject):
    model = TestModelM2MSource


class M2MTarget(DjangoObject):
    model = TestModelM2MTarget


actions = {
    "a": Action(return_value=ObjectType(M2MSource), exec_fn=1),
    "b": Action(return_value=ObjectType(M2MTarget), exec_fn=1),
}

schema = generate(GraphQLAdapter, [M2MSource, M2MTarget])


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
