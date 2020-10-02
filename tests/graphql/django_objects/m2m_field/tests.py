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
                
                type M2MSource {
                  id: Int!
                  m2m_field(ordering: [String!], id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int): M2MTargetList!
                }
                
                type M2MSourceList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [M2MSource!]!
                }
                
                type M2MTarget {
                  id: Int!
                  int_field: Int!
                  m2m_sources(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, ordering: [String!]): M2MSourceList!
                }
                
                input M2MTargetCreateInput {
                  int_field: Int!
                }
                
                type M2MTargetList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [M2MTarget!]!
                }
                
                input M2MTargetUpdateInput {
                  int_field: Int
                }
                
                type Mutation {
                  M2MSourceCreate: M2MSource!
                  M2MSourceUpdate(id: Int!): M2MSource!
                  M2MSourceDelete(id: Int!): Boolean!
                  M2MTargetCreate(data: M2MTargetCreateInput!): M2MTarget!
                  M2MTargetUpdate(data: M2MTargetUpdateInput!, id: Int!): M2MTarget!
                  M2MTargetDelete(id: Int!): Boolean!
                }
                
                type Query {
                  M2MTargetDetail(id: Int!): M2MTarget!
                  M2MTargetList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): M2MTargetList!
                  M2MSourceDetail(id: Int!): M2MSource!
                  M2MSourceList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, ordering: [String!]): M2MSourceList!
                }
                """
            )
        )

        # TODO design many-to-many field without intermediate model
