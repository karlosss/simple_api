from utils import Storage


class ObjectStorage(Storage):
    @staticmethod
    def key_for_class(module_name, class_name):
        return "{}.{}".format(module_name, class_name)

    def store(self, module_name, class_name, cls):
        key = ObjectStorage.key_for_class(module_name, class_name)
        ObjectStorage.storage[key] = cls

    @staticmethod
    def class_exists(module_name, class_name):
        key = ObjectStorage.key_for_class(module_name, class_name)
        return key in ObjectStorage.storage

    def get(self, module_name, class_name):
        key = ObjectStorage.key_for_class(module_name, class_name)
        assert key in ObjectStorage.storage, "Class does not exist: `{}.{}`".format(module_name, class_name)
        return ObjectStorage.storage[key]


object_storage = ObjectStorage()
