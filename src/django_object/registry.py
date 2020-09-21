class DjangoObjectMetaStorage:
    classes_for_related = {}

    @staticmethod
    def store_class(model, cls):
        DjangoObjectMetaStorage.classes_for_related[model] = cls

    @staticmethod
    def get_class(model):
        assert model in DjangoObjectMetaStorage.classes_for_related, \
            "Related class of model `{}` does not exist.".format(model)
        return DjangoObjectMetaStorage.classes_for_related[model]


django_object_meta_storage = DjangoObjectMetaStorage()
