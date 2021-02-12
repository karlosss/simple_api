from inspect import isclass


def build_validation_fn(action_validators, field_validators):
    """
    Prepares function for validation of input values and the action overall, instantiates validators which are not
    already instantiated. Action_validators can be a sigle validator, Field_validators a List of tuples
    (string, (validators...)) as prepared in object/actions.py
    """
    if action_validators and field_validators is None:
        return None

    if not isinstance(action_validators, (list, tuple)):
        action_validators = action_validators,

    # Validators instantiation if they are not already
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
                if not valid.validation_statement(**kwargs):
                    raise ValueError(valid.error_message(**kwargs))
    return fn


class FieldValidator:
    """
    Base class for input field validation, validation itself is done withing validation_statement(self, value,
    **kwargs)
    """
    def __init__(self):
        pass

    def is_valid(self, parameter, **kwargs):
        """Function for passing correct value into validation_statement value argument"""
        return self.validation_statement(kwargs["params"][parameter], **kwargs)

    def validation_statement(self, value, **kwargs):
        """Function to validate input value, True -> input is valid, False -> invalid"""
        raise NotImplementedError()

    def error_message(self, **kwargs):
        """Message to return in API when validation fails"""
        return "Validation failed in FieldValidator"


class ActionValidator:
    """Base class for action validation"""
    def __init__(self):
        pass

    def validation_statement(self, **kwargs):
        """Function to validate action - called directly as no value argument needs to be extracted"""
        raise NotImplementedError()

    def error_message(self, **kwargs):
        """Message to return in API when validation fails"""
        return "Validation failed in ActionValidator"
