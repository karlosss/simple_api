class ObjectMetaStorage:
    classes = {}

    @staticmethod
    def key_for_class(module_name, class_name):
        return "{}.{}".format(module_name, class_name)

    @staticmethod
    def store_class(module_name, class_name, cls):
        key = ObjectMetaStorage.key_for_class(module_name, class_name)
        ObjectMetaStorage.classes[key] = cls

    @staticmethod
    def class_exists(module_name, class_name):
        key = ObjectMetaStorage.key_for_class(module_name, class_name)
        return key in ObjectMetaStorage.classes

    @staticmethod
    def get_class(module_name, class_name):
        key = ObjectMetaStorage.key_for_class(module_name, class_name)
        assert key in ObjectMetaStorage.classes, "Class does not exist: `{}.{}`".format(module_name, class_name)
        return ObjectMetaStorage.classes[key]


object_meta_storage = ObjectMetaStorage()
