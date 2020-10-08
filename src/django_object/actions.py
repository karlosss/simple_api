from adapters.graphql.utils import capitalize
from django_object.datatypes import PaginatedList, resolve_filtering
from django_object.utils import determine_items
from object.actions import Action
from object.datatypes import ObjectType, BooleanType
from object.object import ObjectMeta, Object


class ModelAction(Action):
    @property
    def model(self):
        return self.parent_class.model

    def determine_parameters(self, **kwargs):
        self.parameters = determine_items(self.parent_class.in_fields, self.only_fields,
                                          self.exclude_fields, self.custom_fields)

    def get_exec_fn(self):
        raise NotImplementedError

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, return_value=None,
                 exec_fn=None, permissions=None, **kwargs):
        super().__init__(return_value=return_value, exec_fn=exec_fn, permissions=permissions, **kwargs)
        self.only_fields = only_fields
        self.exclude_fields = exclude_fields
        self.custom_fields = custom_fields or {}

    def convert(self, adapter, **kwargs):
        if self.fn.main_hook is None:
            self.fn.set_main_hook(self.get_exec_fn())
        return super().convert(adapter, **kwargs)


class DetailAction(ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.get(**params)
        return exec_fn

    def __init__(self, lookup_fields=("id",), exec_fn=None, permissions=None, **kwargs):
        super().__init__(only_fields=lookup_fields, exec_fn=exec_fn, permissions=permissions, **kwargs)
        self.return_value = ObjectType("self")


class ListAction(ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return resolve_filtering(request, self.model.objects, params)
        return exec_fn

    def determine_parameters(self, **kwargs):
        # filters need to be added here, as the knowledge of the parent class is essential
        super().determine_parameters()
        self.parameters.update(self.parent_class.filters)

    def __init__(self, exec_fn=None, permissions=None, **kwargs):
        super().__init__(only_fields=(), exec_fn=exec_fn, permissions=permissions, **kwargs)
        self.return_value = PaginatedList("self")


class InputDataMixin:
    def determine_parameters(self, **kwargs):
        fields = determine_items(self.parent_class.in_fields, self.only_fields, self.exclude_fields, self.custom_fields)
        if kwargs.get("force_nullable", False):
            for f in fields.values():
                f._nullable = True
                f._nullable_if_input = True

        if not fields:
            self.parameters = {}
        else:
            attrs = {"fields": fields}
            input_cls = ObjectMeta(self.parent_class.__name__ + capitalize(self.name), (Object,), attrs)
            self.parameters = {"data": ObjectType(input_cls)}


class CreateAction(InputDataMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.create(**params.get("data", {}))
        return exec_fn

    def __init__(self, only_fields=None, exclude_fields=("id",), custom_fields=None, exec_fn=None, permissions=None,
                 **kwargs):
        # todo move mutation=True somewhere else so that the generic action is not graphql-biased
        super().__init__(only_fields=only_fields, exclude_fields=exclude_fields, custom_fields=custom_fields,
                         exec_fn=exec_fn, permissions=permissions, mutation=True, **kwargs)
        self.return_value = ObjectType("self")


class UpdateAction(InputDataMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            data = params.pop("data")
            obj = self.model.objects.get(**params)
            for k, v in data.items():
                setattr(obj, k, v)
            obj.save()
            return obj
        return exec_fn

    def determine_parameters(self, **kwargs):
        super().determine_parameters(force_nullable=True, **kwargs)
        self.parameters.update(determine_items(self.parent_class.in_fields, self.lookup_fields, None, None))

    def __init__(self, lookup_fields=("id",), only_fields=None, exclude_fields=("id",), custom_fields=None,
                 exec_fn=None, permissions=None, **kwargs):
        super().__init__(only_fields=only_fields, exclude_fields=exclude_fields, custom_fields=custom_fields,
                         exec_fn=exec_fn, permissions=permissions, mutation=True, **kwargs)
        self.lookup_fields = lookup_fields
        self.return_value = ObjectType("self")


class DeleteAction(ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            self.model.objects.get(**params).delete()
            return True
        return exec_fn

    def __init__(self, lookup_fields=("id",), exec_fn=None, permissions=None, **kwargs):
        super().__init__(only_fields=lookup_fields, exec_fn=exec_fn, permissions=permissions, mutation=True, **kwargs)
        self.return_value = BooleanType()
