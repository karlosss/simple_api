from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type ActionInfo {
          name: String!
          parameters: [FieldInfo!]!
          data: [FieldInfo!]!
          return_type: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
          mutation: Boolean!
          __str__: String!
        }
        
        type Car {
          model: String!
          color: String!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Owner {
          id: Int!
          car: Car!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        type Query {
          OwnerGetById(id: Int!): Owner!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
    """

    REF_META_SCHEMA = {
        "data": {
            "__types": [
                {
                    "typename": "Car",
                    "fields": [
                        {
                            "name": "model",
                            "typename": "String!"
                        },
                        {
                            "name": "color",
                            "typename": "String!"
                        }
                    ]
                },
                {
                    "typename": "Owner",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer!"
                        },
                        {
                            "name": "car",
                            "typename": "Car!"
                        }
                    ]
                }
            ],
            "__objects": [
                {
                    "name": "Owner",
                    "pk_field": None,
                    "actions": [
                        {
                            "name": "OwnerGetById",
                            "parameters": [
                                {
                                    "name": "id",
                                    "typename": "Integer!",
                                    "default": None
                                }
                            ],
                            "data": [],
                            "mutation": False,
                            "return_type": "Owner!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        }
                    ]
                }
            ],
            "__actions": []
        }
    }

    def test_request(self):
        resp = self.query(
            """
            query{
              OwnerGetById(id: 42){
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
                "OwnerGetById": {
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
