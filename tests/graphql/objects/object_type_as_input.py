from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import StringField, ObjectField, IntegerField
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def get(*args, **kwargs):
    if "id" in kwargs:
        return "{}.{}".format(kwargs["id"]["int1"], kwargs["id"]["int2"])
    return "no params passed"


class TestObject(Object):
    fields = {
        "int1": IntegerField(),
        "int2": IntegerField(),
    }


class Actions(Object):
    actions = {
        "get": Action(parameters={"id": ObjectField(TestObject)}, return_value=StringField(), exec_fn=get),
        "get_null": Action(parameters={"id": ObjectField(TestObject, nullable=True)}, return_value=StringField(), exec_fn=get)
    }


schema = generate(GraphQLAdapter, [Actions, TestObject])


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
                
                type Query {
                  get(id: TestObject!): String!
                  getNull(id: TestObject): String!
                }
                
                input TestObject {
                  int1: Int!
                  int2: Int!
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              get(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
          "data": {
            "get": "1.2"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_fail(self):
        resp = self.query(
            """
            query{
              get
            }
            """
        )

        self.assertResponseHasErrors(resp)

    def test_request_null_param(self):
        resp = self.query(
            """
            query{
              getNull(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
          "data": {
            "getNull": "1.2"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_no_param(self):
        resp = self.query(
            """
            query{
              getNull
            }
            """
        )

        exp = {
          "data": {
            "getNull": "no params passed"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)