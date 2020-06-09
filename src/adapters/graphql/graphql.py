import graphene

from adapters.base import Adapter
from adapters.graphql.converter import convert_field
from adapters.graphql.registry import get_class


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_field(field, **kwargs)

    def convert_action(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, input=True)

        field = action.return_value.convert(self, **params)

        def resolve_field(*args, **kwargs):
            return action.exec_fn(*args, **kwargs)

        return field, resolve_field

    def convert_fields_for_object(self, obj):
        out = {}
        for name, field in obj.fields.items():
            out[name] = field.convert(self)
        return out

    def convert_actions_for_object(self, obj):
        out = {}
        for name, action in obj.actions.items():
            out[name], out["resolve_{}".format(name)] = action.convert(self)
        return out

    def generate(self):
        obj_classes = []
        query_classes = []

        for obj in self.objects:
            obj_class = get_class(obj)

            for name, field in self.convert_fields_for_object(obj).items():
                obj_class._meta.fields[name] = field

            obj_classes.append(obj_class)

            actions = self.convert_actions_for_object(obj)

            if actions:
                query_class = type("Query", (graphene.ObjectType,), actions)
                query_classes.append(query_class)

        query_class = type("Query", tuple(query_classes) + (graphene.ObjectType,), {})
        return graphene.Schema(query=query_class)
