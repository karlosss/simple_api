from django.contrib.auth import get_user_model
from django.db.models import Model, TextField, ForeignKey, CASCADE


class Car(Model):
    manufacturer = TextField()
    owner = ForeignKey(get_user_model(), CASCADE)
