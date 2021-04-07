# Simple API

[![Run tests](https://github.com/ladal1/simple_api/actions/workflows/run_tests.yml/badge.svg)](https://github.com/ladal1/simple_api/actions/workflows/run_tests.yml)

## Purpose of the project
After writing Django models, Simple API builds an API (currently, only GraphQL is supported) extracting the information from the model and requiring to write as little code as possible.

Built on some amazing ideas of [graphene-django-extras](https://github.com/eamigo86/graphene-django-extras). The main difference is that Simple API is a bit more high-level and allows the programmer to write even less code.

## User's Guide

### Introduction

Let's build a forum where users can create posts.
The models are as follows:

```python
from django.db.models import Model, EmailField, CharField, TextField, BooleanField, ForeignKey, CASCADE


class CustomUser(Model):
    email = EmailField()
    username = CharField(max_length=50)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    password = CharField(max_length=50)
    bio = TextField()
    is_admin = BooleanField(default=False)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name 
    
    def __str__(self):
        return "{} ({})".format(self.full_name, self.username)


class Post(Model):
    title = CharField(max_length=50)
    author = ForeignKey(CustomUser, on_delete=CASCADE)
    content = TextField()
    
    def __str__(self):
        return "{} by {}".format(self.title, self.author)

```

Now, we create a Simple API object for each model. We also generate GraphQL API and build URL patterns so that we can access the API:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


class CustomUser(DjangoObject):
    model = CustomUserModel


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
``` 

And that's it! Let's explore what Simple API actually generated for us. Open up `/api/` in the browser (i.e. [http://localhost:8000/api/](http://localhost:8000/api/)) and see the schema:

```
// query

PostDetail(id: Int!): Post!
PostList(filters: PostFiltersInput): PostList!
CustomUserDetail(id: Int!): CustomUser!
CustomUserList(filters: CustomUserFiltersInput): CustomUserList!
__objects: [ObjectInfo!]!
__actions: [ActionInfo!]!

// mutation

CustomUserCreate(data: CustomUserCreateInput!): CustomUser!
CustomUserUpdate(data: CustomUserUpdateInput!id: Int!): CustomUser!
CustomUserDelete(id: Int!): Boolean!
PostCreate(data: PostCreateInput!): Post!
PostUpdate(data: PostUpdateInput!id: Int!): Post!
PostDelete(id: Int!): Boolean!
```

With close to zero effort, we just got a way to do list, show detail, create, update and delete both of our entities. Let's try them one by one.

Create a user:

```graphql
mutation create_user{
  CustomUserCreate(data: {
    email: "user1@example.com", 
    username: "adam", 
    first_name: "Adam", 
    last_name: "First", 
    password: "secret",
    bio: "Just an ordinary person...",
  }){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

// output
{
  "data": {
    "CustomUserCreate": {
      "id": 1,
      "email": "user1@example.com",
      "username": "adam",
      "first_name": "Adam",
      "last_name": "First",
      "password": "secret",
      "bio": "Just an ordinary person...",
      "is_admin": false
    }
  }
}
```

Do a detail of the first user:

```graphql
query detail_of_user{
  CustomUserDetail(id: 1){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

// output
{
  "data": {
    "CustomUserDetail": {
      "id": 1,
      "email": "user1@example.com",
      "username": "adam",
      "first_name": "Adam",
      "last_name": "First",
      "password": "secret",
      "bio": "Just an ordinary person...",
      "is_admin": false
    }
  }
}
```

The listing action is a bit more interesting. In the schema, we can see there an optional parameter to it, `CustomUserFiltersInput`. Let's explore its fields:

```
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
username: String
username__contains: String
...
ordering: [String!]
```

There are automatically generated filter fields for each of the parameters, and the option to specity the order. Both of those use Django syntax.

Upon return, a listing does not just output a list of objects, but rather a `CustomUserList`, which has the following fields:

```
count: Int!
data(limit: Int = 20, offset: Int = 0): [CustomUser!]!
```

`count` returns the length of the list and `data` holds the actual data, accepting two optional parameters, `limit` and `offset`. This allows for pagination.

Now we can create another user and then list both:

```graphql
mutation create_another_user{
  CustomUserCreate(data: {
    email: "user2@example.com", 
    username: "bob", 
    first_name: "Bob", 
    last_name: "Second", 
    password: "secret",
    bio: "Just another ordinary person...",
  }){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

query list_users{
  CustomUserList{
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        },
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        }
      ]
    }
  }
}
```

We can also apply some filters to the listing:

```graphql
query list_filtered_users{
  CustomUserList(filters: {first_name__startswith: "A"}){
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 1,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        }
      ]
    }
  }
}
```

Or we can reorder the results: the primary key is the password, which is the same for both, so the secondary key is applied, which is `id` in the descending order:

```graphql
query list_ordering_users{
  CustomUserList(filters: {ordering: ["password","-id"]}){
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        },
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        }
      ]
    }
  }
}
```

Of course, we can also paginate the results:

```graphql
query list_paginate_users{
  CustomUserList{
    count
    data(offset: 1, limit: 1){
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        }
      ]
    }
  }
}
```

Next, we can update a user's password like this:

```graphql
mutation update_password{
  CustomUserUpdate(id: 1, data: {password: "moresecret"}){
    id
    password
  }
}

