from peewee import (
    Model, AutoField, CharField, DateTimeField
)
from shared.infrastructure.database import db
from datetime import datetime

class DistrictModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)
    inscription_level = CharField(max_length=100, null=False)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        database = db
        table_name = 'districts'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super().save(*args, **kwargs)
