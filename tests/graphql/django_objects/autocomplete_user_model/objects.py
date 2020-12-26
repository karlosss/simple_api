from django.contrib.auth.models import User as UserModel

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from tests.graphql.graphql_test_utils import build_patterns


class User(DjangoObject):
    model = UserModel
    create_action = None
    update_action = None
    delete_action = None


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
