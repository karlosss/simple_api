from object.permissions import BasePermission


class DjangoPermission(BasePermission):
    def __init__(self, get_fn=None, **kwargs):
        self.get_fn = get_fn
        super().__init__(**kwargs)

    def has_permission(self, exclude_classes=(), **kwargs):
        obj = kwargs.pop("obj")
        if obj is None:
            obj = self.get_fn(**kwargs)
        return super().has_permission(exclude_classes=(DjangoPermission,) + exclude_classes, obj=obj, **kwargs)

    def permission_statement(self, **kwargs):
        raise NotImplementedError


class IsAuthenticated(DjangoPermission):
    def permission_statement(self, request, **kwargs):
        return request and request.user and request.user.is_authenticated
