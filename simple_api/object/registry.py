from simple_api.constants import OBJECT_SELF_REFERENCE
from simple_api.utils import Storage


class ObjectStorage(Storage):
    @staticmethod
    def key_for_class(module_name, class_name):
        return "{}.{}".format(module_name, class_name)

    def store(self, module_name, class_name, cls):
        key = ObjectStorage.key_for_class(module_name, class_name)
        ObjectStorage.storage[key] = cls

    @staticmethod
    def class_exists(module_name, class_name):
        assert class_name != OBJECT_SELF_REFERENCE, \
            "`{}` is a reserved keyword and cannot be used as a class name.".format(OBJECT_SELF_REFERENCE)
        key = ObjectStorage.key_for_class(module_name, class_name)
        return key in ObjectStorage.storage

    def get(self, module_name, class_name):
        # if we get just the class name, we try to search for a class with such a name; in case there is a unique class
        # with that name, we use it, otherwise we ask for the module as well
        if module_name is None:
            candidate_classes = []
            for k in ObjectStorage.storage.keys():
                module, cls = k.rsplit(".", 1)
                if cls == class_name:
                    candidate_classes.append(ObjectStorage.key_for_class(module, cls))

            assert len(candidate_classes) < 2, "Ambiguous class name: `{}`. You need to specify the module as well. " \
                                               "The options are: {}".format(class_name, candidate_classes)
            key = candidate_classes[0] if candidate_classes else None
        else:
            key = ObjectStorage.key_for_class(module_name, class_name)
        assert key in ObjectStorage.storage, "Class does not exist: `{}.{}`".format(module_name, class_name)
        return ObjectStorage.storage[key]


object_storage = ObjectStorage()
