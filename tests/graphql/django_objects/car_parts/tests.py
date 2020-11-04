from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_schema(self):
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                  mutation: Mutation
                }

                type Mutation {
                  TestObjectCreate(data: TestObjectCreateInput!): TestObject!
                  TestObjectUpdate(data: TestObjectUpdateInput!, id: Int!): TestObject!
                  TestObjectDelete(id: Int!): Boolean!
                }

                type Query {
                  TestObjectDetail(id: Int!): TestObject!
                  TestObjectList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, string_field: String, string_field__contains: String, string_field__endswith: String, string_field__exact: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, ordering: [String!]): TestObjectList!
                }

                type TestObject {
                  id: Int!
                  int_field: Int!
                  string_field: String
                  int_plus_one: Int!
                }

                input TestObjectCreateInput {
                  int_field: Int!
                  string_field: String!
                }

                type TestObjectList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [TestObject!]!
                }

                input TestObjectUpdateInput {
                  int_field: Int
                  string_field: String
                }
                """
            )
        )

    def test_requests(self):
        resp = self.query(
            """
            mutation create{
              create1: TestObjectCreate(data: {int_field: 10, string_field: "asdf"}){
                id
                string_field
                int_field
                int_plus_one
              }
              create2: TestObjectCreate(data: {int_field: 20, string_field: "a"}){
                id
                string_field
                int_field
                int_plus_one
              }
            }
            """
        )
        exp = {
            "data": {
                "create1": {
                    "id": 1,
                    "string_field": "asdf",
                    "int_field": 10,
                    "int_plus_one": 11
                },
                "create2": {
                    "id": 2,
                    "string_field": None,
                    "int_field": 20,
                    "int_plus_one": 21
                }
            }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
