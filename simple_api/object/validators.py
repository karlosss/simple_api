from inspect import isclass


def build_validation_fn(validators):
    if validators is None:
        return None

    if not isinstance(validators, (list, tuple)):
        validators = validators,

    instantiated_validators = []
    for cls_or_inst in validators:
        if isclass(cls_or_inst):
            instantiated_validators.append(cls_or_inst())
        else:
            instantiated_validators.append(cls_or_inst)

    def fn(**kwargs):
        for valid in instantiated_validators:
            if not valid.is_valid(**kwargs):
                raise ValueError(valid.error_message(**kwargs))

    return fn


class FieldValidator:
    def __init__(self, fn, field_name, field_type):
        self.fn = fn
        self.field_type = field_type
        self.field_name = field_name

    def is_valid(self, **kwargs):
        return self.fn(kwargs["params"]["data"][self.field_name], kwargs["params"])

    def error_message(self, **kwargs):
        return "Validation failed in field {}".format(self.field_name)
