from django.utils.decorators import classproperty


class ObjectMeta(type):
    classes = {}

    @staticmethod
    def store_class(module_name, class_name, cls):
        key = "{}.{}".format(module_name, class_name)
        ObjectMeta.classes[key] = cls

    @staticmethod
    def get_class(module_name, class_name):
        key = "{}.{}".format(module_name, class_name)
        assert key in ObjectMeta.classes, "Class does not exist: `{}.{}`".format(module_name, class_name)
        return ObjectMeta.classes[key]

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs)

        # store class stub
        ObjectMeta.store_class(cls.__module__, name, cls)

        for field in {**cls.fields, **cls.input_fields, **cls.output_fields}.values():
            field.set_parent_class(cls)

        for action in cls.actions.values():
            action.set_parent_class(cls)

        return cls


class Object(metaclass=ObjectMeta):
    fields = {}
    input_fields = {}
    output_fields = {}
    id_field = True

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

    actions = {}
