from graphene_django.utils import GraphQLTestCase
from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_schema(self):
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                }
                
                type FKSource {
                  id: Int!
                  stringField: String!
                  fkField: FKTarget!
                  oneToOneField: FKTarget!
                }
                
                type FKTarget {
                  id: Int!
                  intField: Int!
                  fkSources(id_Exact: Int!, id_Gt: Int!, id_Gte: Int!, id_In: [Int!]!, id_Isnull: Boolean!, id_Lt: Int!, id_Lte: Int!, stringField_Contains: String!, stringField_Endswith: String!, stringField_Icontains: String!, stringField_In: [String!]!, stringField_Iregex: String!, stringField_Isnull: Boolean!, stringField_Regex: String!, stringField_Startswith: String!): TestModelFKSourceList!
                }
                
                type FkTarget2 {
                  id: Int!
                  intField: Int!
                  fkSources(id_Exact: Int!, id_Gt: Int!, id_Gte: Int!, id_In: [Int!]!, id_Isnull: Boolean!, id_Lt: Int!, id_Lte: Int!, stringField_Contains: String!, stringField_Endswith: String!, stringField_Icontains: String!, stringField_In: [String!]!, stringField_Iregex: String!, stringField_Isnull: Boolean!, stringField_Regex: String!, stringField_Startswith: String!): TestModelFKSourceList!
                }
                
                type Query {
                  fkTarget2Detail(id: Int!): FkTarget2!
                  fKTargetDetail(id: Int!): FKTarget!
                  fKSourceDetail(id: Int!): FKSource!
                }
                
                type TestModelFKSourceList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKSource!]!
                }
                """
            )
        )
