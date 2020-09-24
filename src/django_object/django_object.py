from copy import deepcopy

from django_object.actions import DetailAction, ListAction, ModelAction
from django_object.filters import model_filters_storage
from django_object.utils import filter_fields_from_model
from django_object.converter import convert_fields_to_simple_api
from object.object import Object, ObjectMeta
from object.registry import object_storage
from django_object.registry import model_django_object_storage


class DjangoObjectMeta(ObjectMeta):
    base_class = "django_object.django_object.DjangoObject"

    @classmethod
    def inject_references(mcs, cls):
        for action in cls.actions.values():
            # for a model action, set the class so that the action knows which model belongs to it and it can
            # determine the parameters; after that, we can treat it normally
            if isinstance(action, ModelAction):
                action.set_parent_class(cls)
                action.determine_parameters()

        super().inject_references(cls)

    def __new__(mcs, name, bases, attrs, **kwargs):
        if kwargs.get("skip", False) or object_storage.key_for_class(attrs["__module__"], name) == mcs.base_class:
            return super().__new__(mcs, name, bases, attrs, skip=True, **kwargs)

        assert "fields" not in attrs, "`DjangoObject` cannot override `fields`."
        assert "input_fields" not in attrs, "`DjangoObject` cannot override `input_fields`."
        assert "output_fields" not in attrs, "`DjangoObject` cannot override `output_fields`."
        # assert "actions" not in attrs, "`DjangoObject` cannot override `actions`."

        cls = super().__new__(mcs, name, bases, attrs, no_inject=True, **kwargs)

        cls.fields = convert_fields_to_simple_api(
            filter_fields_from_model(cls.model, cls.only_fields, cls.exclude_fields)
        )

        if cls.class_for_related:
            model_django_object_storage.store(cls.model, cls)
            model_filters_storage.store(cls.model, cls)

        cls.actions = {}
        if cls.detail_action:
            cls.actions["detail"] = deepcopy(cls.detail_action)
        # if cls.list_action:
        #     cls.actions["list"] = deepcopy(cls.list_action)

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

    only_filters = None
    exclude_filters = None
    extra_filters = {}

    extra_actions = {}

    detail_action = DetailAction()
    # list_action = ListAction()
