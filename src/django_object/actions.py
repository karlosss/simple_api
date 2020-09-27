from django_object.converter import filter_simple_api_fields_from_model
from django_object.datatypes import PaginatedList
from django_object.paginated_list import resolve_filtering, build_parameters_for_paginated_list
from object.actions import Action
from object.datatypes import ObjectType, PlainListType, StringType
from object.function import Function
from utils import AttrDict


class ModelAction(Action):
    @property
    def model(self):
        return self.parent_class.model

    def determine_parameters(self):
        self.parameters = filter_simple_api_fields_from_model(self.model, self.only_fields, self.exclude_fields)

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

    def __init__(self, only_fields=("id",), exclude_fields=None, exec_fn=None,
                 **kwargs):
        assert "return_value" not in kwargs, "`return_value` cannot be set for `DetailAction`."
        super().__init__(only_fields, exclude_fields, exec_fn, **kwargs)
        self.return_value = ObjectType("self")


class ListAction(DefaultModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params):
            return resolve_filtering(request, self.model.objects, params)
        return Function(exec_fn)

    def determine_parameters(self):
        super().determine_parameters()
        self.parameters.update(build_parameters_for_paginated_list(self.parent_class.filters))

    def __init__(self, exec_fn=None, **kwargs):
        assert "return_value" not in kwargs, "`return_value` cannot be set for `DetailAction`."
        assert "only_fields" not in kwargs, "`only_fields` cannot be set for `ListAction`."
        assert "exclude_fields" not in kwargs, "`exclude_fields` cannot be set for `ListAction`."
        super().__init__(only_fields=(), exec_fn=exec_fn, **kwargs)

        # filters need to be added in determine_parameters, as the knowledge of the parent class is essential
        self.return_value = PaginatedList("self")
