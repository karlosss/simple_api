from copy import deepcopy

from django_object.actions import DetailAction
from django_object.utils import convert_fields_to_simple_api, filter_fields_from_model
from object.object import Object, ObjectMeta
from object.registry import object_meta_storage
from django_object.registry import django_object_meta_storage


class DjangoObjectMeta(ObjectMeta):
    base_class = "django_object.django_object.DjangoObject"

    @classmethod
    def inject_references(mcs, cls):
        if "detail" in cls.actions:
            # sets just the class, parameters and return value are still None; this is important so that the action
            # can read the model from it
            cls.actions["detail"].set_parent_class(cls)

            # with the knowledge of the model, we can now determine parameters and finish the setup
            cls.actions["detail"].determine_parameters()
            cls.actions["detail"].set_parent_class(cls)

        super().inject_references(cls)

    def __new__(mcs, name, bases, attrs, **kwargs):
        if kwargs.get("skip", False) or object_meta_storage.key_for_class(attrs["__module__"], name) == mcs.base_class:
            return super().__new__(mcs, name, bases, attrs, skip=True, **kwargs)

        assert "fields" not in attrs, "`DjangoObject` cannot override `fields`."
        assert "input_fields" not in attrs, "`DjangoObject` cannot override `input_fields`."
        assert "output_fields" not in attrs, "`DjangoObject` cannot override `output_fields`."
        # assert "actions" not in attrs, "`DjangoObject` cannot override `actions`."

        cls = super().__new__(mcs, name, bases, attrs, no_inject=True, **kwargs)

        if cls.class_for_related:
            django_object_meta_storage.store_class(cls.model, cls)

        cls.fields = convert_fields_to_simple_api(
            filter_fields_from_model(cls.model, cls.only_fields, cls.exclude_fields)
        )

        cls.actions = {}
        if cls.detail_action:
            cls.actions["detail"] = deepcopy(cls.detail_action)

        # todo check extra actions for reserved keyword actions

        cls.actions.update(cls.extra_actions)

        mcs.inject_references(cls)

        return cls


class DjangoObject(Object, metaclass=DjangoObjectMeta):
    model = None
    class_for_related = True

    only_fields = None
    exclude_fields = None
    extra_fields = {}

    extra_actions = {}

    detail_action = DetailAction()