// output
{
  "data": {
    "CustomUserUpdate": {
      "id": 1,
      "password": "moresecret"
    }
  }
}
```

And we might delete the second user:

```graphql
mutation delete_user{
  CustomUserDelete(id: 2)
}

// output
{
  "data": {
    "CustomUserDelete": true
  }
}
```

Now, when we list the users again, we can see that there is only one user and the password is changed:

```graphql
query list_users_with_password{
  CustomUserList{
    count
    data{
      id
      first_name
      last_name
      password
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 1,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First",
          "password": "moresecret"
        }
      ]
    }
  }
}
```

And that concludes the showcase of the basic API. Of course, it is very far from what we would like to run on production - we probably don't want the password to be visible and deleting users should be only possible by admin. But as a starting point, this should be good enough.

### Controlling the fields

You for sure noticed that the `CustomUser` model has a property that is not accessible in the API. This is expected - Simple API only automatically converts fields, relations, and reverse relations (you maybe noticed that a `CustomUser` in the first example has `post_set` field in the API). At the end of this section, we show how to add the property.

But let's start from the beginning. Assume the same model, but the following `Object`s:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.datatypes import StringType
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


class ShortCustomUser(DjangoObject):
    model = CustomUserModel
    only_fields = ("first_name", "last_name")
    output_custom_fields = {"full_name": StringType()}


class ShortPost(DjangoObject):
    model = PostModel
    exclude_fields = ("content",)


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

By default, Simple API extracts all fields, models, and reverse relations. If this is not what we want, we have two ways to specify: either list the fields we want using `only_fields`, or list the fields we don't want using `exclude_fields` (but not both at the same time, of course).

After the set of extracted fields is determined, we can add `custom_fields`: each custom field must also have its type specified, as there is no way Simple API can find that out.

Note that model properties are only output fields. Simple API objects can be also used as inputs and in such case, we do not want read-only fields there. Custom fields that should be both for input and output are specified in `custom_fields`, fields only for input in `input_custom_fields`, and those only for output in `output_custom_fields`.

The schema then looks like this:
```
// Short post
id: Int!
title: String!
author: ShortCustomUser!
__str__: String!
__actions: [ActionInfo!]!

// Short custom user
id: Int!
first_name: String!
last_name: String!
full_name: String!
__str__: String!
__actions: [ActionInfo!]!
```

As we can see, the primary key field (in this case `id`) is always included and cannot be got rid of. That comes with a reason - without primary key, the CRUD operations would just not work.

If a custom field happens to have the same name as an extracted field, the original field is overridden. This might be useful for example if a model field is nullable, but we don't want it to be nullable in the API.

### Multiple Objects for one model

Sometimes, we want multiple `Object`s for the same model - for example, the email of a user should be visible only by the user himself and maybe by admins. A way to do this is creating two objects: one for admins, and one for the rest.
```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


class CustomUser(DjangoObject):
    model = CustomUserModel
    class_for_related = False


class CustomUserPublic(DjangoObject):
    model = CustomUserModel
    exclude_fields = ("email", "password")


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

Everything should be self-explanatory except for `class_for_related`. When building relations automatically, Simple API needs to determine a type to return. As long as we have only one `Object` per model, it is obvious as there is no choice. But now Simple API does not know: should it make the field `author` of the `Post` model of type `CustomUser`, or `CustomUserPublic`? And this is exactly what `class_for_related` means: it uses the one which has it set to `True`. That can be seen in the schema - the type of `author` is indeed `CustomUserPublic`, because it is set to be the class to resolve relations:
```
// Post
id: Int!
title: String!
content: String!
author: CustomUserPublic!
__str__: String!
__actions: [ActionInfo!]!
```

If the one-fits-them-all method is not fine-grained enough, the field for relations can be overridden the same way as any other field in `custom_fields`.

### Custom filtering

As shown in the beginning, a `ListAction` has a builtin way to filter the results: it does so by filters automatically generated from fields of the target model.

It is, of course, possible to alter the set of filters generated for a field by overriding the field and specify the filters as follows:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.datatypes import StringType, ObjectType
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


class CustomUser(DjangoObject):
    model = CustomUserModel
    custom_fields = {
        "email": StringType(only_filters=("email__exact", "email__icontains")),
        "first_name": StringType(exclude_filters=("first_name__regex", "first_name__iregex")),
    }


