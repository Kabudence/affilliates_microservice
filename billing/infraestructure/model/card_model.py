from peewee import (
    Model, AutoField, CharField, IntegerField, DateTimeField
)
from shared.infrastructure.database import db
from datetime import datetime

class CardModel(Model):
    id = AutoField(primary_key=True)
    number = CharField(max_length=20, null=False)
    expiration_date = CharField(max_length=7, null=False)
    cvv = CharField(max_length=4, null=False)
    user_id = IntegerField(null=False)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        database = db
        table_name = 'cards'
        indexes = (
            (('user_id', 'number'), True),   # impide que un mismo usuario duplique el nº de tarjeta
        )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super().save(*args, **kwargs)
