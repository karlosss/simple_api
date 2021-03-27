from copy import deepcopy

from django.utils.decorators import classproperty

from simple_api.object.datatypes import PlainListType, ObjectType, StringType
from simple_api.object.meta_resolvers import build_actions_resolver
from simple_api.object.registry import object_storage


class ObjectMeta(type):
    base_class = "simple_api.object.object.Object"

    @classmethod
    def inject_references(mcs, cls):
        for field in {**cls.fields, **cls.input_fields, **cls.output_fields}.values():
            field.set_parent_class(cls)

        for action_name, action in cls.actions.items():
            action.set_parent_class(cls)
            action.set_name(action_name)

        if not getattr(cls, "hidden", False):
            cls.output_fields["__actions"] = PlainListType(ObjectType("simple_api.object.meta_types.ActionInfo"),
                                                           resolver=build_actions_resolver(cls))

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

        cls.output_fields["__str__"] = StringType(resolver=lambda *a, **kw: kw["parent_val"]())

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
    field_difficulty_scores = {}

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

    @classproperty
    def difficulty_scores(cls):
        default_values = {k: 1 for k in cls.out_fields}
        return {**default_values, **cls.field_difficulty_scores}

    @classproperty
    def connected_fields(cls):
        connected_fields = {k: str(v) for k, v in cls.out_fields.items() if hasattr(v, 'to')}
        return connected_fields
