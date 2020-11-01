from copy import deepcopy
from inspect import isclass

from django.db.models import Model

from adapters.utils import TemplateGenerator
from django_object.django_object import DjangoObjectMeta, DjangoObject
from django_object.registry import model_django_object_storage
from object.datatypes import ObjectType


def model_set_ref_handler(object_type):
    if isclass(object_type.to) and issubclass(object_type.to, Model):
        object_type.to = model_django_object_storage.get(object_type.to).to_object()
    elif isclass(object_type.to) and issubclass(object_type.to, DjangoObject):
        object_type.to = object_type.to.to_object()


needed_model_classes = set()
def model_create_handler(object_type):
    if isclass(object_type.to) and issubclass(object_type.to, Model):
        needed_model_classes.add(object_type.to)


ObjectType._set_ref_handler = model_set_ref_handler
ObjectType._create_handler = model_create_handler


def generate_model_object_classes():
    classes_to_create = needed_model_classes.difference(model_django_object_storage.storage.keys())
    if not classes_to_create:
        return

    for model in classes_to_create:
        attrs = {
            "__module__": "django_object",
            "model": model,
            "create_action": None,
            "list_action": None,
            "detail_action": None,
            "update_action": None,
            "delete_action": None,
        }
        DjangoObjectMeta(model.__name__, (DjangoObject,), attrs)

    generate_model_object_classes()


TemplateGenerator.generate_pre_hook = generate_model_object_classes
