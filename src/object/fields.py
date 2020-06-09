from inspect import isclass

from object.object import ObjectMeta, Object


class Field:
    def __init__(self, nullable=False, default=None):
        self.parent_class = None
        self.nullable = nullable
        self.default = default

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def set_parent_class(self, cls):
        self.parent_class = cls

    def convert(self, adapter, **kwargs):
        return adapter.convert_field(self, **kwargs)


class PrimitiveField(Field):
    def __str__(self):
        return super().__str__() + " nullable={}".format(self.nullable)


class IntegerField(PrimitiveField):
    pass


class FloatField(PrimitiveField):
    pass


class StringField(PrimitiveField):
    pass


class BooleanField(PrimitiveField):
    pass


class ObjectField(Field):
    def __init__(self, to, nullable=False, default=None):
        super().__init__(nullable=nullable, default=default)
        self.to = to

    def set_ref(self):
        if isclass(self.to) and issubclass(self.to, Object):
            pass
        elif self.to == "self":
            self.to = self.parent_class
        elif "." not in self.to:
            self.to = ObjectMeta.get_class(self.parent_class.__module__, self.to)
        else:
            self.to = ObjectMeta.get_class(*self.to.rsplit(".", 1))

    def __str__(self):
        return super().__str__() + " to " + str(self.to.model)

    def convert(self, adapter, **kwargs):
        self.set_ref()
        return super().convert(adapter, **kwargs)


class ListField(Field):
    def __init__(self, of, nullable=False, default=None):
        super().__init__(nullable=nullable, default=default)
        self.of = of

    def __str__(self):
        return super().__str__() + " of " + str(self.of.model)
