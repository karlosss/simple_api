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

        for field in cls.fields.values():
            field.set_parent_class(cls)

        for action in cls.actions.values():
            action.set_parent_class(cls)

        return cls


class Object(metaclass=ObjectMeta):
    fields = {}
    id_field = True

    actions = {}
