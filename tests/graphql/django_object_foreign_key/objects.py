from django.urls import path
from graphene_django.views import GraphQLView

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import TestModelFKSource, TestModelFKTarget


class FKSource(DjangoObject):
    model = TestModelFKSource


class FKTarget(DjangoObject):
    model = TestModelFKTarget


class FkTarget2(DjangoObject):
    model = TestModelFKTarget
    class_for_related = False


schema = generate(GraphQLAdapter)
patterns = [path("api/", GraphQLView.as_view(graphiql=True, schema=schema))]
