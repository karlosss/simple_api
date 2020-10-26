from django_object.permissions import IsAuthenticated


class IsAdmin(IsAuthenticated):
    def permission_statement(self):
        return self.request.user.is_staff or self.request.user.is_superuser
