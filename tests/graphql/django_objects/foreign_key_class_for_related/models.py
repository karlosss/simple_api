from django.db.models import Model, IntegerField, CharField, ForeignKey, OneToOneField, CASCADE


class TestModelFKTarget(Model):
    int_field = IntegerField()


class TestModelFKSource(Model):
    string_field = CharField(max_length=50)
    fk_field = ForeignKey(TestModelFKTarget, on_delete=CASCADE, related_name="fk_sources")
    one_to_one_field = OneToOneField(TestModelFKTarget, on_delete=CASCADE, related_name="one_to_one_rel")
