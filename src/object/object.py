from copy import deepcopy

from django.utils.decorators import classproperty

from object.datatypes import PlainListType, ObjectType
from object.permissions import AllowAll, permissions_pre_hook
from object.registry import object_storage


class ObjectMeta(type):
    base_class = "object.object.Object"

    @classmethod
    def inject_references(mcs, cls):
        for field in {**cls.fields, **cls.input_fields, **cls.output_fields}.values():
            field.set_parent_class(cls)
            if not field.resolver.pre_hook_set:
                field.resolver.set_pre_hook(permissions_pre_hook(cls.default_fields_permission))

        for action_name, action in cls.actions.items():
            action.set_parent_class(cls)
            action.set_name(action_name)
            if not action.permissions:
                action.set_permissions(cls.default_actions_permission)

        if not getattr(cls, "hidden", False) and "__actions" not in cls.out_fields:
            cls.output_fields["__actions"] = PlainListType(ObjectType("ActionInfo"))

            def resolver(**kwargs):
                raise
            cls.output_fields["__actions"].resolver.set_main_hook(resolver)

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        if kwargs.get("skip", False) or object_storage.key_for_class(attrs.get("__module__", None), name) == mcs.base_class:
            return cls

        # store class stub
        object_storage.store(kwargs.get("module", None) or cls.__module__, name, cls)

        cls.fields = deepcopy(cls.fields)
        cls.input_fields = deepcopy(cls.input_fields)
        cls.output_fields = deepcopy(cls.output_fields)
        cls.actions = deepcopy(cls.actions)

        if "module" in kwargs:
            cls.__module__ = kwargs["module"]

        if not kwargs.get("no_inject", False):
            mcs.inject_references(cls)

        return cls


class Object(metaclass=ObjectMeta):
    fields = {}
    input_fields = {}
    output_fields = {}
    actions = {}

    default_fields_permission = AllowAll
    default_actions_permission = AllowAll
    default_field_validators = {}

    @classproperty
    def in_fields(cls):
        for f in cls.input_fields:
            assert f not in cls.fields, "Redefinition of `{}` field.".format(f)
        return {**cls.fields, **cls.input_fields}

    @classproperty
    def out_fields(cls):
        for f in cls.output_fields:
            assert f not in cls.fields, "Redefinition of `{}` field.".format(f)
        return {**cls.fields, **cls.output_fields}
