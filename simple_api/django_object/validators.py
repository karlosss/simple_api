from django.core.exceptions import ValidationError
from simple_api.object.validators import Validator


class DjangoValidator(Validator):
    def __init__(self, validation_fn):
        self.callable = validation_fn

    def validation_statement(self, request, value=None, **kwargs):
        try:
            self.callable(value)
            return True
        except ValidationError:
            return False

    def error_message(self, **kwargs):
        return "Django validator error"


class ForeignKeyValidator(Validator):
    def __init__(self, target_model):
        self.target_model = target_model

    def validation_statement(self, request, value=None, **kwargs):
        return self.target_model.objects.filter(pk=value).exists()

    def error_message(self, **kwargs):
        return "Error: Referenced object doesn't exist"
