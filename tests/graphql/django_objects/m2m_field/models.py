from django.db.models import Model, IntegerField, ManyToManyField


class TestModelM2MTarget(Model):
    int_field = IntegerField()


class TestModelM2MSource(Model):
    m2m_field = ManyToManyField(TestModelM2MTarget, related_name="m2m_sources")
