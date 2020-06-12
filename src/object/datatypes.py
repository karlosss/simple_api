from inspect import isclass

from constants import OBJECT_SELF_REFERENCE, LIST_DEFAULT_OFFSET, LIST_DEFAULT_LIMIT
from object.object import ObjectMeta, Object


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


class PrimitiveType(Type):
    pass


class IntegerType(PrimitiveType):
    pass


class FloatType(PrimitiveType):
    pass


class StringType(PrimitiveType):
    pass


class BooleanType(PrimitiveType):
    pass


class ObjectType(Type):
    def __init__(self, to, nullable=False, default=None, parameters=None, resolver=None,
                 nullable_if_input=None, default_if_input=None):
        super().__init__(nullable=nullable, default=default, parameters=parameters, resolver=resolver,
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input)
        self.to = to

    def set_ref(self):
        if isclass(self.to) and issubclass(self.to, Object):
            pass
        elif self.to == OBJECT_SELF_REFERENCE:
            self.to = self.parent_class
        elif "." not in self.to:
            self.to = ObjectMeta.get_class(self.parent_class.__module__, self.to)
        else:
            self.to = ObjectMeta.get_class(*self.to.rsplit(".", 1))

    def convert(self, adapter, **kwargs):
        self.set_ref()
        return super().convert(adapter, **kwargs)


class PlainListType(Type):
    def __init__(self, of, nullable=False, default=None, parameters=None, resolver=None,
                 nullable_if_input=None, default_if_input=None):
        super().__init__(nullable=nullable, default=default, parameters=parameters, resolver=resolver,
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input)
        self.of = of

    def set_parent_class(self, cls):
        self.of.set_parent_class(cls)
        super().set_parent_class(cls)
