from peewee import (
    Model, AutoField, CharField, FloatField, DateTimeField, TimestampField
)
from shared.infrastructure.database import db
import datetime

class InscriptionLevelModel(Model):
    id = AutoField(primary_key=True)
    name_level = CharField(max_length=100, null=False)
    registration_cost = FloatField(null=False, default=0.0)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)
    updated_at = DateTimeField(default=datetime.datetime.now, null=False)  # ← sin auto_now

    class Meta:
        database = db
        table_name = 'inscription_levels'


