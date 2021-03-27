from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString


class DisableIntrospectionMiddleware(object):

    @staticmethod
    def resolve(next, root, info, **kwargs):
        if info.field_name.lower() in ['__schema', '__introspection']:
            query = GraphQLObjectType(
                "Query", lambda: {"ID": GraphQLField(GraphQLString, resolver=lambda *_: "I am a teapot")}
            )
            info.schema = GraphQLSchema(query=query)
            return next(root, info, **kwargs)
        return next(root, info, **kwargs)
