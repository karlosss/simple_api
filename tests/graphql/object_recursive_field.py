from django.urls import reverse_lazy
from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import IntegerField, StringField, ObjectField
from object.object import Object


def resolve_show(*args, **kwargs):
    return f'Hefllo {kwargs["id"]}!'


class Publisher(Object):
    fields = {
        "name": StringField()
    }

    actions = {
        "show": Action({"id": IntegerField()}, StringField(), resolve_show)
    }


# schema = generate(GraphQLAdapter, [Publisher])


# class SimpleFieldsTestCase(GraphQLTestCase):
#     GRAPHQL_SCHEMA = schema
#     GRAPHQL_URL = reverse_lazy("simple_fields")
#
#     def test_book_detail(self):
#         response = self.query(
#             """
#             query {
#                 nodeDetail(id: 1) {
#                     value
#                     next {
#                         value
#                         next
#                     }
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
#         self.assertResponseNoErrors(response)
#         self.assertJSONEqual(response.content, expected)
