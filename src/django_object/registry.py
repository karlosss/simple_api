
from utils import Storage


class ModelDjangoObjectStorage(Storage):
    @staticmethod
    def same_class(a, b):
        return a.__module__ == b.__module__ and a.__name__ == b.__name__

    def get(self, model):
        assert model in self.storage, "Related class for model `{}` does not exist.".format(model)
        return self.storage[model]

    def store(self, model, cls):
        assert model not in self.storage or self.same_class(self.storage[model], cls), \
            "Multiple related classes for model `{}`: `{}` and `{}`.".format(model, self.storage[model],cls)
        self.storage[model] = cls


model_django_object_storage = ModelDjangoObjectStorage()
