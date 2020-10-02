from adapters.graphql.utils import capitalize
from django_object.converter import filter_simple_api_fields_from_model
from django_object.datatypes import PaginatedList, resolve_filtering, build_parameters_for_paginated_list
from object.actions import Action
from object.datatypes import ObjectType, BooleanType
from object.function import Function
from object.object import ObjectMeta, Object


class ModelAction(Action):
    @property
    def model(self):
        return self.parent_class.model

    def determine_parameters(self, **kwargs):
        self.parameters = filter_simple_api_fields_from_model(self.model, self.only_fields,
                                                              self.exclude_fields, input=True)

    def __init__(self, only_fields=None, exclude_fields=None, exec_fn=None, **kwargs):
        super().__init__(exec_fn, **kwargs)
        self.only_fields = only_fields
        self.exclude_fields = exclude_fields


class DefaultModelAction(ModelAction):
    def default_exec_fn(self):
        raise NotImplementedError

    def get_exec_fn(self):
        if self.exec_fn is not None:
            return self.exec_fn
        return self.default_exec_fn()


class DetailAction(DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            return self.model.objects.get(**params)
        return Function(exec_fn)

    def __init__(self, lookup_fields=("id",), exec_fn=None, **kwargs):
        super().__init__(only_fields=lookup_fields, exec_fn=exec_fn, **kwargs)
        self.return_value = ObjectType("self")


class ListAction(DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            return resolve_filtering(request, self.model.objects, params)
        return Function(exec_fn)

    def determine_parameters(self, **kwargs):
        # filters need to be added here, as the knowledge of the parent class is essential
        super().determine_parameters()
        self.parameters.update(build_parameters_for_paginated_list(self.parent_class.filters))

    def __init__(self, exec_fn=None, **kwargs):
        super().__init__(only_fields=(), exec_fn=exec_fn, **kwargs)
        self.return_value = PaginatedList("self")


class InputDataMixin:
    def determine_parameters(self, **kwargs):
        attrs = {
            "fields": filter_simple_api_fields_from_model(self.model, self.only_fields,
                                                          self.exclude_fields, input=True,
                                                          nullable=kwargs.get("nullable", False))
        }
        input_cls = ObjectMeta(self.parent_class.__name__ + capitalize(self.name), (Object,), attrs)
        self.parameters = {"data": ObjectType(input_cls)}


class CreateAction(InputDataMixin, DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            return self.model.objects.create(**params["data"])
        return Function(exec_fn)

    def __init__(self, only_fields=None, exclude_fields=("id",), exec_fn=None,
                 **kwargs):
        # todo move mutation=True somewhere else so that the generic action is not graphql-biased
        super().__init__(only_fields, exclude_fields, exec_fn, mutation=True, **kwargs)
        self.return_value = ObjectType("self")


class UpdateAction(InputDataMixin, DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            data = params.pop("data")
            obj = self.model.objects.get(**params)
            for k, v in data.items():
                setattr(obj, k, v)
            obj.save()
            return obj
        return Function(exec_fn)

    def determine_parameters(self, **kwargs):
        super().determine_parameters(nullable=True, **kwargs)
        self.parameters.update(filter_simple_api_fields_from_model(self.model, self.lookup_fields, None, input=True))

    def __init__(self, lookup_fields=("id",), only_fields=None, exclude_fields=("id",), exec_fn=None,
                 **kwargs):
        super().__init__(only_fields, exclude_fields, exec_fn, mutation=True, **kwargs)
        self.lookup_fields = lookup_fields
        self.return_value = ObjectType("self")


class DeleteAction(DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            self.model.objects.get(**params).delete()
            return True
        return Function(exec_fn)

    def __init__(self, lookup_fields=("id",), exec_fn=None, **kwargs):
        super().__init__(only_fields=lookup_fields, exec_fn=exec_fn, mutation=True, **kwargs)
        self.return_value = BooleanType()
