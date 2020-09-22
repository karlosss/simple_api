import datetime

from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from testcases.models import TestModelPrimitiveFields
from tests.graphql_test_utils import get_graphql_url, remove_ws


class TestModelObjectAllFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False


class TestModelObjectOnlyFields(DjangoObject):
    model = TestModelPrimitiveFields
    only_fields = ("int_field", "float_field")


class TestModelObjectExcludeFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False
    exclude_fields = ("string_char_field", "string_text_field")


schema = generate(GraphQLAdapter, [TestModelObjectAllFields, TestModelObjectOnlyFields, TestModelObjectExcludeFields])


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = get_graphql_url(__file__)

    def setUp(self):
        TestModelPrimitiveFields.objects.create(
            int_field=0,
            float_field=1.5,
            string_char_field="CharField holding a short text",
            string_text_field="TextField holding a loooooooooooooooooong text",
            bool_field=True,
            date_field=datetime.date(year=2020, month=1, day=1),
            time_field=datetime.time(hour=12, minute=34, second=56),
            date_time_field=datetime.datetime(year=2020, month=1, day=1, hour=12, minute=34, second=56)
        )

    def test_all(self):
        resp = self.query(
            """
            query{
              testModelObjectAllFieldsDetail(id: 1){
                id
                intField
                floatField
                stringCharField
                stringTextField
                boolField
                dateField
                timeField
                dateTimeField
              }
            }
            """
        )

        exp = {
            "data": {
                "testModelObjectAllFieldsDetail": {
                    "id": 1,
                    "intField": 0,
                    "floatField": 1.5,
                    "stringCharField": "CharField holding a short text",
                    "stringTextField": "TextField holding a loooooooooooooooooong text",
                    "boolField": True,
                    "dateField": "2020-01-01",
                    "timeField": "12:34:56",
                    "dateTimeField": "2020-01-01T12:34:56+00:00"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
