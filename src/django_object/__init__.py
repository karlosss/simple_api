from inspect import isclass

from django.db.models import Model

from django_object.registry import model_django_object_storage
from object.datatypes import ObjectType


def model_set_ref_handler(object_type):
    if isclass(object_type.to) and issubclass(object_type.to, Model):
        object_type.to = model_django_object_storage.get(object_type.to)


ObjectType._set_ref_handler = model_set_ref_handler
