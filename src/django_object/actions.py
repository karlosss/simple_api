from django_object.datatypes import PaginatedList, resolve_filtering
from django_object.utils import determine_items, add_item, remove_item
from object.actions import Action
from object.datatypes import ObjectType, BooleanType


class WithObjectMixin:
    with_object = True

    def determine_parameters(self):
        self.only_fields, self.exclude_fields = add_item(self.parent_class.pk_field_name,
                                                         self.only_fields,
                                                         self.exclude_fields)
        super().determine_parameters()

    def determine_exec_fn(self):
        self.determine_get_fn()
        super().determine_exec_fn()
        get_fn = self.get_fn
        exec_fn = self.exec_fn

        def fn(request, params, obj, **kwargs):
            obj = obj or get_fn(request, params, **kwargs)
            return exec_fn(request, params, obj=obj, **kwargs)

        self.exec_fn = fn

    def default_get_fn(self):
        def get_fn(request, params, **kwargs):
            pk = params.get(self.parent_class.pk_field_name)
            return self.model.objects.get(pk=pk)

        return get_fn

    def determine_get_fn(self):
        self.get_fn = self.get_fn or self.default_get_fn()

    def instantiate_permissions(self):
        if self.permissions is None:
            return
        if not isinstance(self.permissions, (list, tuple)):
            self.permissions = self.permissions,

        instantiated_permissions = []
        for pc in self.permissions:
            instantiated_permissions.append(pc(get_fn=self.determine_get_fn()))
        self.permissions = instantiated_permissions

    def __init__(self, get_fn=None, **kwargs):
        self.get_fn = get_fn
        super().__init__(**kwargs)


class ModelAction:
    with_object = False

    @property
    def model(self):
        return self.parent_class.model

    def set_parent_class(self, cls):
        self.parent_class = cls

    def determine_parameters(self):
        self.parameters.update(determine_items(self.parent_class.in_fields, self.only_fields,
                                               self.exclude_fields, self.custom_fields))

    def determine_data(self, **kwargs):
        pass

    def determine_exec_fn(self):
        self.exec_fn = self.exec_fn or self.default_exec_fn()

    def default_exec_fn(self):
        raise NotImplementedError

    def set_name(self, name):
        self.name = name

    def instantiate_permissions(self):
        pass

    def set_validators(self, validators):
        for field_name, validator in validators.items():
            if field_name not in self.validators:
                self.validators[field_name] = validator.fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None, return_value=None,
                 exec_fn=None, validators=None, validate_fn=None, permissions=None, hidden=False, hide_if_denied=False,
                 retry_in=None, **kwargs):
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

        self.hidden = hidden
        self.hide_if_denied = hide_if_denied
        self.retry_in = retry_in

        self.parameters = {}
        self.data = None
        self.return_value = return_value
        self.exec_fn = exec_fn

    def to_action(self):
        if self._action is None:
            self.determine_parameters()
            self.determine_data()
            self.determine_exec_fn()
            self.instantiate_permissions()
            self._action = Action(parameters=self.parameters, data=self.data,
                                  return_value=self.return_value, exec_fn=self.exec_fn,
                                  validators=self.validators, validate_fn=self.validate_fn,
                                  permissions=self.permissions, with_object=self.with_object,
                                  hidden=self.hidden, hide_if_denied=self.hide_if_denied, retry_in=self.retry_in,
                                  mutation=self.kwargs.get("mutation", False))
        return self._action


class InputDataMixin:
    def __init__(self, data_only_fields=None, data_exclude_fields=None, data_custom_fields=None,
                 force_nullable=False, required_fields=(), **kwargs):
        self.force_nullable = force_nullable
        self.data_only_fields = data_only_fields
        self.data_exclude_fields = data_exclude_fields
        self.data_custom_fields = data_custom_fields
        self.required_fields = required_fields
        super().__init__(**kwargs)

    def determine_data(self, **kwargs):
        if self.parent_class.auto_pk and self.parent_class.pk_field_name in self.parent_class.in_fields:
            self.data_only_fields, self.data_exclude_fields = remove_item(self.parent_class.pk_field_name,
                                                                          self.data_only_fields,
                                                                          self.data_exclude_fields)

        data = determine_items(self.parent_class.in_fields, self.data_only_fields,
                               self.data_exclude_fields, self.data_custom_fields)
        if self.force_nullable:
            for name, field in data.items():
                if name not in self.required_fields:
                    field._nullable_if_input = True
        self.data = data


class DetailAction(WithObjectMixin, ModelAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            return obj
        return fn

    def __init__(self, get_fn=None, exec_fn=None, return_value=None, **kwargs):
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(only_fields=(), get_fn=get_fn, exec_fn=exec_fn, return_value=return_value, **kwargs)


class ListAction(ModelAction):
    def determine_parameters(self):
        self.parameters.update({"filters": ObjectType(self.parent_class.filter_type, nullable=True)})
        super().determine_parameters()

    def determine_exec_fn(self):
        super().determine_exec_fn()
        fn = self.exec_fn
        def filtering_exec_fn(request, params, **kwargs):
            res = fn(request, params, **kwargs)
            return resolve_filtering(request, res, params, **kwargs)
        self.exec_fn = filtering_exec_fn
        super().determine_exec_fn()

    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.all()
        return exec_fn

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


class UpdateAction(WithObjectMixin, InputDataMixin, ModelAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            data = params.pop("data")
            for k, v in data.items():
                setattr(obj, k, v)
            obj.save()
            return obj
        return fn

    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None,
                 get_fn=None, exec_fn=None, permissions=None, return_value=None, required_fields=(), **kwargs):
        if return_value is None:
            return_value = ObjectType("self")
        super().__init__(data_only_fields=only_fields, data_exclude_fields=exclude_fields,
                         data_custom_fields=custom_fields, only_fields=(),
                         get_fn=get_fn, exec_fn=exec_fn, permissions=permissions,
                         mutation=True, force_nullable=True, required_fields=required_fields,
                         return_value=return_value, **kwargs)


class DeleteAction(WithObjectMixin, ModelAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            obj.delete()
            return True
        return fn

    def __init__(self, get_fn=None, exec_fn=None, return_value=None, **kwargs):
        if return_value is None:
            return_value = BooleanType()
        super().__init__(only_fields=(), get_fn=get_fn, exec_fn=exec_fn, mutation=True,
                         return_value=return_value, **kwargs)


class ListObjectAction(WithObjectMixin, ListAction):
    pass


class CreateObjectAction(WithObjectMixin, CreateAction):
    pass
