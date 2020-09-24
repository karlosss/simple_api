from django.urls import path
from graphene_django.utils import GraphQLTestCase as OriginalGraphQLTestCase
from graphene_django.views import GraphQLView


def remove_ws(s):
    return " ".join(s.split())


def build_patterns(schema):
    return [path("api/", GraphQLView.as_view(graphiql=True, schema=schema))]


class GraphQLTestCase(OriginalGraphQLTestCase):
    GRAPHQL_URL = "/api/"
