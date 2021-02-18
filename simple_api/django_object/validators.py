from django.core.exceptions import ValidationError
from simple_api.object.validators import Validator


class DjangoValidator(Validator):
    def __init__(self, field_name, validation_fn):
        self.fn = validation_fn
        self.field_name = field_name

    def validation_statement(self, request, value=None, **kwargs):
        try:
            self.fn(value)
            return True
        except ValidationError:
            return False

    def error_message(self, **kwargs):
        return "Django validator failed in field {}".format(self.field_name)


class ForeignKeyValidator(Validator):
    def __init__(self, target_model):
        self.target_model = target_model

    def validation_statement(self, request, value=None, **kwargs):
        return self.target_model.objects.filter(id=value).exists()

    def error_message(self, **kwargs):
        return "Error: Referenced object doesn't exist"
