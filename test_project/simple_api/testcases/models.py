from django.db.models import Model, IntegerField, FloatField, CharField, TextField, DateField, TimeField, DateTimeField, \
    BooleanField, ForeignKey, CASCADE, ManyToManyField, OneToOneField


class TestModelPrimitiveFields(Model):
    int_field = IntegerField()
    float_field = FloatField()
    string_char_field = CharField(max_length=50)
    string_text_field = TextField()
    bool_field = BooleanField()
    date_field = DateField()
    time_field = TimeField()
    date_time_field = DateTimeField()


class TestModelFKTarget(Model):
    int_field = IntegerField()

    
class TestModelFKSource(Model):
    fk_field = ForeignKey(TestModelFKTarget, on_delete=CASCADE, related_name="fk_sources")
    one_to_one_field = OneToOneField(TestModelFKTarget, on_delete=CASCADE)


class TestModelM2MTarget(Model):
    int_field = IntegerField()


class TestModelM2MSource(Model):
    m2m_field = ManyToManyField(TestModelM2MTarget, related_name="m2m_sources")

