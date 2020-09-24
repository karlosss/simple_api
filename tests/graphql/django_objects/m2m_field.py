from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.registry import object_storage
from testcases.models import TestModelM2MSource, TestModelM2MTarget
from tests.graphql_test_utils import get_graphql_url, remove_ws, CustomGraphQLTestCase


class M2MSource(DjangoObject):
    model = TestModelM2MSource


class M2MTarget(DjangoObject):
    model = TestModelM2MTarget

print(object_storage.storage.values())


schema = generate(GraphQLAdapter, [M2MSource, M2MTarget])


class Test(CustomGraphQLTestCase):
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
                
                type M2MSource {
                  id: Int!
                  m2mField: [M2MTarget!]!
                }
                
                type M2MTarget {
                  id: Int!
                  intField: Int!
                  m2mSources: [M2MSource!]!
                }
                
                type Query {
                  m2MTargetDetail(id: Int!): M2MTarget!
                  m2MSourceDetail(id: Int!): M2MSource!
                }
                """
            )
        )
