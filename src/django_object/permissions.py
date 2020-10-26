from object.permissions import BasePermission


class DjangoPermission(BasePermission):
    def __init__(self, request=None, obj=None, qs=None, **kwargs):
        super().__init__(request=request, obj=obj, qs=qs, **kwargs)
        self.request = request
        self.obj = obj
        self.qs = qs

    def has_permission(self, exclude_classes=()):
        return super().has_permission(exclude_classes=(DjangoPermission,) + exclude_classes)

    def permission_statement(self):
        raise NotImplementedError


class IsAuthenticated(DjangoPermission):
    def permission_statement(self):
        return self.request and self.request.user and self.request.user.is_authenticated
