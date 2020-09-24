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
                }
                
                type M2MSource {
                  id: Int!
                  m2mField(id_Exact: Int!, id_Gt: Int!, id_Gte: Int!, id_In: [Int!]!, id_Isnull: Boolean!, id_Lt: Int!, id_Lte: Int!, intField_Exact: Int!, intField_Gt: Int!, intField_Gte: Int!, intField_In: [Int!]!, intField_Isnull: Boolean!, intField_Lt: Int!, intField_Lte: Int!): TestModelM2MTargetList!
                }
                
                type M2MTarget {
                  id: Int!
                  intField: Int!
                  m2mSources(id_Exact: Int!, id_Gt: Int!, id_Gte: Int!, id_In: [Int!]!, id_Isnull: Boolean!, id_Lt: Int!, id_Lte: Int!): TestModelM2MSourceList!
                }
                
                type Query {
                  m2MTargetDetail(id: Int!): M2MTarget!
                  m2MSourceDetail(id: Int!): M2MSource!
                }
                
                type TestModelM2MSourceList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [M2MSource!]!
                }
                
                type TestModelM2MTargetList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [M2MTarget!]!
                }
                """
            )
        )
