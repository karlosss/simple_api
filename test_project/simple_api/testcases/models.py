from django.db.models import Model, IntegerField, FloatField, CharField, TextField, DateField, TimeField, DateTimeField, \
    BooleanField, ForeignKey, CASCADE


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
    fk_field = ForeignKey(TestModelFKTarget, on_delete=CASCADE, related_name="sources")
