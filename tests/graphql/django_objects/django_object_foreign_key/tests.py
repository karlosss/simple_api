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
                
                type FKSource {
                  id: Int!
                  string_field: String!
                  fk_field: FKTarget!
                  one_to_one_field: FKTarget!
                }
                
                type FKTarget {
                  id: Int!
                  int_field: Int!
                  fk_sources(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field__contains: String, string_field__endswith: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, ordering: [String!]): TestModelFKSourceList!
                }
                
                type FkTarget2 {
                  id: Int!
                  int_field: Int!
                  fk_sources(id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field__contains: String, string_field__endswith: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, ordering: [String!]): TestModelFKSourceList!
                }
                
                type Query {
                  FkTarget2Detail(id: Int!): FkTarget2!
                  FKTargetDetail(id: Int!): FKTarget!
                  FKSourceDetail(id: Int!): FKSource!
                }
                
                type TestModelFKSourceList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKSource!]!
                }
                """
            )
        )
