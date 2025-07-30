import enum
from peewee import Model, AutoField, CharField, DateTimeField
from shared.infrastructure.database import db

class ApplicationType(enum.Enum):
    EMPRENDEX = "emprendex"
    FULLVENTASGYM = "fullventasgym"

class ApplicationModel(Model):
    id               = AutoField(primary_key=True)
    name             = CharField(null=False)
    description      = CharField(null=False)
    application_type = CharField(
        max_length=32,
        null=False,
        choices=[(e.value, e.value) for e in ApplicationType]
    )
    created_at       = DateTimeField(constraints=[db.SQL("DEFAULT CURRENT_TIMESTAMP")], null=False)
    updated_at       = DateTimeField(constraints=[db.SQL(
        "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")], null=False)

    class Meta:
        database   = db
        table_name = 'applications'
