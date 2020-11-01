from django_object.datatypes import PaginatedList, resolve_filtering
from django_object.utils import determine_items, add_item, remove_item
from object.actions import Action
from object.datatypes import ObjectType, BooleanType


class ModelAction:
    @property
    def model(self):
        return self.parent_class.model

    def set_parent_class(self, cls):
        self.parent_class = cls

    def determine_parameters(self, **kwargs):
        self.parameters = determine_items(self.parent_class.in_fields, self.only_fields,
                                          self.exclude_fields, self.custom_fields)

    def determine_data(self, **kwargs):
        pass

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, return_value=None,
                 exec_fn=None, **kwargs):
        self.parent_class = None
        self._action = None
        self.only_fields = only_fields
        self.exclude_fields = exclude_fields
        self.custom_fields = custom_fields or {}
        self.kwargs = kwargs

        self.parameters = None
        self.data = None
        self.return_value = return_value
        self.exec_fn = exec_fn

    def to_action(self):
        if self._action is None:
            self.determine_parameters()
            self.determine_data()
            self._action = Action(parameters=self.parameters, data=self.data,
                                  return_value=self.return_value, exec_fn=self.exec_fn,
                                  mutation=self.kwargs.get("mutation", False))
        return self._action


class ObjectMixin:
    def determine_parameters(self, **kwargs):
        self.only_fields, self.exclude_fields = add_item(self.parent_class.pk_field_name,
                                                         self.only_fields,
                                                         self.exclude_fields)
        super().determine_parameters(**kwargs)


class InputDataMixin:
    def __init__(self, data_only_fields=None, data_exclude_fields=None, data_custom_fields=None,
                 force_nullable=False, **kwargs):
        self.force_nullable = force_nullable
        self.data_only_fields = data_only_fields
        self.data_exclude_fields = data_exclude_fields
        self.data_custom_fields = data_custom_fields
        super().__init__(**kwargs)

    def determine_data(self, **kwargs):
        if self.parent_class.auto_pk:
            self.data_only_fields, self.data_exclude_fields = remove_item(self.parent_class.pk_field_name,
                                                                          self.data_only_fields,
                                                                          self.data_exclude_fields)
        data = determine_items(self.parent_class.in_fields, self.data_only_fields,
                               self.data_exclude_fields, self.data_custom_fields)
        if self.force_nullable:
            for f in data.values():
                f.data = True
                f._nullable_if_input = True
        self.data = data


class FilterMixin:
    def determine_parameters(self, **kwargs):
        super().determine_parameters(**kwargs)
        self.parameters.update(self.parent_class.filters)

    def __init__(self, exec_fn, **kwargs):
        def filter_exec_fn(request, params, **kwargs):
            res = exec_fn(request, params, **kwargs)
            return resolve_filtering(request, res, params, **kwargs)
        exec_fn = filter_exec_fn
        super().__init__(exec_fn=exec_fn, **kwargs)


class DetailAction(ObjectMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.get(**params)
        return exec_fn

    def __init__(self, exec_fn=None, return_value=None, **kwargs):
        if exec_fn is None:
            exec_fn = self.get_exec_fn()
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(only_fields=(), exec_fn=exec_fn, return_value=return_value, **kwargs)


class ListAction(FilterMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.all()
        return exec_fn

    def __init__(self, exec_fn=None, return_value=None, **kwargs):
        if exec_fn is None:
            exec_fn = self.get_exec_fn()
        if return_value is None:
            return_value = PaginatedList("self")
        super().__init__(only_fields=(), exec_fn=exec_fn, return_value=return_value, **kwargs)


class CreateAction(InputDataMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.create(**params.get("data", {}))
        return exec_fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, exec_fn=None, permissions=None,
                 return_value=None, **kwargs):
        # todo move mutation=True somewhere else so that the generic action is not graphql-biased
        #  (probably upon importing GraphQLAdapter)
        if exec_fn is None:
            exec_fn = self.get_exec_fn()
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(data_only_fields=only_fields, data_exclude_fields=exclude_fields,
                         data_custom_fields=custom_fields, only_fields=(),
                         exec_fn=exec_fn, permissions=permissions, mutation=True, return_value=return_value, **kwargs)


class UpdateAction(InputDataMixin, ObjectMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            data = params.pop("data")
            obj = self.model.objects.get(**params)
            for k, v in data.items():
                setattr(obj, k, v)
            obj.save()
            return obj
        return exec_fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None,
                 exec_fn=None, permissions=None, return_value=None, **kwargs):
        if exec_fn is None:
            exec_fn = self.get_exec_fn()
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(data_only_fields=only_fields, data_exclude_fields=exclude_fields,
                         data_custom_fields=custom_fields, only_fields=(),
                         exec_fn=exec_fn, permissions=permissions, mutation=True, force_nullable=True,
                         return_value=return_value, **kwargs)


class DeleteAction(ObjectMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            self.model.objects.get(**params).delete()
            return True
        return exec_fn

    def __init__(self, exec_fn=None, return_value=None, **kwargs):
        if exec_fn is None:
            exec_fn = self.get_exec_fn()
        if return_value is None:
            return_value = BooleanType()
        super().__init__(only_fields=(), exec_fn=exec_fn, mutation=True,
                         return_value=return_value, **kwargs)
