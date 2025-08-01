import datetime

from peewee import Model, AutoField, CharField, DateTimeField, TimestampField

from application.domain.entities.application_data import ApplicationType
from shared.infrastructure.database import db


class ApplicationModel(Model):
    id               = AutoField(primary_key=True)
    name             = CharField(null=False)
    description      = CharField(null=False)
    application_type = CharField(
        max_length=32,
        null=False,
        choices=[(e.value, e.value) for e in ApplicationType]
    )
    created_at = DateTimeField(default=datetime.datetime.now, null=False)
    updated_at = DateTimeField(default=datetime.datetime.now, null=False)  # ← sin auto_now

    class Meta:
        database   = db
        table_name = 'applications'
