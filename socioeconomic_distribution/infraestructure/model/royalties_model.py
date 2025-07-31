from peewee import Model, AutoField, IntegerField, FloatField, DateTimeField
from shared.infrastructure.database import db
from datetime import datetime

class RoyaltiesModel(Model):
    id = AutoField(primary_key=True)
    inscription_level_id = IntegerField(null=False)
    cost = FloatField(null=False)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        database = db
        table_name = 'royalties'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super().save(*args, **kwargs)
