from object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType


def build_action_type(obj):
    return PlainListType(ObjectType(obj), parameters={"name": StringType(nullable=True)})


def build_action_type_fields():
    return {
        "fields": {
            "name": StringType(),
            "permitted": BooleanType(),
            "deny_reason": StringType(nullable=True),
            "retry_in": DurationType(nullable=True),
        }
    }


def build_action_type_resolver(actions):
    def resolver(**kwargs):
        filter_name = kwargs["params"].get("name")
        out = []
        for name, action in actions.items():
            if filter_name and name != filter_name:
                continue
            try:
                action.has_permission(**kwargs)
                permitted = True
            except PermissionError as e:
                if action.hide_if_denied:
                    continue
                permitted = False
                deny_reason = str(e)

            action_data = {
                "name": name,
                "permitted": permitted,
                "deny_reason": deny_reason if not permitted else None,
                "retry_in": action.retry_interval
            }
            out.append(action_data)
        return out
    return resolver
