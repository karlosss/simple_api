from simple_api.django_object.converter import get_simple_api_pk_field
from simple_api.django_object.datatypes import PaginatedList, resolve_filtering
from simple_api.django_object.utils import determine_items, remove_item
from simple_api.object.actions import Action, ToActionMixin, SetReferencesMixin
from simple_api.object.datatypes import ObjectType, BooleanType
from .permissions import permission_class_with_get_fn
from ..utils import ensure_tuple


class WithObjectMixin:
    def __init__(self, **kwargs):
        super().__init__(with_object=True, **kwargs)


# basically a copy of object.actions.Action, except it implements composition and thus translates itself into
# object.actions.Action using the ToActionMixin; this is important so that this one can be overridden/extended
# to support more specific model actions, but from the user point of view, these two should be equivalent
class ModelAction(SetReferencesMixin, ToActionMixin):
    @property
    def model(self):
        return self.parent_class.model

    def __init__(self, parameters=None, data=None, return_value=None, exec_fn=None, permissions=None, **kwargs):
        self.parameters = parameters or {}
        self.data = data or {}
        self.return_value = return_value or ObjectType("self")
        self.exec_fn = exec_fn
        self.permissions = ensure_tuple(permissions)
        self.kwargs = kwargs

        # these attributes exist to ensure that 1) the input from the user is stored unmodified in the attributes above
        # and 2) everything is determined just once (better performance, less error-prone)
        self._determined_exec_fn = None
        self._determined_parameters = None
        self._determined_permissions = None
        self._determined_data = None

        self._action = None
        super().__init__()

    # a hook for getting user-defined exec_fn, meant to override later with a default
    def get_exec_fn(self):
        return self.exec_fn

    def determine_exec_fn(self):
        if self._determined_exec_fn is None:
            self._determined_exec_fn = self.get_exec_fn()

    def determine_data(self):
        if self._determined_data is None:
            self._determined_data = self.data

    def determine_permissions(self):
        if self._determined_permissions is None:
            self._determined_permissions = self.permissions

    def determine_parameters(self):
        if self._determined_parameters is None:
            self._determined_parameters = self.parameters

    def to_action(self):
        if self._action is None:
            self.determine_exec_fn()
            self.determine_permissions()
            self.determine_parameters()
            self.determine_data()
            self._action = Action(parameters=self._determined_parameters, data=self._determined_data,
                                  return_value=self.return_value, exec_fn=self._determined_exec_fn,
                                  permissions=self._determined_permissions, **self.kwargs)
        return self._action


# implemented as composition because the parameters are not known at compile time - first, the model reference
# must be injected to determine the name and type of the pk field
#
# after all references are injected, the action determines the final set of parameters, permissions, get_fn and exec_fn
# and builds an action, which is then passed to lower layers for further processing
class ModelObjectAction(WithObjectMixin, ModelAction):
    def __init__(self, parameters=None, data=None, return_value=None, get_fn=None, exec_fn=None,
                 permissions=None, **kwargs):
        return_value = return_value or ObjectType("self")
        super().__init__(parameters=parameters, data=data, return_value=return_value, exec_fn=exec_fn,
                         permissions=permissions, **kwargs)
        self.get_fn = get_fn
        self._determined_get_fn = None

    def default_get_fn(self):
        def get_fn(request, params, **kwargs):
            pk = params.get(self.parent_class.pk_field_name)
            return self.model.objects.get(pk=pk)
        return get_fn

    # a hook for getting user-defined get_fn, or the default if not provided
    def get_get_fn(self):
        return self.get_fn or self.default_get_fn()

    def determine_get_fn(self):
        if self._determined_get_fn is None:
            self._determined_get_fn = self.get_get_fn()

    def determine_exec_fn(self):
        if self._determined_exec_fn is None:
            self.determine_get_fn()
            get_fn = self._determined_get_fn
            exec_fn = self.get_exec_fn()

            def fn(request, params, obj, **kwargs):
                obj = obj or get_fn(request, params, **kwargs)
                return exec_fn(request, params, obj=obj, **kwargs)

            self._determined_exec_fn = fn

    # injects get_fn into the permission classes so that this information can be used to determine permissions
    def determine_permissions(self):
        if self._determined_permissions is None:
            self._determined_permissions = []
            self.determine_get_fn()
            for pc in self.permissions:
                # here we extract the information from a permission class and use it to build a new class with the
                # function to get the related object embedded; this is because permissions are supposed to be classes
                # and not their instances and since django actions are implemented as composition with respect to
                # actions, there would be a problem with actions seeing instantiated permission classes, which would
                # create problems later
                self._determined_permissions.append(permission_class_with_get_fn(pc, self._determined_get_fn))

    def determine_parameters(self):
        if self._determined_parameters is None:
            self._determined_parameters = get_simple_api_pk_field(self.model)
            self._determined_parameters.update(self.parameters)


