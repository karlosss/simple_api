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
                
                type CarObject {
                  id: Int!
                  brand: String!
                  owner: PersonObject!
                }
                
                input CarObjectCreateInput {
                  brand: String!
                  owner_id: Int!
                }
                
                type CarObjectList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [CarObject!]!
                }
                
                input CarObjectUpdateInput {
                  brand: String
                  owner_id: Int
                }
                
                type Mutation {
                  PersonObjectCreate(data: PersonObjectCreateInput!): PersonObject!
                  PersonObjectUpdate(data: PersonObjectUpdateInput!, id: Int!): PersonObject!
                  PersonObjectDelete(id: Int!): Boolean!
                  CarObjectCreate(data: CarObjectCreateInput!): CarObject!
                  CarObjectUpdate(data: CarObjectUpdateInput!, id: Int!): CarObject!
                  CarObjectDelete(id: Int!): Boolean!
                }
                
                type PersonObject {
                  id: Int!
                  age: Int!
                  car_set(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, brand: String, brand__contains: String, brand__endswith: String, brand__exact: String, brand__icontains: String, brand__in: [String!], brand__iregex: String, brand__isnull: Boolean, brand__regex: String, brand__startswith: String, owner__age: Int, owner__age__exact: Int, owner__age__gt: Int, owner__age__gte: Int, owner__age__in: [Int!], owner__age__isnull: Boolean, owner__age__lt: Int, owner__age__lte: Int, ordering: [String!]): CarObjectList!
                }
                
                input PersonObjectCreateInput {
                  age: Int!
                }
                
                type PersonObjectList {
                  count: Int!
                  data(limit: Int = 20, offset: Int = 0): [PersonObject!]!
                }
                
                input PersonObjectUpdateInput {
                  age: Int
                }
                
                type Query {
                  CarObjectDetail(id: Int!): CarObject!
                  CarObjectList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, brand: String, brand__contains: String, brand__endswith: String, brand__exact: String, brand__icontains: String, brand__in: [String!], brand__iregex: String, brand__isnull: Boolean, brand__regex: String, brand__startswith: String, owner__age: Int, owner__age__exact: Int, owner__age__gt: Int, owner__age__gte: Int, owner__age__in: [Int!], owner__age__isnull: Boolean, owner__age__lt: Int, owner__age__lte: Int, ordering: [String!]): CarObjectList!
                  PersonObjectDetail(id: Int!): PersonObject!
                  PersonObjectList(id: Int, id__exact: Int, id__gt: Int, id__gte: Int, id__in: [Int!], id__isnull: Boolean, id__lt: Int, id__lte: Int, age: Int, age__exact: Int, age__gt: Int, age__gte: Int, age__in: [Int!], age__isnull: Boolean, age__lt: Int, age__lte: Int, ordering: [String!]): PersonObjectList!
                }
                """
            )
        )

    def test_requests(self):
        # create
        resp = self.query(
            """
            mutation create{
              person: PersonObjectCreate(data: {age: 20}){
                id
                age
              }
              car1: CarObjectCreate(data: {brand: "Renault", owner_id: 1}){
                id
                brand
                owner{
                  id
                }
              }
              car2: CarObjectCreate(data: {brand: "BMW", owner_id: 1}){
                id
                brand
                owner{
                  id
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "person": {
              "id": 1,
              "age": 20
            },
            "car1": {
              "id": 1,
              "brand": "Renault",
              "owner": {
                "id": 1
              }
            },
            "car2": {
              "id": 2,
              "brand": "BMW",
              "owner": {
                "id": 1
              }
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

        # test filter
        resp = self.query(
            """
            query{
              detail1: PersonObjectDetail(id: 1){
                car_set(owner__age__lt: 25){
                  count
                  data{
                    id
                    brand
                  }
                }
              }
              detail2: PersonObjectDetail(id: 1){
                car_set(owner__age__lt: 15){
                  count
                  data{
                    id
                    brand
                  }
                }
              }
            }
            """
        )
        exp = {
          "data": {
            "detail1": {
              "car_set": {
                "count": 2,
                "data": [
                  {
                    "id": 1,
                    "brand": "Renault"
                  },
                  {
                    "id": 2,
                    "brand": "BMW"
                  }
                ]
              }
            },
            "detail2": {
              "car_set": {
                "count": 0,
                "data": []
              }
            }
          }
        }
        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
