from django.core.exceptions import ValidationError
from simple_api.object.validators import FieldValidator


class DjangoValidator(FieldValidator):
    def is_valid(self, value, **kwargs):
        try:
            return not self.fn(value, **kwargs)
        except ValidationError:
            return False


class DjangoFKValidator(FieldValidator):
    def is_valid(self, value, **kwargs):
        pass
