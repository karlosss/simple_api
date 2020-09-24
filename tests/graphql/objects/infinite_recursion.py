from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import ObjectType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws, CustomGraphQLTestCase


def get(request, params):
    return None


class TestObject(Object):
    fields = {
        "self": ObjectType("self", nullable=True)
    }


actions = {
    "get": Action(return_value=ObjectType(TestObject, nullable=True), exec_fn=Function(get))
}

schema = generate(GraphQLAdapter, [TestObject], actions)


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
                
                type Query {
                  get: TestObject
                }
                
                type TestObject {
                  self: TestObject
                }
                """
            )
        )

    # no requests possible
