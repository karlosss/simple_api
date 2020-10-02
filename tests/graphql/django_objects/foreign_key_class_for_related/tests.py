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
                
                type FKSource {
                  id: Int!
                  string_field: String!
                  fk_field: FKTarget!
                  one_to_one_field: FKTarget!
                }
                
                type FKSource2 {
                  id: Int!
                  string_field: String!
                  fk_field: FKTarget!
                  one_to_one_field: FKTarget!
                }
                
                input FKSource2CreateInput {
                  string_field: String!
                  fk_field_id: Int!
                  one_to_one_field_id: Int!
                }
                
                type FKSource2List {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKSource2!]!
                }
                
                input FKSource2UpdateInput {
                  string_field: String
                  fk_field_id: Int
                  one_to_one_field_id: Int
                }
                
                input FKSourceCreateInput {
                  string_field: String!
                  fk_field_id: Int!
                  one_to_one_field_id: Int!
                }
                
                type FKSourceList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKSource!]!
                }
                
                input FKSourceUpdateInput {
                  string_field: String
                  fk_field_id: Int
                  one_to_one_field_id: Int
                }
                
                type FKTarget {
                  id: Int!
                  int_field: Int!
                  fk_sources(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field: String, string_field__contains: String, string_field__endswith: String, string_field__exact: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, fk_field_id: Int, fk_field_id__exact: Int, fk_field_id__gt: Int, fk_field_id__gte: Int, fk_field_id__in: [Int!], fk_field_id__isnull: Boolean, fk_field_id__lt: Int, fk_field_id__lte: Int, one_to_one_field_id: Int, one_to_one_field_id__exact: Int, one_to_one_field_id__gt: Int, one_to_one_field_id__gte: Int, one_to_one_field_id__in: [Int!], one_to_one_field_id__isnull: Boolean, one_to_one_field_id__lt: Int, one_to_one_field_id__lte: Int, ordering: [String!]): FKSourceList!
                  one_to_one_rel: FKSource
                }
                
                type FKTarget2 {
                  id: Int!
                  int_field: Int!
                  fk_sources(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field: String, string_field__contains: String, string_field__endswith: String, string_field__exact: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, fk_field_id: Int, fk_field_id__exact: Int, fk_field_id__gt: Int, fk_field_id__gte: Int, fk_field_id__in: [Int!], fk_field_id__isnull: Boolean, fk_field_id__lt: Int, fk_field_id__lte: Int, one_to_one_field_id: Int, one_to_one_field_id__exact: Int, one_to_one_field_id__gt: Int, one_to_one_field_id__gte: Int, one_to_one_field_id__in: [Int!], one_to_one_field_id__isnull: Boolean, one_to_one_field_id__lt: Int, one_to_one_field_id__lte: Int, ordering: [String!]): FKSourceList!
                  one_to_one_rel: FKSource
                }
                
                input FKTarget2CreateInput {
                  int_field: Int!
                }
                
                type FKTarget2List {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKTarget2!]!
                }
                
                input FKTarget2UpdateInput {
                  int_field: Int
                }
                
                input FKTargetCreateInput {
                  int_field: Int!
                }
                
                type FKTargetList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [FKTarget!]!
                }
                
                input FKTargetUpdateInput {
                  int_field: Int
                }
                
                type Mutation {
                  FKSourceCreate(data: FKSourceCreateInput!): FKSource!
                  FKSourceUpdate(data: FKSourceUpdateInput!, id: Int!): FKSource!
                  FKSourceDelete(id: Int!): Boolean!
                  FKSource2Create(data: FKSource2CreateInput!): FKSource2!
                  FKSource2Update(data: FKSource2UpdateInput!, id: Int!): FKSource2!
                  FKSource2Delete(id: Int!): Boolean!
                  FKTargetCreate(data: FKTargetCreateInput!): FKTarget!
                  FKTargetUpdate(data: FKTargetUpdateInput!, id: Int!): FKTarget!
                  FKTargetDelete(id: Int!): Boolean!
                  FKTarget2Create(data: FKTarget2CreateInput!): FKTarget2!
                  FKTarget2Update(data: FKTarget2UpdateInput!, id: Int!): FKTarget2!
                  FKTarget2Delete(id: Int!): Boolean!
                }
                
                type Query {
                  FKTarget2Detail(id: Int!): FKTarget2!
                  FKTarget2List(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): FKTarget2List!
                  FKTargetDetail(id: Int!): FKTarget!
                  FKTargetList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, int_field: Int, int_field__exact: Int, int_field__gt: Int, int_field__gte: Int, int_field__in: [Int!], int_field__isnull: Boolean, int_field__lt: Int, int_field__lte: Int, ordering: [String!]): FKTargetList!
                  FKSource2Detail(id: Int!): FKSource2!
                  FKSource2List(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field: String, string_field__contains: String, string_field__endswith: String, string_field__exact: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, fk_field_id: Int, fk_field_id__exact: Int, fk_field_id__gt: Int, fk_field_id__gte: Int, fk_field_id__in: [Int!], fk_field_id__isnull: Boolean, fk_field_id__lt: Int, fk_field_id__lte: Int, one_to_one_field_id: Int, one_to_one_field_id__exact: Int, one_to_one_field_id__gt: Int, one_to_one_field_id__gte: Int, one_to_one_field_id__in: [Int!], one_to_one_field_id__isnull: Boolean, one_to_one_field_id__lt: Int, one_to_one_field_id__lte: Int, ordering: [String!]): FKSource2List!
                  FKSourceDetail(id: Int!): FKSource!
                  FKSourceList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, string_field: String, string_field__contains: String, string_field__endswith: String, string_field__exact: String, string_field__icontains: String, string_field__in: [String!], string_field__iregex: String, string_field__isnull: Boolean, string_field__regex: String, string_field__startswith: String, fk_field_id: Int, fk_field_id__exact: Int, fk_field_id__gt: Int, fk_field_id__gte: Int, fk_field_id__in: [Int!], fk_field_id__isnull: Boolean, fk_field_id__lt: Int, fk_field_id__lte: Int, one_to_one_field_id: Int, one_to_one_field_id__exact: Int, one_to_one_field_id__gt: Int, one_to_one_field_id__gte: Int, one_to_one_field_id__in: [Int!], one_to_one_field_id__isnull: Boolean, one_to_one_field_id__lt: Int, one_to_one_field_id__lte: Int, ordering: [String!]): FKSourceList!
                }
                """
            )
        )

    def test_requests(self):
        # create
        resp = self.query(
            """
            mutation create{
              createTarget1: FKTargetCreate(data: {int_field: 10}){
                id
              }
              createTarget2: FKTarget2Create(data: {int_field: 20}){
                id
              }
              createTarget3: FKTargetCreate(data: {int_field: 30}){
                id
              }
              createTarget4: FKTargetCreate(data: {int_field: 40}){
                id
              }
              createSource1: FKSourceCreate(data: {string_field: "A", fk_field_id: 1, one_to_one_field_id: 2}){
                id
              }
              createSource2: FKSource2Create(data: {string_field: "B", fk_field_id: 1, one_to_one_field_id: 3}){
                id
              }
              createSource3: FKSourceCreate(data: {string_field: "C", fk_field_id: 2, one_to_one_field_id: 1}){
                id
              }
            }
            """
        )
        exp = {
          "data": {
            "createTarget1": {
              "id": 1
            },
            "createTarget2": {
              "id": 2
            },
            "createTarget3": {
              "id": 3
            },
            "createTarget4": {
              "id": 4
            },
            "createSource1": {
              "id": 1
            },
            "createSource2": {
              "id": 2
            },
            "createSource3": {
              "id": 3
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # detail
        resp = self.query(
            """
            query{
              FKTargetDetail(id: 1){
                id
                int_field
                fk_sources{
                  count
                  data{
                    id
                    string_field
                    one_to_one_field{
                      id
                    }
                  }
                }
                one_to_one_rel{
                  id
                  string_field
                  fk_field{
                    id
                  }
                  one_to_one_field{
                    id
                  }
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "FKTargetDetail": {
              "id": 1,
              "int_field": 10,
              "fk_sources": {
                "count": 2,
                "data": [
                  {
                    "id": 1,
                    "string_field": "A",
                    "one_to_one_field": {
                      "id": 2
                    }
                  },
                  {
                    "id": 2,
                    "string_field": "B",
                    "one_to_one_field": {
                      "id": 3
                    }
                  }
                ]
              },
              "one_to_one_rel": {
                "id": 3,
                "string_field": "C",
                "fk_field": {
                  "id": 2
                },
                "one_to_one_field": {
                  "id": 1
                }
              }
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # list
        resp = self.query(
            """
            query{
              FKTargetList{
                count
                data{
                  id
                  int_field
                  fk_sources{
                    count
                    data{
                      id
                    }
                  }
                  one_to_one_rel{
                    id
                  }
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "FKTargetList": {
              "count": 4,
              "data": [
                {
                  "id": 1,
                  "int_field": 10,
                  "fk_sources": {
                    "count": 2,
                    "data": [
                      {
                        "id": 1
                      },
                      {
                        "id": 2
                      }
                    ]
                  },
                  "one_to_one_rel": {
                    "id": 3
                  }
                },
                {
                  "id": 2,
                  "int_field": 20,
                  "fk_sources": {
                    "count": 1,
                    "data": [
                      {
                        "id": 3
                      }
                    ]
                  },
                  "one_to_one_rel": {
                    "id": 1
                  }
                },
                {
                  "id": 3,
                  "int_field": 30,
                  "fk_sources": {
                    "count": 0,
                    "data": []
                  },
                  "one_to_one_rel": {
                    "id": 2
                  }
                },
                {
                  "id": 4,
                  "int_field": 40,
                  "fk_sources": {
                    "count": 0,
                    "data": []
                  },
                  "one_to_one_rel": None
                }
              ]
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # update
        resp = self.query(
            """
            mutation update{
              FKSourceUpdate(id: 1, data: {fk_field_id: 3}){
                id
              }
            }
            """
        )
        exp = {
          "data": {
            "FKSourceUpdate": {
              "id": 1
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # check updated value
        resp = self.query(
            """
            query{
              FKSourceDetail(id: 1){
                id
                fk_field{
                  id
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "FKSourceDetail": {
              "id": 1,
              "fk_field": {
                "id": 3
              }
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # delete
        resp = self.query(
            """
            mutation delete{
              FKSourceDelete(id: 1)
            }
            """
        )
        exp = {
          "data": {
            "FKSourceDelete": True
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # check missing value
        resp = self.query(
            """
            query{
              FKSource2List{
                count
                data{
                  id
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "FKSource2List": {
              "count": 2,
              "data": [
                {
                  "id": 2
                },
                {
                  "id": 3
                }
              ]
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
