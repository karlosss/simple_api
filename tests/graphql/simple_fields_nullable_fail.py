# from django.urls import reverse_lazy
# from graphene_django.utils import GraphQLTestCase
#
# from adapters.base import generate
# from adapters.graphql.graphql import GraphQLAdapter
# from object.fields import IntegerField, StringField
# from object.mixins import DetailMixin
# from object.object import Object
# from testcases.db import BookWithIsbnDB
# from testcases.utils import get_error_message
# from utils.data_dict import AttrDict
#
#
# class Book(DetailMixin, Object):
#     fields = {
#         "page_count": IntegerField(nullable=False),
#         "title": StringField(nullable=False),
#         "isbn": StringField(nullable=False)
#     }
#
#     def detail(self, id, *args, **kwargs):
#         return BookWithIsbnDB(id, 250, "Othello", None)
#
#
# schema = generate(GraphQLAdapter, [Book])
#
#
# class SimpleFieldsTestCase(GraphQLTestCase):
#     GRAPHQL_SCHEMA = schema
#     GRAPHQL_URL = reverse_lazy("simple_fields_nullable_fail")
#
#     def test_book_detail(self):
#         response = self.query(
#             """
#             query {
#                 bookDetail(id: 1) {
#                     id
#                     pageCount
#                     title
#                     isbn
#                 }
#             }
#             """,
#         )
#
#         self.assertResponseHasErrors(response)
#         self.assertEqual(get_error_message(response.content), 'Cannot return null for non-nullable field Book.isbn.')
