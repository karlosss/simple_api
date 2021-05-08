import json

from django.urls import path
from graphene_django.utils import GraphQLTestCase as OriginalGraphQLTestCase
from graphene_django.views import GraphQLView


def remove_ws(s):
    return " ".join(s.split())


class Empty:
    pass


def ascii_sum(s):
    return sum([ord(c) for c in str(s).replace(" ", "").replace("\n", "").replace("\t", "")])


class GraphQLTestCase(OriginalGraphQLTestCase):
    GRAPHQL_URL = "/api/"
    REF_META_SCHEMA = None
    GRAPHQL_SCHEMA = Empty
    REF_GRAPHQL_SCHEMA = None

    # TODO do this better
    def assertJSONEqualArraysShuffled(self, raw, ref):
        self.assertEqual(ascii_sum(raw), ascii_sum(ref))

    def test_schema(self):
        if self.REF_GRAPHQL_SCHEMA is None:
            return
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(str(self.REF_GRAPHQL_SCHEMA))
        )

    def test_meta_schema(self):
        if self.REF_META_SCHEMA is None:
            return

        resp = self.query(
            """
            query Metaschema{
              __types{
                typename
                fields{
                name
                typename
                }
              }
              __objects{
                name
                pk_field
                actions{
                name
                parameters{
                    name
                    typename
                  default
                }
                data{
                    name
                    typename
                  default
                }
                mutation
                return_type
                permitted
                deny_reason
                retry_in
                }
              }
              __actions{
                name
                parameters{
                  name
                  typename
                  default
                }
                data{
                    name
                    typename
                  default
                }
                mutation
                return_type
                permitted
                deny_reason
                retry_in
              }
            }
            """
        )

        self.assertResponseNoErrors(resp)

        # ignore the order of the elements
        data = json.loads(resp.content)
        self.assertJSONEqualArraysShuffled(data, self.REF_META_SCHEMA)
