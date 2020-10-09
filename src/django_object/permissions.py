from object.permissions import BasePermission


class DjangoPermission(BasePermission):
    def __init__(self, request=None, obj=None, qs=None):
        super().__init__(request=request, obj=obj, qs=qs)
        self.request = request
        self.obj = obj
        self.qs = qs

    def permission_statement(self):
        raise NotImplementedError


class IsAuthenticated(DjangoPermission):
    def permission_statement(self):
        return self.request and self.request.user and self.request.user.is_authenticated
