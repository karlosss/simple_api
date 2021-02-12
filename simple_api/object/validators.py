from inspect import isclass


def build_validation_fn(action_validators, field_validators):
    if action_validators and field_validators is None:
        return None

    if not isinstance(action_validators, (list, tuple)):
        action_validators = action_validators,

    instantiated_validators = []
    for cls_or_inst in action_validators:
        if isclass(cls_or_inst):
            instantiated_validators.append(cls_or_inst())
        else:
            instantiated_validators.append(cls_or_inst)
    for tup_of_validators in field_validators:
        for validator in tup_of_validators[1]:
            if isclass(validator):
                instantiated_validators.append((tup_of_validators[0], validator()))
            else:
                instantiated_validators.append((tup_of_validators[0], validator))

    def fn(**kwargs):
        for valid in instantiated_validators:
            if isinstance(valid, tuple):
                if not valid[1].is_valid(valid[0], **kwargs):
                    raise ValueError(valid[1].error_message(**kwargs))
            else:
                if not valid.is_valid(**kwargs):
                    raise ValueError(valid.error_message(**kwargs))
    return fn


class FieldValidator:
    def __init__(self):
        pass

    def is_valid(self, parameter, **kwargs):
        return self.validation_statement(kwargs["params"][parameter], **kwargs)

    def validation_statement(self, value, **kwargs):
        raise NotImplementedError()

    def error_message(self, **kwargs):
        return "Validation failed in field {}".format(self.field_name)


class ActionValidator:
    def __init__(self):
        pass

    def is_valid(self, **kwargs):
        return self.validation_statement(kwargs["params"]["data"], **kwargs)

    def validation_statement(self, value, **kwargs):
        raise NotImplementedError()

    def error_message(self, **kwargs):
        return "Validation failed in action"
