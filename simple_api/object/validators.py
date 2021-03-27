from inspect import isclass


def build_validation_fn(action_validators, parameter_validators, data_validators):
    """
    Prepares function for validation of input values and the action overall, instantiates validators which are not
    already instantiated. Action_validators can be a sigle validator, Field_validators a List of tuples
    (string, (validators...)) as prepared in object/actions.py
    """
    ins_action_validators = []
    ins_parameter_validators = {}
    ins_data_validators = {}

    # Validators instantiation if they are not already
    for cls_or_inst in action_validators:
        if isclass(cls_or_inst):
            ins_action_validators.append(cls_or_inst())
        else:
            ins_action_validators.append(cls_or_inst)
    for parameter_field, parameter_validators in parameter_validators.items():
        for validator in parameter_validators:
            if isclass(validator):
                ins_parameter_validators.setdefault(parameter_field, []).append(validator())
            else:
                ins_parameter_validators.setdefault(parameter_field, []).append(validator)
    for data_field, data_validators in data_validators.items():
        for validator in data_validators:
            if isclass(validator):
                ins_data_validators.setdefault(data_field, []).append(validator())
            else:
                ins_data_validators.setdefault(data_field, []).append(validator)

    def fn(**kwargs):
        # Action validators
        for valid in ins_action_validators:
            if not valid.validation_statement(**kwargs):
                raise ValueError(valid.error_message(**kwargs))
        # Parameters validators
        for param_field, validators in ins_parameter_validators.items():
            for validator in validators:
                if param_field in kwargs["params"] and \
                        not validator.is_valid(kwargs["request"], value=kwargs["params"][param_field]):
                    raise ValueError(validator.error_message(error_field=param_field, **kwargs))

        # Data validators
        for data_field, validators in ins_data_validators.items():
            for validator in validators:
                if data_field in kwargs["params"]["data"] and \
                        not validator.is_valid(kwargs["request"], value=kwargs["params"]["data"][data_field]):
                    raise ValueError(validator.error_message(error_field=data_field, **kwargs))

    return fn


class Validator:
    """
    Base class for input field validation, validation itself is done within validation_statement(self, value,
    **kwargs)
    """

    def is_valid(self, request, value=None, exclude_classes=(), **kwargs):
        for cls in reversed(self.__class__.__mro__):
            if cls in (object, Validator) + exclude_classes:
                continue
            if not self.validation_statement(request, value=value, **kwargs):
                return False
        return True

    def validation_statement(self, request, value=None, **kwargs):
        """Function to validate input value, True -> input is valid, False -> invalid"""
        raise NotImplementedError

    def error_message(self, error_field=None, **kwargs):
        """Message to return in API when validation fails"""

        if error_field:
            return "Validation failed in Validator \"{}\" on field \"{}\"".format(self.__class__.__name__, error_field)
        return "Validation failed in Validator \"{}\"".format(self.__class__.__name__)


class LogicalConnector:
    def __init__(self, *validators):
        self.validators = []
        for cls_or_inst in validators:
            if isclass(cls_or_inst):
                self.validators.append(cls_or_inst())
            else:
                self.validators.append(cls_or_inst)

    def is_valid(self, request, value=None, exclude_classes=(), **kwargs):
        return NotImplementedError

    def error_message(self, error_field=None, **kwargs):
        """Message to return in API when validation fails"""

        if error_field:
            return "Validation failed in LogicalConnector \"{}\" on field \"{}\"".format(self.__class__.__name__, error_field)
        return "Validation failed in LogicalConnector \"{}\"".format(self.__class__.__name__)


class And(LogicalConnector):
    def is_valid(self, request, value=None, exclude_classes=(), **kwargs):
        for validator in self.validators:
            if not validator.is_valid(request, value, exclude_classes=exclude_classes, **kwargs):
                return False
        return True


class Or(LogicalConnector):
    def is_valid(self, request, value=None, exclude_classes=(), **kwargs):
        for validator in self.validators:
            if validator.is_valid(request, value, exclude_classes=exclude_classes, **kwargs):
                return True
        return False


class Not(LogicalConnector):
    def is_valid(self, request, value=None, exclude_classes=(), **kwargs):
        assert len(self.validators) == 1, "`Not` accepts only one validator as parameter."
        return not self.validators[0].is_valid(request, value, exclude_classes=exclude_classes, **kwargs)
