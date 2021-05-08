from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type ActionInfo {
          name: String!
          parameters: [FieldInfo!]!
          data: [FieldInfo!]!
          return_type: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
          mutation: Boolean!
          __str__: String!
        }
        
        type ContentType {
          id: Int!
          app_label: String!
          model: String!
          logentry_set(filters: LogEntryFiltersInput): LogEntryList!
          permission_set(filters: PermissionFiltersInput): PermissionList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        scalar DateTime
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type Group {
          id: Int!
          name: String!
          permissions(filters: PermissionFiltersInput): PermissionList!
          user_set(filters: UserFiltersInput): UserList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input GroupFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          name: String
          name__contains: String
          name__endswith: String
          name__exact: String
          name__icontains: String
          name__in: [String!]
          name__iregex: String
          name__isnull: Boolean
          name__regex: String
          name__startswith: String
          ordering: [String!]
        }
        
        type GroupList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [Group!]!
          __str__: String!
        }
        
        type LogEntry {
          id: Int!
          action_time: DateTime!
          object_id: String
          object_repr: String!
          action_flag: Int!
          change_message: String!
          user: User!
          content_type: ContentType
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input LogEntryFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          object_id: String
          object_id__contains: String
          object_id__endswith: String
          object_id__exact: String
          object_id__icontains: String
          object_id__in: [String!]
          object_id__iregex: String
          object_id__isnull: Boolean
          object_id__regex: String
          object_id__startswith: String
          object_repr: String
          object_repr__contains: String
          object_repr__endswith: String
          object_repr__exact: String
          object_repr__icontains: String
          object_repr__in: [String!]
          object_repr__iregex: String
          object_repr__isnull: Boolean
          object_repr__regex: String
          object_repr__startswith: String
          action_flag: Int
          action_flag__exact: Int
          action_flag__gt: Int
          action_flag__gte: Int
          action_flag__in: [Int!]
          action_flag__isnull: Boolean
          action_flag__lt: Int
          action_flag__lte: Int
          change_message: String
          change_message__contains: String
          change_message__endswith: String
          change_message__exact: String
          change_message__icontains: String
          change_message__in: [String!]
          change_message__iregex: String
          change_message__isnull: Boolean
          change_message__regex: String
          change_message__startswith: String
          user_id: Int
          user_id__exact: Int
          user_id__gt: Int
          user_id__gte: Int
          user_id__in: [Int!]
          user_id__isnull: Boolean
          user_id__lt: Int
          user_id__lte: Int
          content_type_id: Int
          content_type_id__exact: Int
          content_type_id__gt: Int
          content_type_id__gte: Int
          content_type_id__in: [Int!]
          content_type_id__isnull: Boolean
          content_type_id__lt: Int
          content_type_id__lte: Int
          ordering: [String!]
        }
        
        type LogEntryList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [LogEntry!]!
          __str__: String!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Permission {
          id: Int!
          name: String!
          codename: String!
          content_type: ContentType!
          group_set(filters: GroupFiltersInput): GroupList!
          user_set(filters: UserFiltersInput): UserList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input PermissionFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          name: String
          name__contains: String
          name__endswith: String
          name__exact: String
          name__icontains: String
          name__in: [String!]
          name__iregex: String
          name__isnull: Boolean
          name__regex: String
          name__startswith: String
          codename: String
          codename__contains: String
          codename__endswith: String
          codename__exact: String
          codename__icontains: String
          codename__in: [String!]
          codename__iregex: String
          codename__isnull: Boolean
          codename__regex: String
          codename__startswith: String
          content_type_id: Int
          content_type_id__exact: Int
          content_type_id__gt: Int
          content_type_id__gte: Int
          content_type_id__in: [Int!]
          content_type_id__isnull: Boolean
          content_type_id__lt: Int
          content_type_id__lte: Int
          ordering: [String!]
        }
        
        type PermissionList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [Permission!]!
          __str__: String!
        }
        
        type Query {
          UserDetail(id: Int!): User!
          UserList(filters: UserFiltersInput): UserList!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
        
        type User {
          id: Int!
          password: String!
          last_login: DateTime
          is_superuser: Boolean!
          username: String!
          first_name: String!
          last_name: String!
          email: String!
          is_staff: Boolean!
          is_active: Boolean!
          date_joined: DateTime!
          groups(filters: GroupFiltersInput): GroupList!
          user_permissions(filters: PermissionFiltersInput): PermissionList!
          logentry_set(filters: LogEntryFiltersInput): LogEntryList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input UserFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          password: String
          password__contains: String
          password__endswith: String
          password__exact: String
          password__icontains: String
          password__in: [String!]
          password__iregex: String
          password__isnull: Boolean
          password__regex: String
          password__startswith: String
          username: String
          username__contains: String
          username__endswith: String
          username__exact: String
          username__icontains: String
          username__in: [String!]
          username__iregex: String
          username__isnull: Boolean
          username__regex: String
          username__startswith: String
          first_name: String
          first_name__contains: String
          first_name__endswith: String
          first_name__exact: String
          first_name__icontains: String
          first_name__in: [String!]
          first_name__iregex: String
          first_name__isnull: Boolean
          first_name__regex: String
          first_name__startswith: String
          last_name: String
          last_name__contains: String
          last_name__endswith: String
          last_name__exact: String
          last_name__icontains: String
          last_name__in: [String!]
          last_name__iregex: String
          last_name__isnull: Boolean
          last_name__regex: String
          last_name__startswith: String
          email: String
          email__contains: String
          email__endswith: String
          email__exact: String
          email__icontains: String
          email__in: [String!]
          email__iregex: String
          email__isnull: Boolean
          email__regex: String
          email__startswith: String
          ordering: [String!]
        }
        
        type UserList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [User!]!
          __str__: String!
        }
        """

    REF_META_SCHEMA = {
      "data": {
        "__types": [
          {
            "typename": "UserFilters",
            "fields": [
              {
                "name": "id",
                "typename": "Integer"
              },
              {
                "name": "id__exact",
                "typename": "Integer"
              },
              {
                "name": "id__gt",
                "typename": "Integer"
              },
              {
                "name": "id__gte",
                "typename": "Integer"
              },
              {
                "name": "id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "id__lt",
                "typename": "Integer"
              },
              {
                "name": "id__lte",
                "typename": "Integer"
              },
              {
                "name": "password",
                "typename": "String"
              },
              {
                "name": "password__contains",
                "typename": "String"
              },
              {
                "name": "password__endswith",
                "typename": "String"
              },
              {
                "name": "password__exact",
                "typename": "String"
              },
              {
                "name": "password__icontains",
                "typename": "String"
              },
              {
                "name": "password__in",
                "typename": "[String!]"
              },
              {
                "name": "password__iregex",
                "typename": "String"
              },
              {
                "name": "password__isnull",
                "typename": "Boolean"
              },
              {
                "name": "password__regex",
                "typename": "String"
              },
              {
                "name": "password__startswith",
                "typename": "String"
              },
              {
                "name": "username",
                "typename": "String"
              },
              {
                "name": "username__contains",
                "typename": "String"
              },
              {
                "name": "username__endswith",
                "typename": "String"
              },
              {
                "name": "username__exact",
                "typename": "String"
              },
              {
                "name": "username__icontains",
                "typename": "String"
              },
              {
                "name": "username__in",
                "typename": "[String!]"
              },
              {
                "name": "username__iregex",
                "typename": "String"
              },
              {
                "name": "username__isnull",
                "typename": "Boolean"
              },
              {
                "name": "username__regex",
                "typename": "String"
              },
              {
                "name": "username__startswith",
                "typename": "String"
              },
              {
                "name": "first_name",
                "typename": "String"
              },
              {
                "name": "first_name__contains",
                "typename": "String"
              },
              {
                "name": "first_name__endswith",
                "typename": "String"
              },
              {
                "name": "first_name__exact",
                "typename": "String"
              },
              {
                "name": "first_name__icontains",
                "typename": "String"
              },
              {
                "name": "first_name__in",
                "typename": "[String!]"
              },
              {
                "name": "first_name__iregex",
                "typename": "String"
              },
              {
                "name": "first_name__isnull",
                "typename": "Boolean"
              },
              {
                "name": "first_name__regex",
                "typename": "String"
              },
              {
                "name": "first_name__startswith",
                "typename": "String"
              },
              {
                "name": "last_name",
                "typename": "String"
              },
              {
                "name": "last_name__contains",
                "typename": "String"
              },
              {
                "name": "last_name__endswith",
                "typename": "String"
              },
              {
                "name": "last_name__exact",
                "typename": "String"
              },
              {
                "name": "last_name__icontains",
                "typename": "String"
              },
              {
                "name": "last_name__in",
                "typename": "[String!]"
              },
              {
                "name": "last_name__iregex",
                "typename": "String"
              },
              {
                "name": "last_name__isnull",
                "typename": "Boolean"
              },
              {
                "name": "last_name__regex",
                "typename": "String"
              },
              {
                "name": "last_name__startswith",
                "typename": "String"
              },
              {
                "name": "email",
                "typename": "String"
              },
              {
                "name": "email__contains",
                "typename": "String"
              },
              {
                "name": "email__endswith",
                "typename": "String"
              },
              {
                "name": "email__exact",
                "typename": "String"
              },
              {
                "name": "email__icontains",
                "typename": "String"
              },
              {
                "name": "email__in",
                "typename": "[String!]"
              },
              {
                "name": "email__iregex",
                "typename": "String"
              },
              {
                "name": "email__isnull",
                "typename": "Boolean"
              },
              {
                "name": "email__regex",
                "typename": "String"
              },
              {
                "name": "email__startswith",
                "typename": "String"
              },
              {
                "name": "ordering",
                "typename": "[String!]"
              }
            ]
          },
          {
            "typename": "User",
            "fields": [
              {
                "name": "id",
                "typename": "Integer!"
              },
              {
                "name": "password",
                "typename": "String!"
              },
              {
                "name": "last_login",
                "typename": "DateTime"
              },
              {
                "name": "is_superuser",
                "typename": "Boolean!"
              },
              {
                "name": "username",
                "typename": "String!"
              },
              {
                "name": "first_name",
                "typename": "String!"
              },
              {
                "name": "last_name",
                "typename": "String!"
              },
              {
                "name": "email",
                "typename": "String!"
              },
              {
                "name": "is_staff",
                "typename": "Boolean!"
              },
              {
                "name": "is_active",
                "typename": "Boolean!"
              },
              {
                "name": "date_joined",
                "typename": "DateTime!"
              },
              {
                "name": "groups",
                "typename": "Paginated[Group]!"
              },
              {
                "name": "user_permissions",
                "typename": "Paginated[Permission]!"
              },
              {
                "name": "logentry_set",
                "typename": "Paginated[LogEntry]!"
              }
            ]
          },
          {
            "typename": "LogEntryFilters",
            "fields": [
              {
                "name": "id",
                "typename": "Integer"
              },
              {
                "name": "id__exact",
                "typename": "Integer"
              },
              {
                "name": "id__gt",
                "typename": "Integer"
              },
              {
                "name": "id__gte",
                "typename": "Integer"
              },
              {
                "name": "id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "id__lt",
                "typename": "Integer"
              },
              {
                "name": "id__lte",
                "typename": "Integer"
              },
              {
                "name": "object_id",
                "typename": "String"
              },
              {
                "name": "object_id__contains",
                "typename": "String"
              },
              {
                "name": "object_id__endswith",
                "typename": "String"
              },
              {
                "name": "object_id__exact",
                "typename": "String"
              },
              {
                "name": "object_id__icontains",
                "typename": "String"
              },
              {
                "name": "object_id__in",
                "typename": "[String!]"
              },
              {
                "name": "object_id__iregex",
                "typename": "String"
              },
              {
                "name": "object_id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "object_id__regex",
                "typename": "String"
              },
              {
                "name": "object_id__startswith",
                "typename": "String"
              },
              {
                "name": "object_repr",
                "typename": "String"
              },
              {
                "name": "object_repr__contains",
                "typename": "String"
              },
              {
                "name": "object_repr__endswith",
                "typename": "String"
              },
              {
                "name": "object_repr__exact",
                "typename": "String"
              },
              {
                "name": "object_repr__icontains",
                "typename": "String"
              },
              {
                "name": "object_repr__in",
                "typename": "[String!]"
              },
              {
                "name": "object_repr__iregex",
                "typename": "String"
              },
              {
                "name": "object_repr__isnull",
                "typename": "Boolean"
              },
              {
                "name": "object_repr__regex",
                "typename": "String"
              },
              {
                "name": "object_repr__startswith",
                "typename": "String"
              },
              {
                "name": "action_flag",
                "typename": "Integer"
              },
              {
                "name": "action_flag__exact",
                "typename": "Integer"
              },
              {
                "name": "action_flag__gt",
                "typename": "Integer"
              },
              {
                "name": "action_flag__gte",
                "typename": "Integer"
              },
              {
                "name": "action_flag__in",
                "typename": "[Integer!]"
              },
              {
                "name": "action_flag__isnull",
                "typename": "Boolean"
              },
              {
                "name": "action_flag__lt",
                "typename": "Integer"
              },
              {
                "name": "action_flag__lte",
                "typename": "Integer"
              },
              {
                "name": "change_message",
                "typename": "String"
              },
              {
                "name": "change_message__contains",
                "typename": "String"
              },
              {
                "name": "change_message__endswith",
                "typename": "String"
              },
              {
                "name": "change_message__exact",
                "typename": "String"
              },
              {
                "name": "change_message__icontains",
                "typename": "String"
              },
              {
                "name": "change_message__in",
                "typename": "[String!]"
              },
              {
                "name": "change_message__iregex",
                "typename": "String"
              },
              {
                "name": "change_message__isnull",
                "typename": "Boolean"
              },
              {
                "name": "change_message__regex",
                "typename": "String"
              },
              {
                "name": "change_message__startswith",
                "typename": "String"
              },
              {
                "name": "user_id",
                "typename": "Integer"
              },
              {
                "name": "user_id__exact",
                "typename": "Integer"
              },
              {
                "name": "user_id__gt",
                "typename": "Integer"
              },
              {
                "name": "user_id__gte",
                "typename": "Integer"
              },
              {
                "name": "user_id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "user_id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "user_id__lt",
                "typename": "Integer"
              },
              {
                "name": "user_id__lte",
                "typename": "Integer"
              },
              {
                "name": "content_type_id",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__exact",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__gt",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__gte",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "content_type_id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "content_type_id__lt",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__lte",
                "typename": "Integer"
              },
              {
                "name": "ordering",
                "typename": "[String!]"
              }
            ]
          },
          {
            "typename": "LogEntry",
            "fields": [
              {
                "name": "id",
                "typename": "Integer!"
              },
              {
                "name": "action_time",
                "typename": "DateTime!"
              },
              {
                "name": "object_id",
                "typename": "String"
              },
              {
                "name": "object_repr",
                "typename": "String!"
              },
              {
                "name": "action_flag",
                "typename": "Integer!"
              },
              {
                "name": "change_message",
                "typename": "String!"
              },
              {
                "name": "user",
                "typename": "User!"
              },
              {
                "name": "content_type",
                "typename": "ContentType"
              }
            ]
          },
          {
            "typename": "PermissionFilters",
            "fields": [
              {
                "name": "id",
                "typename": "Integer"
              },
              {
                "name": "id__exact",
                "typename": "Integer"
              },
              {
                "name": "id__gt",
                "typename": "Integer"
              },
              {
                "name": "id__gte",
                "typename": "Integer"
              },
              {
                "name": "id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "id__lt",
                "typename": "Integer"
              },
              {
                "name": "id__lte",
                "typename": "Integer"
              },
              {
                "name": "name",
                "typename": "String"
              },
              {
                "name": "name__contains",
                "typename": "String"
              },
              {
                "name": "name__endswith",
                "typename": "String"
              },
              {
                "name": "name__exact",
                "typename": "String"
              },
              {
                "name": "name__icontains",
                "typename": "String"
              },
              {
                "name": "name__in",
                "typename": "[String!]"
              },
              {
                "name": "name__iregex",
                "typename": "String"
              },
              {
                "name": "name__isnull",
                "typename": "Boolean"
              },
              {
                "name": "name__regex",
                "typename": "String"
              },
              {
                "name": "name__startswith",
                "typename": "String"
              },
              {
                "name": "codename",
                "typename": "String"
              },
              {
                "name": "codename__contains",
                "typename": "String"
              },
              {
                "name": "codename__endswith",
                "typename": "String"
              },
              {
                "name": "codename__exact",
                "typename": "String"
              },
              {
                "name": "codename__icontains",
                "typename": "String"
              },
              {
                "name": "codename__in",
                "typename": "[String!]"
              },
              {
                "name": "codename__iregex",
                "typename": "String"
              },
              {
                "name": "codename__isnull",
                "typename": "Boolean"
              },
              {
                "name": "codename__regex",
                "typename": "String"
              },
              {
                "name": "codename__startswith",
                "typename": "String"
              },
              {
                "name": "content_type_id",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__exact",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__gt",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__gte",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "content_type_id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "content_type_id__lt",
                "typename": "Integer"
              },
              {
                "name": "content_type_id__lte",
                "typename": "Integer"
              },
              {
                "name": "ordering",
                "typename": "[String!]"
              }
            ]
          },
          {
            "typename": "Permission",
            "fields": [
              {
                "name": "id",
                "typename": "Integer!"
              },
              {
                "name": "name",
                "typename": "String!"
              },
              {
                "name": "codename",
                "typename": "String!"
              },
              {
                "name": "content_type",
                "typename": "ContentType!"
              },
              {
                "name": "group_set",
                "typename": "Paginated[Group]!"
              },
              {
                "name": "user_set",
                "typename": "Paginated[User]!"
              }
            ]
          },
          {
            "typename": "GroupFilters",
            "fields": [
              {
                "name": "id",
                "typename": "Integer"
              },
              {
                "name": "id__exact",
                "typename": "Integer"
              },
              {
                "name": "id__gt",
                "typename": "Integer"
              },
              {
                "name": "id__gte",
                "typename": "Integer"
              },
              {
                "name": "id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "id__lt",
                "typename": "Integer"
              },
              {
                "name": "id__lte",
                "typename": "Integer"
              },
              {
                "name": "name",
                "typename": "String"
              },
              {
                "name": "name__contains",
                "typename": "String"
              },
              {
                "name": "name__endswith",
                "typename": "String"
              },
              {
                "name": "name__exact",
                "typename": "String"
              },
              {
                "name": "name__icontains",
                "typename": "String"
              },
              {
                "name": "name__in",
                "typename": "[String!]"
              },
              {
                "name": "name__iregex",
                "typename": "String"
              },
              {
                "name": "name__isnull",
                "typename": "Boolean"
              },
              {
                "name": "name__regex",
                "typename": "String"
              },
              {
                "name": "name__startswith",
                "typename": "String"
              },
              {
                "name": "ordering",
                "typename": "[String!]"
              }
            ]
          },
          {
            "typename": "Group",
            "fields": [
              {
                "name": "id",
                "typename": "Integer!"
              },
              {
                "name": "name",
                "typename": "String!"
              },
              {
                "name": "permissions",
                "typename": "Paginated[Permission]!"
              },
              {
                "name": "user_set",
                "typename": "Paginated[User]!"
              }
            ]
          },
          {
            "typename": "ContentTypeFilters",
            "fields": [
              {
                "name": "id",
                "typename": "Integer"
              },
              {
                "name": "id__exact",
                "typename": "Integer"
              },
              {
                "name": "id__gt",
                "typename": "Integer"
              },
              {
                "name": "id__gte",
                "typename": "Integer"
              },
              {
                "name": "id__in",
                "typename": "[Integer!]"
              },
              {
                "name": "id__isnull",
                "typename": "Boolean"
              },
              {
                "name": "id__lt",
                "typename": "Integer"
              },
              {
                "name": "id__lte",
                "typename": "Integer"
              },
              {
                "name": "app_label",
                "typename": "String"
              },
              {
                "name": "app_label__contains",
                "typename": "String"
              },
              {
                "name": "app_label__endswith",
                "typename": "String"
              },
              {
                "name": "app_label__exact",
                "typename": "String"
              },
              {
                "name": "app_label__icontains",
                "typename": "String"
              },
              {
                "name": "app_label__in",
                "typename": "[String!]"
              },
              {
                "name": "app_label__iregex",
                "typename": "String"
              },
              {
                "name": "app_label__isnull",
                "typename": "Boolean"
              },
              {
                "name": "app_label__regex",
                "typename": "String"
              },
              {
                "name": "app_label__startswith",
                "typename": "String"
              },
              {
                "name": "model",
                "typename": "String"
              },
              {
                "name": "model__contains",
                "typename": "String"
              },
              {
                "name": "model__endswith",
                "typename": "String"
              },
              {
                "name": "model__exact",
                "typename": "String"
              },
              {
                "name": "model__icontains",
                "typename": "String"
              },
              {
                "name": "model__in",
                "typename": "[String!]"
              },
              {
                "name": "model__iregex",
                "typename": "String"
              },
              {
                "name": "model__isnull",
                "typename": "Boolean"
              },
              {
                "name": "model__regex",
                "typename": "String"
              },
              {
                "name": "model__startswith",
                "typename": "String"
              },
              {
                "name": "ordering",
                "typename": "[String!]"
              }
            ]
          },
          {
            "typename": "ContentType",
            "fields": [
              {
                "name": "id",
                "typename": "Integer!"
              },
              {
                "name": "app_label",
                "typename": "String!"
              },
              {
                "name": "model",
                "typename": "String!"
              },
              {
                "name": "logentry_set",
                "typename": "Paginated[LogEntry]!"
              },
              {
                "name": "permission_set",
                "typename": "Paginated[Permission]!"
              }
            ]
          }
        ],
        "__objects": [
          {
            "name": "User",
            "pk_field": "id",
            "actions": [
              {
                "name": "UserList",
                "parameters": [
                  {
                    "name": "filters",
                    "typename": "UserFilters",
                    "default": None
                  }
                ],
                "data": [],
                "mutation": False,
                "return_type": "Paginated[User]!",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              }
            ]
          }
        ],
        "__actions": []
      }
    }
