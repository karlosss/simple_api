from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate_w
from simple_api.django_object.django_object import DjangoObject
from simple_api.object.actions import Action
from simple_api.object.datatypes import StringType

from simple_api.adapters.graphql.utils import build_patterns_w

from .models import Book as BookModel, Bookmark as BookmarkModel


class Book(DjangoObject):
    model = BookModel
    field_difficulty_scores = {"shelf": 200001}


class Bookmark(DjangoObject):
    model = BookmarkModel


def ping(**kwargs):
    return "Action run"


actions = {
    "Heavy_Action": Action(return_value=StringType(), exec_fn=ping, action_weight=100001),
    "Light_Action": Action(return_value=StringType(), exec_fn=ping, action_weight=1)
}

schema, weight_schema = generate_w(GraphQLAdapter, actions)
patterns = build_patterns_w("api/", schema, weight_schema)
