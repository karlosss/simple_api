from django.contrib.auth import get_user_model
from django.db.models import Model, TextField, ForeignKey, CASCADE, BooleanField


class Car(Model):
    number_plate = TextField()
    locked = BooleanField(default=False)
    owner = ForeignKey(get_user_model(), CASCADE)
