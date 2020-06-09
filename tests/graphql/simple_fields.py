from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import IntegerField, StringField
from object.object import Object
from tests.graphql_test_utils import get_graphql_url


def resolve_show(*args, **kwargs):
    return f'Hefllo {kwargs["id"]}!'


class Book(Object):
    fields = {
        "page_count": IntegerField(nullable=False),
        "title": StringField(nullable=False),
    }

    actions = {
        "show": Action({"id": IntegerField()}, StringField(), resolve_show)
    }


# schema = generate(GraphQLAdapter, [Book])


# class SimpleFieldsTestCase(GraphQLTestCase):
#     GRAPHQL_SCHEMA = schema
#     GRAPHQL_URL = get_graphql_url(__file__)
#
#     def test_book_detail(self):
#         response = self.query(
#             """
#             query {
#                 bookDetail(id: 1) {
#                     id
#                     pageCount
#                     title
#                 }
#             }
#             """,
#         )
#
#         expected = {
#             "data": {
#                 "bookDetail": {
#                     "id": 1,
#                     "pageCount": 250,
#                     "title": "Othello",
#                 }
#             }
#         }
#
#         print(self.GRAPHQL_URL)
#
#         self.assertResponseNoErrors(response)
#         self.assertJSONEqual(response.content, expected)
