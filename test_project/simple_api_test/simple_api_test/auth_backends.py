from django.contrib.auth import get_user_model


class TestcaseUserBackend:
    def authenticate(self, request=None, user=None):
        return user

    def get_user(self, user_id):
        User = get_user_model()
        return User.objects.get(pk=user_id)
