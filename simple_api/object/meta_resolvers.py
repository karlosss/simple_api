from copy import deepcopy

from simple_api.adapters.graphql.utils import capitalize
from simple_api.object.registry import object_storage
from simple_api.utils import AttrDict


def object_info(**kwargs):
    out = []
    for cls in object_storage.storage.values():
        if getattr(cls, "hidden", False):
            continue
        if not cls.actions:
            continue
        item = {
            "name": cls.__name__,
            "pk_field": getattr(cls, "pk_field", None),
            "actions": build_actions_resolver(cls, with_object=False)(**kwargs)
        }
        out.append(item)
    return out


def type_info(**kwargs):
    out = []
    for cls in object_storage.storage.values():
        if getattr(cls, "hidden", False):
            continue

        fields = []
        for field_name, field in cls.out_fields.items():
            if not field_name.startswith("__"):
                fields.append(build_field_info(field_name, field))

        item = {
            "typename": cls.__name__,
            "fields": fields
        }
        out.append(item)
    return out


def build_action_info_fn(actions):
    dummy_cls = AttrDict(__name__="", actions=deepcopy(actions))
    return build_actions_resolver(dummy_cls, with_object=False)


def build_field_info(field_name, field):
    return {
        "name": field_name,
        "typename": str(field),
        "default": field.default()
    }


def build_actions_resolver(cls, with_object=True):
    def actions_resolver(**kwargs):
        out = []
        for action in cls.actions.values():
            if action.with_object != with_object or action.hidden:
                continue

            params = []
            for param_name, param in action.parameters.items():
                params.append(build_field_info(param_name, param))

            data = []
            for field_name, field in action.data.items():
                data.append(build_field_info(field_name, field))

            try:
                action.has_permission(**kwargs)
                permitted = True
                deny_reason = None
            except PermissionError as e:
                if action.hide_if_denied:
                    continue
                permitted = False
                deny_reason = str(e)

            try:
                mutation = action.kwargs["mutation"]
            except KeyError:
                mutation = False

            action_item = {
                # todo change this to be graphql independent
                "name": "{}{}".format(cls.__name__, capitalize(action.name) if cls.__name__ != "" else action.name),
                "permitted": permitted,
                "deny_reason": deny_reason,
                "retry_in": action.retry_in,
                "return_type": str(action.return_value),
                "parameters": params,
                "data": data,
                "mutation": mutation
            }
            out.append(action_item)
        return out
    return actions_resolver
