from enum import Enum

from django.urls import path
from graphene_django.views import GraphQLView
from django.conf import settings

from simple_api.adapters.graphql.security.DifficultyScoreGraphQLView import DifficultyScoreGraphQLView
from simple_api.adapters.graphql.security.disable_introspection import DisableIntrospectionMiddleware


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
                                               **kwargs))]


def build_patterns_w(url_path, schema, weight_schema, default_introspection=False, middleware=None, **kwargs):
    list_limit = None
    depth_limit = None
    weight_limit = None
    action_limit = None
    settings_dict = getattr(settings, "SIMPLE_API", None)
    if settings_dict and "SECURITY" in settings_dict:
        if "LIST_LIMIT" in settings_dict["SECURITY"]:
            list_limit = settings_dict["SECURITY"]["LIST_LIMIT"]
        if "DEPTH_LIMIT" in settings_dict["SECURITY"]:
            depth_limit = settings_dict["SECURITY"]["DEPTH_LIMIT"]
        if "WEIGHT_LIMIT" in settings_dict["SECURITY"]:
            weight_limit = settings_dict["SECURITY"]["WEIGHT_LIMIT"]

    middleware_list = []
    if isinstance(middleware, list):
        middleware_list = middleware

    if not default_introspection:
        middleware_list.append(DisableIntrospectionMiddleware())

    return [path(url_path, DifficultyScoreGraphQLView.as_view(graphiql=True,
                                                              schema=schema,
                                                              sec_weight_schema=weight_schema,
                                                              middleware=middleware_list,
                                                              weight_limit=weight_limit,
                                                              list_limit=list_limit,
                                                              depth_limit=depth_limit,
                                                              **kwargs))]