class DefaultExecFnMixin:
    def default_exec_fn(self):
        raise NotImplementedError

    def get_exec_fn(self):
        return self.exec_fn or self.default_exec_fn()


class DetailAction(DefaultExecFnMixin, ModelObjectAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            return obj
        return fn


class InputDataMixin:
    def __init__(self, only_fields=None, exclude_fields=None, custom_fields=None,
                 force_nullable=False, required_fields=(), **kwargs):
        self.force_nullable = force_nullable
        self.only_fields = only_fields
        self.exclude_fields = exclude_fields
        self.custom_fields = custom_fields
        self.required_fields = required_fields  # fields that are not nullable even when force_nullable=True
        super().__init__(**kwargs)

    def determine_data(self, **kwargs):
        if self._determined_data is None:
            only_fields = self.only_fields
            exclude_fields = self.exclude_fields

            # if the primary key is automatic, ensure it is not present in the data fields
            if self.parent_class.auto_pk and self.parent_class.pk_field_name in self.parent_class.in_fields:
                only_fields, exclude_fields = remove_item(self.parent_class.pk_field_name, only_fields, exclude_fields)

            data = determine_items(self.parent_class.in_fields, only_fields, exclude_fields, {})

            # if the fields should be nullable by default, ensure they are
            if self.force_nullable:
                for name, field in data.items():
                    if name not in self.required_fields:
                        field._nullable_if_input = True

            # apply custom fields as-is, without forcibly nullifying them
            data.update(self.custom_fields or {})

            self._determined_data = data


# TODO make this non graphql-biased (probably do some magic upon importing graphql adapter)
class MutationMixin:
    def __init__(self, **kwargs):
        super().__init__(mutation=True, **kwargs)


class UpdateAction(DefaultExecFnMixin, InputDataMixin, MutationMixin, ModelObjectAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            data = params.pop("data")
            for k, v in data.items():
                setattr(obj, k, v)
            obj.save()
            return obj
        return fn

    def __init__(self, custom_parameters=None, only_fields=None, exclude_fields=None, custom_fields=None,
                 return_value=None, get_fn=None, exec_fn=None, permissions=None, **kwargs):
        super().__init__(only_fields=only_fields, exclude_fields=exclude_fields, custom_fields=custom_fields,
                         return_value=return_value, custom_parameters=custom_parameters, get_fn=get_fn, exec_fn=exec_fn,
                         permissions=permissions, force_nullable=True, **kwargs)


class DeleteAction(DefaultExecFnMixin, MutationMixin, ModelObjectAction):
    def default_exec_fn(self):
        def fn(request, params, obj, **kwargs):
            obj.delete()
            return True
        return fn

    def __init__(self, custom_parameters=None, data=None, return_value=None, get_fn=None, exec_fn=None,
                 permissions=None, **kwargs):
        return_value = return_value or BooleanType()
        super().__init__(custom_parameters=custom_parameters, data=data, return_value=return_value, get_fn=get_fn,
                         exec_fn=exec_fn, permissions=permissions, **kwargs)


class CreateAction(DefaultExecFnMixin, InputDataMixin, MutationMixin, ModelAction):
    def default_exec_fn(self):
        def fn(request, params, **kwargs):
            return self.model.objects.create(**params.get("data", {}))
        return fn

    def __init__(self, parameters=None, only_fields=None, exclude_fields=None, custom_fields=None,
                 exec_fn=None, permissions=None, return_value=None, **kwargs):
        super().__init__(only_fields=only_fields, exclude_fields=exclude_fields, custom_fields=custom_fields,
                         exec_fn=exec_fn, permissions=permissions, return_value=return_value,
                         parameters=parameters, **kwargs)


class ListAction(DefaultExecFnMixin, ModelAction):
    def default_exec_fn(self):
        def exec_fn(request, params, **kwargs):
            return self.model.objects.all()
        return exec_fn

    def determine_parameters(self):
        if self._determined_parameters is None:
            self._determined_parameters = ({"filters": ObjectType(self.parent_class.filter_type, nullable=True)})
            self._determined_parameters.update(self.parameters)

    def determine_exec_fn(self):
        if self._determined_exec_fn is None:
            exec_fn = self.get_exec_fn()

            def fn(request, params, **kwargs):
                res = exec_fn(request, params, **kwargs)
                return resolve_filtering(request, res, params, **kwargs)

            self._determined_exec_fn = fn

    def __init__(self, parameters=None, exec_fn=None, permissions=None, return_value=None, **kwargs):
        return_value = return_value or PaginatedList("self")
        super().__init__(parameters=parameters, exec_fn=exec_fn, permissions=permissions, return_value=return_value,
                         **kwargs)
