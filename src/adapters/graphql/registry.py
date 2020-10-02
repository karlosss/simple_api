import graphene

from adapters.graphql.constants import INPUT_CLASS_SUFFIX
from utils import ClassStub, Storage


class InputClassStorage(Storage):
    def get(self, cls_str, cls):
        if cls_str not in self.storage:
            self.storage[cls_str] = ClassStub("{}{}".format(cls.__name__, INPUT_CLASS_SUFFIX),
                                              (graphene.InputObjectType,)).build()
        return self.storage[cls_str]

    def store(self, *args, **kwargs):
        raise NotImplementedError


class OutputClassStorage(Storage):
    def get(self, cls_str, cls):
        if cls_str not in self.storage:
            self.storage[cls_str] = ClassStub(cls.__name__, (graphene.ObjectType,)).build()
        return self.storage[cls_str]

    def store(self, *args, **kwargs):
        raise NotImplementedError


input_class_storage = InputClassStorage()
output_class_storage = OutputClassStorage()


def get_class(cls, input=False):
    assert not cls.__name__.endswith(INPUT_CLASS_SUFFIX), \
        "`{}`: An object name cannot end with `{}`.".format(cls.__name__, INPUT_CLASS_SUFFIX)

    cls_str = "{}.{}".format(cls.__module__, cls.__name__)

    if input:
        return input_class_storage.get(cls_str, cls)
    else:
        return output_class_storage.get(cls_str, cls)


def check_classes_for_fields():
    for name, cls in input_class_storage.storage.items():
        assert cls._meta.fields, "Object `{}` is used as input, but does not contain any input fields.".format(name)

    for name, cls in output_class_storage.storage.items():
        assert cls._meta.fields, "Object `{}` is used as output, but does not contain any output fields.".format(name)
