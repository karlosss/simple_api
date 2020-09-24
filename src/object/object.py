from django.utils.decorators import classproperty

from object.registry import object_storage


class ObjectMeta(type):
    base_class = "object.object.Object"

    @classmethod
    def inject_references(mcs, cls):
        for field in {**cls.fields, **cls.input_fields, **cls.output_fields}.values():
            field.set_parent_class(cls)

        for action in cls.actions.values():
            action.set_parent_class(cls)

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)
        if kwargs.get("skip", False) or object_storage.key_for_class(attrs.get("__module__", None), name) == mcs.base_class:
            return cls

        # store class stub
        object_storage.store(cls.__module__, name, cls)

        if not kwargs.get("no_inject", False):
            mcs.inject_references(cls)

        return cls


class Object(metaclass=ObjectMeta):
    fields = {}
    input_fields = {}
    output_fields = {}
    actions = {}

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
