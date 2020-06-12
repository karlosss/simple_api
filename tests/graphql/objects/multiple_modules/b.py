from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import StringType, ObjectType, IntegerType
from object.function import Function
from object.object import Object
from tests.graphql.objects.multiple_modules.a import A
from tests.graphql_test_utils import get_graphql_url, remove_ws
from utils import AttrDict


def get(request, params):
    return {
        "a": {
            "s1": "A"
        },
        "b": {
            "s1": "B"
        }
    }


class B(Object):
    fields = {
        "s1": StringType(),
        "s2": ObjectType("self", nullable=True)
    }


class C(Object):
    fields = {
        "a": ObjectType(A),
        "b": ObjectType("B")
    }


actions = {
    "get": Action(return_value=ObjectType(C), exec_fn=Function(get))
}


schema = generate(GraphQLAdapter, [A, B, C], actions)


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
                
                type A {
                  s1: String!
                  s2: A
                }
                
                type B {
                  s1: String!
                  s2: B
                }
                
                type C {
                  a: A!
                  b: B!
                }
                
                type Query {
                  get: C!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              get{
                a{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
                b{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "a": {
                "s1": "A",
                "s2": None
              },
              "b": {
                "s1": "B",
                "s2": None
              }
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
