from object.fields import IntegerField
from object.mixins import DetailMixin


def add_id_field(obj):
    if issubclass(obj, DetailMixin):
        if obj.id_field:
            obj.fields["id"] = IntegerField(nullable=False)


def generate(adapter, objs, extra_actions=None):
    for obj in objs:
        add_id_field(obj)

    return adapter(objs, extra_actions).generate()
