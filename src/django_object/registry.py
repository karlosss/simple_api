class DjangoObjectMetaStorage:
    classes_for_related = {}

    @staticmethod
    def same_class(a, b):
        return a.__module__ == b.__module__ and a.__name__ == b.__name__

    @staticmethod
    def store_class(model, cls):
        assert model not in DjangoObjectMetaStorage.classes_for_related or DjangoObjectMetaStorage.same_class(DjangoObjectMetaStorage.classes_for_related[model], cls), \
            "Multiple related classes for model `{}`: `{}` and `{}`.".format(model, DjangoObjectMetaStorage.classes_for_related[model], cls)
        DjangoObjectMetaStorage.classes_for_related[model] = cls

    @staticmethod
    def get_class(model):
        assert model in DjangoObjectMetaStorage.classes_for_related, \
            "Related class for model `{}` does not exist.".format(model)
        return DjangoObjectMetaStorage.classes_for_related[model]


django_object_meta_storage = DjangoObjectMetaStorage()