class Post(DjangoObject):
    model = PostModel
    output_custom_fields = {
        "author": ObjectType(CustomUser, exclude_filters=(),
                             custom_filters={"author__email": StringType(nullable=True)})
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)

```

The `only_filters`, `exclude_filters` and `custom_filters` work the same way as filtering fields, with the exception that without modifiers, no filters are created. This is for obvious reasons: if we create a custom field, we probably don't want any filters for it, as it is probably not a field in the database and Django would just crash on those non-existent filters.

Note that when overriding a foreign key field, both the original filters (if intended to keep) and the custom ones need to be specified.

### Custom actions

So far, we only were using the automatically generated actions - `list`, `detail`, `create`, `update` and `delete`. Now we show how to add more: say a user should be able to change their password and list their own posts. But let's start from the beginning.

First, we can modify the way the basic actions are generated:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.actions import CreateAction
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


def custom_create_user(request, params, **kwargs):
    return CustomUserModel.objects.create(
        email="default@example.com",
        username=params["data"]["username"],
        first_name="Name",
        last_name="Surname",
        password="default"
    )


class CustomUser(DjangoObject):
    model = CustomUserModel

    create_action = CreateAction(only_fields=("username",), exec_fn=custom_create_user)
    update_action = None
    delete_action = None


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

```graphql
mutation create_user_username_only{
  CustomUserCreate(data: {username: "cindy"}){
    id
  }
}

// output
{
  "data": {
    "CustomUserCreate": {
      "id": 1,
      "email": "default@example.com",
      "username": "cindy",
      "first_name": "Name",
      "last_name": "Surname",
      "password": "default",
      "bio": "",
      "is_admin": false
    }
  }
}
```

Our customized `CreateAction` has only one data parameter, the username, and the rest is filled with some default values, as specified in `custom_create_user`. If an action should not be generated at all, just set it to `None`.

Let's say we want the users to be able to change their own password. For this, we need to add a custom actions as follows:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.actions import UpdateAction
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns

class CustomUser(DjangoObject):
    model = CustomUserModel

    custom_actions = {
        "changePassword": UpdateAction(only_fields=("password",), 
                                       required_fields=("password",))
    }


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

By default, the fields of an `UpdateAction` are not mandatory - it would be very annoying to
specify the whole large object when modifying just a single value! This, however, is not
always what we want: when the action is supposed to change only the password, the new password
should be mandatory to provide. This is exactly what `required_fields` stands for: specify
the fields which should be required, even in an `UpdateAction`.

Sometimes, an action is not a CRUD operation. For these cases, the custom `exec_fn` must be
written by the user. Refer to `ModelAction` or `ModelObjectAction`, depending if the action
should operate on the object class (like `create` for example), or on specific instances
of the object (like `update` or `delete` for example) respectively.

### Permissions

The forum now has one obvious problem mentioned above - everyone can do everything. Now it is time to change it. 
Each action in Simple API might include a set of permissions required to pass - if it does not, an error occurs
and the action is not performed.

The permissions should only determine if a user is allowed to execute an action or not based on the user and the
current application state. The input data for the action should not be considered. 
**TODO: Rejection based on input data is not implemented yet.**

Permissions are shipped as classes. The key part is overriding the `permission_statement` method:

```python
from django_object.permissions import DjangoPermission
class IsAuthenticated(DjangoPermission):
    def permission_statement(self, request, **kwargs):
        return request and request.user and request.user.is_authenticated
```

Let's say we now want to create an `IsAdmin` permission class, which would allow through only those users
which have either `is_admin` or `is_superuser` set. This is what we would do:

```python
from django_object.permissions import IsAuthenticated
class IsAdmin(IsAuthenticated):
    def permission_statement(self, request, **kwargs):
        return request.user.is_staff or request.user.is_superuser
```

You might be wondering why don't we call the `permission_statement` method of the superclass. One would do
this all the time, therefore Simple API just calls the method of the superclass automatically, based on
the inheritance chain. This saves some boilerplate code and makes the result a bit more readable.

Let's see how to use the permissions in practice. Our forum API enhanced with the permissions could look
as follows:

```python
from django.contrib.auth.models import User as UserModel

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.actions import CreateAction, UpdateAction, DeleteAction, DetailAction, ListAction, ModelAction
from django_object.django_object import DjangoObject
from django_object.permissions import IsAuthenticated
from object.datatypes import StringType
from object.permissions import Or
from .models import Post as PostModel
from simple_api.adapters.graphql.utils import build_patterns


