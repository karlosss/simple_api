from adapters.graphql.utils import capitalize
from object.registry import object_storage


def object_info(**kwargs):
    out = []
    for cls in object_storage.storage.values():
        if getattr(cls, "hidden", False):
            continue
        item = {
            "name": cls.__name__,
            "pk_field": getattr(cls, "pk_field", None),
            "actions": build_actions_resolver(cls, with_object=False)(**kwargs)
        }
        out.append(item)
    return out


def build_actions_resolver(cls, with_object=True):
    def actions_resolver(**kwargs):
        out = []
        for action in cls.actions.values():
            if action.with_object != with_object or action.hidden:
                continue

            try:
                action.has_permission(**kwargs)
                permitted = True
                deny_reason = None
            except PermissionError as e:
                if action.hide_if_denied:
                    continue
                permitted = False
                deny_reason = str(e)

            action_item = {
                "name": "{}{}".format(cls.__name__, capitalize(action.name)),
                "permitted": permitted,
                "deny_reason": deny_reason,
                "retry_in": action.retry_in,
                "choices": action.choice_map
            }
            out.append(action_item)
        return out
    return actions_resolver
