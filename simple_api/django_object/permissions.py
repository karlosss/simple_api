from simple_api.object.permissions import BasePermission


def permission_class_with_get_fn(permission_class, get_fn):
    # takes a permission class and embeds the get_fn of the object into it; this is so that it can be passed around
    # as a class and there is no need to instantiate it (otherwise we would run into trying to instantiate something
    # that has already been instantiated)
    class _DjangoPermission:
        def has_permission(self, **kwargs):
            obj = kwargs.pop("obj")
            if obj is None:
                obj = get_fn(**kwargs)
            return permission_class().has_permission(obj=obj, **kwargs)

        def error_message(self, **kwargs):
            return permission_class().error_message(**kwargs)
    return _DjangoPermission


class DjangoPermission(BasePermission):
    def permission_statement(self, request, obj, **kwargs):
        raise NotImplementedError


class IsAuthenticated(DjangoPermission):
    def permission_statement(self, request, obj, **kwargs):
        return request and request.user and request.user.is_authenticated
