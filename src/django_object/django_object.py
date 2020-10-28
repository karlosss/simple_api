from copy import deepcopy

from django_object.actions import DetailAction, ListAction, ModelAction, CreateAction, UpdateAction, DeleteAction
from django_object.datatypes import create_associated_list_type
from django_object.filters import generate_filters
from django_object.converter import determine_simple_api_fields
from django_object.utils import get_pk_field_name
from object.object import Object, ObjectMeta
from object.registry import object_storage
from django_object.registry import model_django_object_storage


class DjangoObjectMeta(ObjectMeta):
    base_class = "django_object.django_object.DjangoObject"

    @classmethod
    def inject_references(mcs, cls):
        for action_name, action in cls.actions.items():
            # for a model action, set the class so that the action knows which model belongs to it and it can
            # determine the parameters; after that, we can treat it normally
            if isinstance(action, ModelAction):
                action.set_parent_class(cls)
                action.set_name(action_name)
                action.determine_parameters()

        super().inject_references(cls)

    def __new__(mcs, name, bases, attrs, **kwargs):
        if kwargs.get("skip", False) or object_storage.key_for_class(attrs["__module__"], name) == mcs.base_class:
            return super().__new__(mcs, name, bases, attrs, skip=True, **kwargs)

        assert "fields" not in attrs, "`DjangoObject` cannot override `fields`."
        assert "input_fields" not in attrs, "`DjangoObject` cannot override `input_fields`."
        assert "output_fields" not in attrs, "`DjangoObject` cannot override `output_fields`."
        assert "actions" not in attrs, "`DjangoObject` cannot override `actions`."

        cls = super().__new__(mcs, name, bases, attrs, no_inject=True, **kwargs)

        cls.pk_field = get_pk_field_name(cls.model)
        if cls.only_fields is not None and cls.pk_field not in cls.only_fields:
            cls.only_fields = cls.only_fields + (cls.pk_field,)

        cls.custom_fields = deepcopy(cls.custom_fields)
        cls.input_custom_fields = deepcopy(cls.input_custom_fields)
        cls.output_custom_fields = deepcopy(cls.output_custom_fields)
        cls.custom_actions = deepcopy(cls.custom_actions)

        cls.fields, cls.input_fields, cls.output_fields, field_validators = determine_simple_api_fields(
            cls.model,
            cls.only_fields, cls.exclude_fields,
            cls.custom_fields, cls.input_custom_fields, cls.output_custom_fields,
        )

        cls.filters = generate_filters(cls)

        if cls.class_for_related:
            model_django_object_storage.store(cls.model, cls)

        cls.actions = {}

        if cls.detail_action:
            cls.actions["detail"] = deepcopy(cls.detail_action)
        if cls.list_action:
            cls.actions["list"] = deepcopy(cls.list_action)
        if cls.create_action:
            cls.actions["create"] = deepcopy(cls.create_action)
        if cls.update_action:
            cls.actions["update"] = deepcopy(cls.update_action)
        if cls.delete_action:
            cls.actions["delete"] = deepcopy(cls.delete_action)

        cls.actions.update(cls.custom_actions)

        mcs.inject_references(cls)

        create_associated_list_type(cls)

        return cls


class DjangoObject(Object, metaclass=DjangoObjectMeta):
    model = None
    class_for_related = True

    only_fields = None
    exclude_fields = None

    custom_fields = {}
    input_custom_fields = {}
    output_custom_fields = {}

    detail_action = DetailAction()
    list_action = ListAction()
    create_action = CreateAction()
    update_action = UpdateAction()
    delete_action = DeleteAction()
    custom_actions = {}
