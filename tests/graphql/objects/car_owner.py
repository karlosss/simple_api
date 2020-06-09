from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import StringField, ObjectField, IntegerField
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws
from utils import AttrDict


def get_by_id(*args, **kwargs):
    return AttrDict(id=kwargs["id"], car=AttrDict(model="BMW", color="blue"))


class Car(Object):
    fields = {
        "model": StringField(),
        "color": StringField()
    }


class Owner(Object):
    fields = {
        "id": IntegerField(),
        "car": ObjectField(Car)
    }

    actions = {
        "get_by_id": Action(parameters={"id": IntegerField()}, return_value=ObjectField("self"), exec_fn=get_by_id)
    }


schema = generate(GraphQLAdapter, [Car, Owner])


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
                
                type Car {
                  model: String!
                  color: String!
                }
                
                type Owner {
                  id: Int!
                  car: Car!
                }
                
                type Query {
                  getById(id: Int!): Owner!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              getById(id: 42){
                id
                car{
                  model
                  color
                }
              }
            }
            """
        )

        exp = {
          "data": {
            "getById": {
              "id": 42,
              "car": {
                "model": "BMW",
                "color": "blue"
              }
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
