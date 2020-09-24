from django.db.models import Model, IntegerField, FloatField, CharField, TextField, BooleanField, DateField, TimeField, \
    DateTimeField


class TestModelPrimitiveFields(Model):
    int_field = IntegerField()
    float_field = FloatField()
    string_char_field = CharField(max_length=50)
    string_text_field = TextField()
    bool_field = BooleanField()
    date_field = DateField()
    time_field = TimeField()
    date_time_field = DateTimeField()