class IsAdmin(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user.is_staff or request.user.is_superuser


class IsSelf(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user == obj


class IsTheirs(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user == obj.author


def set_password(request, params, **kwargs):
    # this would set a password to request.user, but for the showcase it is not needed
    pass


def create_post(request, params, **kwargs):
    data = params["data"]
    return PostModel.objects.create(title=data["title"], content=data["content"], author=request.user)


class User(DjangoObject):
    model = UserModel
    only_fields = ("username", )

    create_action = CreateAction(permissions=IsAdmin)
    update_action = UpdateAction(permissions=IsAdmin)
    delete_action = DeleteAction(permissions=IsAdmin)
    detail_action = DetailAction(permissions=IsAdmin)
    list_action = ListAction(permissions=IsAdmin)

    custom_actions = {
        "changePassword": ModelAction(data={"password": StringType()}, exec_fn=set_password,
                                      permissions=IsAuthenticated),
        "myProfile": ModelAction(exec_fn=lambda request, **kwargs: request.user, permissions=IsAuthenticated)
    }


class Post(DjangoObject):
    model = PostModel

    create_action = CreateAction(exclude_fields=("author_id",), permissions=IsAuthenticated, exec_fn=create_post)
    update_action = UpdateAction(permissions=Or(IsAdmin, IsTheirs))
    delete_action = DeleteAction(permissions=Or(IsAdmin, IsTheirs))
    list_action = ListAction(permissions=IsAuthenticated)
    detail_action = DetailAction(permissions=IsAuthenticated)


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

This slightly more comprehensive example shows how one could do the forum. Let's have two
types of users: admins and the others. Everyone can view their own profile, change their own
password, create and list all posts and edit and delete their own posts. Admins on top of that
can manipulate the database of users and also their posts.

As we can see, for a logical expression consisting of multiple permissions, we can use
`And`, `Or` and `Not` connectors, which form a universal set of connectors, and therefore
can express any logical expression. For sure, we could write a permission class with permission 
statement covering exactly those options, but this way the code is more readable and therefore
less error-prone.

Besides the logical expressions, we also show how to use `ModelAction` and a custom create 
(the autor of the post is the one who sent the create request).

### Meta schemas

**Note: this part will likely significantly change in the future.**

GraphiQL already contains some information about types, parameters, etc. Meta schemas
of Simple API extend this schema by the information about actions and permissions. These
are supposed to be used in order to maintain loose coupling between the backend and any
possible frontend clients.

On the top level, there are two meta endpoints `__objects` and `__actions`. They can be
queried as follows:

```graphql
query{
  __objects{
    name
    pk_field
    actions{
      name
      permitted
      deny_reason
      retry_in
    }
  }
  __actions{
    name
    permitted
    deny_reason
    retry_in
  }
}
```

`__objects` contains information about objects. Each object created in Simple API by the user
is automatically registered. Besides the `name`, Simple API also tells the frontend which
is the primary key field, which is necessary for all actions operating on a specific instance
of an object. Follows a list of actions not bound to any specific instance (such as `create`
or `list`). For each of those actions, Simple API also tells if, based on the user and current
system state, the action is allowed or not, why it is disallowed, and in what time 
this information should be refreshed. This way, frontend can display (or not display)
buttons, disabled buttons, error messages etc.

The `__actions` endpoint covers the actions not connected to a particular object.

Each instance of an object also has `__actions` field:

```graphql
query list_users{
  CustomUserList{
    data{
      id
      username
      password
      __actions{
        name
        permitted
        deny_reason
        retry_in
      }
    }
  }
}
```

This field contains information about actions for that particular instance, for example `update`
or `delete`.

### Creating Objects without Django model

It is also possible to create an object without Django model. In fact, Simple API only
extracts information from Django models, and then completely forgets that Django exists!
These two layers allow for simple modification of the objects - for example, required fields
in Django do not need to be required in Simple API: once the information is extracted from
Django, it can be easily rewritten without looking back to Django, not causing any conflicts.

An example can be seen here:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType, IntegerType, ObjectType
from object.object import Object
from simple_api.adapters.graphql.utils import build_patterns
from utils import AttrDict


def get_by_id(request, params, **kwargs):
    return AttrDict(id=params["id"], car=AttrDict(model="BMW", color="blue"))


class Car(Object):
    fields = {
        "model": StringType(),
        "color": StringType()
    }


class Owner(Object):
    fields = {
        "id": IntegerType(),
        "car": ObjectType(Car)
    }

    actions = {
        "getById": Action(parameters={"id": IntegerType()}, return_value=ObjectType("self"), exec_fn=get_by_id)
    }

schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
```

The `getById` action returns a blue BMW with the `id` specified in its parameter.

### Future Works

Currently (as of January 2021), there is a thesis going on at Czech Technical University 
in Prague. Its main goal is to generate a frontend off of the API that can make use of all 
of its features and should allow for easy testing of the backend functionalities.
