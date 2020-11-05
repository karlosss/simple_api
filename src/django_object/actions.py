from copy import deepcopy

from adapters.graphql.utils import capitalize
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
        self.parameters.update(determine_items(self.parent_class.in_fields, self.only_fields,
                                               self.exclude_fields, self.custom_fields))

    def determine_data(self, **kwargs):
        pass

    def determine_exec_fn(self, **kwargs):
        self.exec_fn = self.exec_fn or self.default_exec_fn()

    def default_exec_fn(self):
        raise NotImplemented

    def set_name(self, name):
        self.name = name

    def set_validators(self, validators):
        for field_name, validator in validators.items():
            if field_name not in self.validators:
                self.validators[field_name] = validator.fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, return_value=None,
                 exec_fn=None, validators=None, validate_fn=None, permissions=None, **kwargs):
        self.parent_class = None
        self._action = None
        self._aux_actions = {}
        self.name = None
        self.only_fields = only_fields
        self.exclude_fields = exclude_fields
        self.custom_fields = custom_fields or {}
        self.validators = validators or {}
        self.validate_fn = validate_fn
        self.permissions = permissions
        self.kwargs = kwargs

        self.hidden = kwargs.get("hidden", False)
        self.hide_if_denied = kwargs.get("hide_if_denied", False)
        self.retry_in = kwargs.get("retry_in")
        self.choice_map = []

        self.parameters = {}
        self.data = None
        self.return_value = return_value
        self.exec_fn = exec_fn

    def auxiliary_actions(self):
        if not self._aux_actions:
            self._aux_actions = {}
        return self._aux_actions

    def to_action(self):
        if self._action is None:
            self.determine_parameters()
            self.determine_data()
            self.determine_exec_fn()
            self._action = Action(parameters=self.parameters, data=self.data,
                                  return_value=self.return_value, exec_fn=self.exec_fn,
                                  validators=self.validators, validate_fn=self.validate_fn,
                                  permissions=self.permissions, with_object=getattr(self, "with_object", False),
                                  hidden=self.hidden, hide_if_denied=self.hide_if_denied, retry_in=self.retry_in,
                                  choice_map=self.choice_map, mutation=self.kwargs.get("mutation", False))
        return self._action


class ObjectMixin:
    with_object = True

    def determine_parameters(self, **kwargs):
        self.only_fields, self.exclude_fields = add_item(self.parent_class.pk_field_name,
                                                         self.only_fields,
                                                         self.exclude_fields)
        super().determine_parameters(**kwargs)

    def auxiliary_actions(self):
        actions = super().auxiliary_actions()
        for action in actions.values():
            pk_field_name = self.parent_class.pk_field_name
            action.custom_fields.update({pk_field_name: deepcopy(self.parent_class.in_fields[pk_field_name])})
        return actions


class InputDataMixin:
    def __init__(self, data_only_fields=None, data_exclude_fields=None, data_custom_fields=None,
                 force_nullable=False, **kwargs):
        self.force_nullable = force_nullable
        self.data_only_fields = data_only_fields
        self.data_exclude_fields = data_exclude_fields
        self.data_custom_fields = data_custom_fields
        super().__init__(**kwargs)

    def determine_data(self, **kwargs):
        if self.parent_class.auto_pk and self.parent_class.pk_field_name in self.parent_class.in_fields:
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

    def auxiliary_actions(self):
        actions = super().auxiliary_actions()
        for field_name, validator in self.parent_class.field_validators.items():
            action = ListAction(exec_fn=validator.fn, return_value=validator.field_type, permissions=self.permissions,
                                hidden=True)
            action.set_parent_class(self.parent_class)
            action.set_name("{}__{}".format(self.name, field_name))
            actions[field_name] = action
            self.choice_map.append({
                "parameter_name": field_name,
                "action_name": "{}{}".format(self.parent_class.__name__, capitalize(action.name)),
                "field_name": validator.field_name,
            })
        return actions


class FilterMixin:
    def determine_parameters(self, **kwargs):
        self.parameters.update({"filters": ObjectType(self.parent_class.filter_type, nullable=True)})
        super().determine_parameters(**kwargs)

    def determine_exec_fn(self):
        fn = self.exec_fn
        def filtering_exec_fn(request, params, **kwargs):
            res = fn(request, params, **kwargs)
            return resolve_filtering(request, res, params, **kwargs)
        self.exec_fn = filtering_exec_fn
        super().determine_exec_fn()


class DetailAction(ObjectMixin, ModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.get(**params)
        return exec_fn

    def __init__(self, exec_fn=None, return_value=None, **kwargs):
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(only_fields=(), exec_fn=exec_fn, return_value=return_value, **kwargs)


class ListAction(FilterMixin, ModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.all()
        return exec_fn

    def determine_exec_fn(self):
        # todo resolve code duplication with the base ModelAction class
        self.exec_fn = self.exec_fn or self.default_exec_fn()
        super().determine_exec_fn()

    def __init__(self, exec_fn=None, return_value=None, custom_fields=None, **kwargs):
        if return_value is None:
            return_value = PaginatedList("self")
        super().__init__(only_fields=(), exec_fn=exec_fn, return_value=return_value, custom_fields=custom_fields,
                         **kwargs)


class CreateAction(InputDataMixin, ModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.create(**params.get("data", {}))
        return exec_fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, exec_fn=None, permissions=None,
                 return_value=None, **kwargs):
        # todo move mutation=True somewhere else so that the generic action is not graphql-biased
        #  (probably upon importing GraphQLAdapter)
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(data_only_fields=only_fields, data_exclude_fields=exclude_fields,
                         data_custom_fields=custom_fields, only_fields=(),
                         exec_fn=exec_fn, permissions=permissions, mutation=True, return_value=return_value, **kwargs)


class UpdateAction(ObjectMixin, InputDataMixin, ModelAction):
    def default_exec_fn(self):
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
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(data_only_fields=only_fields, data_exclude_fields=exclude_fields,
                         data_custom_fields=custom_fields, only_fields=(),
                         exec_fn=exec_fn, permissions=permissions, mutation=True, force_nullable=True,
                         return_value=return_value, **kwargs)


class DeleteAction(ObjectMixin, ModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            self.model.objects.get(**params).delete()
            return True
        return exec_fn

    def __init__(self, exec_fn=None, return_value=None, **kwargs):
        if return_value is None:
            return_value = BooleanType()
        super().__init__(only_fields=(), exec_fn=exec_fn, mutation=True,
                         return_value=return_value, **kwargs)
