from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import StringField, ObjectField
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws
from utils import AttrDict


def non_null_only(*args, **kwargs):
    return AttrDict(string_non_null="string")


def non_null_and_null(*args, **kwargs):
    return AttrDict(string_non_null="string", string_null="string")


def all(*args, **kwargs):
    return AttrDict(string_non_null="string", string_null="string", string_default="string")


class TestObject(Object):
    fields = {
        "string_non_null": StringField(),
        "string_null": StringField(nullable=True),
        "string_default": StringField(default="default")
    }

    actions = {
        "non_null_only": Action(return_value=ObjectField("self"), exec_fn=non_null_only),
        "non_null_and_null": Action(return_value=ObjectField("TestObject"), exec_fn=non_null_and_null),
        "all": Action(return_value=ObjectField("tests.graphql.objects.object_primitive_fields_class_ref_by_string.TestObject"), exec_fn=all)
    }


schema = generate(GraphQLAdapter, [TestObject])


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
                  nonNullOnly: TestObject!
                  nonNullAndNull: TestObject!
                  all: TestObject!
                }
                
                type TestObject {
                  stringNonNull: String!
                  stringNull: String
                  stringDefault: String!
                }
                """
            )
        )

    def test_request_non_null_only(self):
        resp = self.query(
            """
            query{
              nonNullOnly{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
            "data": {
                "nonNullOnly": {
                  "stringNonNull": "string",
                  "stringNull": None,
                  "stringDefault": "default"
                }
              }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_and_null(self):
        resp = self.query(
            """
            query{
              nonNullAndNull{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
          "data": {
            "nonNullAndNull": {
              "stringNonNull": "string",
              "stringNull": "string",
              "stringDefault": "default"
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_all(self):
        resp = self.query(
            """
            query{
              all{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
          "data": {
            "all": {
              "stringNonNull": "string",
              "stringNull": "string",
              "stringDefault": "string"
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
