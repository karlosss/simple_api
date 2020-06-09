from inspect import isclass

from constants import OBJECT_SELF_REFERENCE
from object.object import ObjectMeta, Object


class Type:
    def __init__(self, nullable=False, default=None):
        self.parent_class = None
        self.nullable = nullable
        self.default = default

    def set_parent_class(self, cls):
        self.parent_class = cls

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
    def __init__(self, to, nullable=False, default=None):
        super().__init__(nullable=nullable, default=default)
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
    def __init__(self, of, nullable=False, default=None):
        super().__init__(nullable=nullable, default=default)
        self.of = of

    def set_parent_class(self, cls):
        self.of.set_parent_class(cls)
        super().set_parent_class(cls)
