from enum import Enum

from graphene_django.views import GraphQLView
from django.urls import path

from simple_api.adapters.graphql.security.disable_introspection import DisableIntrospectionMiddleware
from simple_api.adapters.graphql.security.security import PreflightQueryManager


class ConversionType(Enum):
    # type conversions
    OUTPUT = 1
    INPUT = 2
    LIST_OUTPUT = 3
    LIST_INPUT = 4
    PARAMETER = 5

    # function conversions
    EXEC_FN = 6
    RESOLVER = 7


def is_mutation(action):
    return action.kwargs.get("mutation", False)  # todo list of mutation actions


def capitalize(string):
    return string[0].upper() + string[1:]


def build_patterns(url_path, schema, **kwargs):
    return [path(url_path, GraphQLView.as_view(graphiql=True,
                                               schema=schema,
                                               backend=PreflightQueryManager(),
                                               middleware=[DisableIntrospectionMiddleware()], **kwargs))]
