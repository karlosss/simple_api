from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.actions import CreateAction, UpdateAction
from django_object.django_object import DjangoObject
from django_object.permissions import IsAuthenticated
from object.permissions import AllowNone
from tests.graphql.graphql_test_utils import build_patterns

from .models import Exhaust as ExhaustModel, Car as CarModel, Wheel as WheelModel, Manufacturer as ManufacturerModel


class Manufacturer(DjangoObject):
    model = ManufacturerModel


class Exhaust(DjangoObject):
    model = ExhaustModel


class Car(DjangoObject):
    model = CarModel
    auto_pk = False


class Wheel(DjangoObject):
    model = WheelModel
    # create_action = CreateAction(permissions=AllowNone)
    update_action = UpdateAction(permissions=IsAuthenticated)
    # field_validators = {
    #     "manufacturer_id": lambda *a, **kw: ManufacturerModel.objects.none()
    # }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
