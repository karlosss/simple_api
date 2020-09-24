from inspect import isclass

from constants import OBJECT_SELF_REFERENCE
from object.object import Object
from object.registry import object_storage


class Type:
    def __init__(self, nullable=False, default=None, parameters=None, resolver=None,
                 nullable_if_input=None, default_if_input=None):
        self.parent_class = None
        self._nullable = nullable
        self._default = default
        self.parameters = parameters or {}
        self.resolver = resolver
        self._nullable_if_input = nullable_if_input
        self._default_if_input = default_if_input

    def set_parent_class(self, cls):
        self.parent_class = cls

    def nullable(self, input=False):
        if not input:
            return self._nullable
        if self._nullable_if_input is None:
            return self._nullable
        return self._nullable_if_input

    def default(self, input=False):
        if not input:
            return self._default
        if self._default_if_input is None:
            return self._default
        return self._default_if_input

    def convert(self, adapter, **kwargs):
        return adapter.convert_field(self, **kwargs)

    def to_string(self):
        return "Type"

    def __str__(self):
        return "{}{}".format(self.to_string(), "" if self.nullable() else "!")

    def __repr__(self):
        return str(self)


class PrimitiveType(Type):
    pass


class IntegerType(PrimitiveType):
    def to_string(self):
        return "Integer"


class FloatType(PrimitiveType):
    def to_string(self):
        return "Float"


class StringType(PrimitiveType):
    def to_string(self):
        return "String"


class BooleanType(PrimitiveType):
    def to_string(self):
        return "Boolean"


class DateType(PrimitiveType):
    def to_string(self):
        return "Date"


class TimeType(PrimitiveType):
    def to_string(self):
        return "Time"


class DateTimeType(PrimitiveType):
    def to_string(self):
        return "DateTime"


class ObjectType(Type):
    _set_ref_handler = None  # Django model handler goes here - this way, we don't mix layers

    def __init__(self, to, nullable=False, default=None, parameters=None, resolver=None,
                 nullable_if_input=None, default_if_input=None):
        super().__init__(nullable=nullable, default=default, parameters=parameters, resolver=resolver,
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input)
        self.to = to

    def get_parent_class(self):
        assert self.parent_class is not None, \
            "`{}` is not allowed reference for actions without associated object. " \
            "Pass either class reference, or an absolute module path.".format(self.to)
        return self.parent_class

    def set_ref(self):
        if ObjectType._set_ref_handler is not None:
            ObjectType._set_ref_handler(self)

        if isclass(self.to) and issubclass(self.to, Object):
            pass
        elif self.to == OBJECT_SELF_REFERENCE:
            self.to = self.get_parent_class()
        elif "." not in self.to:
            self.to = object_storage.get(self.get_parent_class().__module__, self.to)
        else:
            self.to = object_storage.get(*self.to.rsplit(".", 1))

    def convert(self, adapter, **kwargs):
        self.set_ref()
        return super().convert(adapter, **kwargs)

    def to_string(self):
        if isclass(self.to):
            return self.to.__name__
        return self.to


class PlainListType(Type):
    def __init__(self, of, nullable=False, default=None, parameters=None, resolver=None,
                 nullable_if_input=None, default_if_input=None):
        super().__init__(nullable=nullable, default=default, parameters=parameters, resolver=resolver,
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input)
        self.of = of

    def set_parent_class(self, cls):
        self.of.set_parent_class(cls)
        super().set_parent_class(cls)

    def to_string(self):
        return "[{}]".format(self.of)
