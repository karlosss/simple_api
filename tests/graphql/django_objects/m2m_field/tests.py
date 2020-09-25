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
                  m2m_field(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): TestModelM2MTargetList!
                }
                
                type M2MTarget {
                  id: Int!
                  int_field: Int!
                  m2m_sources(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, ordering: [String!]): TestModelM2MSourceList!
                }
                
                type Query {
                  M2MTargetDetail(id: Int!): M2MTarget!
                  M2MSourceDetail(id: Int!): M2MSource!
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
