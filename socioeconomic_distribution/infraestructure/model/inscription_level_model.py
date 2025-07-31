from peewee import (
    Model, AutoField, CharField, FloatField, DateTimeField
)
from shared.infrastructure.database import db
from datetime import datetime

class InscriptionLevelModel(Model):
    id = AutoField(primary_key=True)
    name_level = CharField(max_length=100, null=False)
    registration_cost = FloatField(null=False, default=0.0)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        database = db
        table_name = 'inscription_levels'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super().save(*args, **kwargs)
