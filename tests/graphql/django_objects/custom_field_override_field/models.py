from django.db.models import Model, IntegerField, TextField


class TestModel(Model):
    int_field = IntegerField()
    string_field = TextField()

    @property
    def int_plus_one(self):
        return self.int_field + 1
