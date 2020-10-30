from adapters.graphql.utils import capitalize
from django_object.datatypes import PaginatedList, resolve_filtering
from django_object.utils import determine_items, add_item, remove_item
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

    def create_auxiliary_actions(self, default_validators, **kwargs):
        actions = kwargs.get("actions")
        if actions is not None:
            return actions
        actions = {}
        for field_name, validator in {**default_validators, **self.field_validators}.items():
            if field_name in self.parameters:
                name = "{}__{}".format(self.name, field_name)
                actions[name] = ListAction(exec_fn=validator.fn, permissions=self.permissions,
                                           return_value=validator.type, hidden=True)
                actions[name].set_name(name)
        return actions

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


class ObjectMixin:
    on_object = True

    def determine_parameters(self, **kwargs):
        self.only_fields, self.exclude_fields = add_item(self.parent_class.pk_field,
                                                         self.only_fields,
                                                         self.exclude_fields)
        super().determine_parameters(**kwargs)

    def create_auxiliary_actions(self, default_validators, **kwargs):
        actions = kwargs.get("actions") or super().create_auxiliary_actions(default_validators, **kwargs)
        for action in actions.values():
            action.parameters.update(
                {self.parent_class.pk_field: self.parent_class.in_fields[self.parent_class.pk_field]})
        return actions


class InputDataMixin:
    def __init__(self, data_only_fields=None, data_exclude_fields=None, data_custom_fields=None,
                 force_nullable=False, **kwargs):
        self.force_nullable = force_nullable
        self.data_only_fields = data_only_fields
        self.data_exclude_fields = data_exclude_fields
        self.data_custom_fields = data_custom_fields
        super().__init__(**kwargs)

    def determine_parameters(self, **kwargs):
        if self.parent_class.auto_pk:
            self.data_only_fields, self.data_exclude_fields = remove_item(self.parent_class.pk_field,
                                                                          self.data_only_fields,
                                                                          self.data_exclude_fields)
        fields = determine_items(self.parent_class.in_fields, self.data_only_fields,
                                 self.data_exclude_fields, self.data_custom_fields)
        if self.force_nullable:
            for f in fields.values():
                f._nullable = True
                f._nullable_if_input = True
        if fields:
            attrs = {"fields": fields, "hidden": True}
            input_cls = ObjectMeta(self.parent_class.__name__ + capitalize(self.name), (Object,), attrs)
            self.custom_fields["data"] = ObjectType(input_cls)
        super().determine_parameters(**kwargs)

    def create_auxiliary_actions(self, default_validators, **kwargs):
        actions = {}
        for field_name, validator in {**default_validators, **self.field_validators}.items():
            if field_name in self.custom_fields["data"].to.in_fields:
                name = "{}__{}".format(self.name, field_name)
                actions[name] = ListAction(exec_fn=validator.fn, permissions=self.permissions,
                                           return_value=validator.type, hidden=True)
                actions[name].set_name(name)
        return super().create_auxiliary_actions(default_validators, actions=actions)


class FilterMixin:
    def determine_parameters(self, **kwargs):
        super().determine_parameters(**kwargs)
        self.parameters.update(self.parent_class.filters)

    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            data = super().get_exec_fn()(request, params, **kwargs)
            return resolve_filtering(request, data, params)
        return exec_fn


class DetailAction(ObjectMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.get(**params)
        return exec_fn

    def __init__(self, exec_fn=None, permissions=None, return_value=ObjectType("self"), **kwargs):
        super().__init__(only_fields=(), exec_fn=exec_fn, permissions=permissions, return_value=return_value, **kwargs)


class ListAction(FilterMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.all()
        return exec_fn

    def __init__(self, exec_fn=None, permissions=None, return_value=PaginatedList("self"), **kwargs):
        super().__init__(only_fields=(), exec_fn=exec_fn, permissions=permissions, return_value=return_value, **kwargs)


class CreateAction(InputDataMixin, ModelAction):
    def get_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.create(**params.get("data", {}))
        return exec_fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, exec_fn=None, permissions=None,
                 return_value=ObjectType("self"), **kwargs):
        # todo move mutation=True somewhere else so that the generic action is not graphql-biased
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
                 exec_fn=None, permissions=None, return_value=ObjectType("self"), **kwargs):
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

    def __init__(self, exec_fn=None, permissions=None, return_value=BooleanType(), **kwargs):
        super().__init__(only_fields=(), exec_fn=exec_fn, permissions=permissions, mutation=True,
                         return_value=return_value, **kwargs)
