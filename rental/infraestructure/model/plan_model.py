import datetime

from peewee import Model, AutoField, CharField, FloatField, IntegerField, CompositeKey, DateTimeField
from shared.infrastructure.database import db

class PlanModel(Model):
    id          = AutoField(primary_key=True)
    name        = CharField(null=False)
    description = CharField(null=False)
    duration    = IntegerField(null=False)       # Nuevo campo
    price       = FloatField(null=False)
    app_id      = IntegerField(null=False)       # Nuevo campo
    created_at = DateTimeField(default=datetime.datetime.now, null=False)
    updated_at = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'plans'
        indexes    = (
            (('name',), False),  # Puedes poner True si quieres que name sea único
        )

class PlanModuleModel(Model):
    plan_id   = IntegerField()
    module_id = IntegerField()

    class Meta:
        database    = db
        table_name  = 'plan_modules'
        primary_key = CompositeKey('plan_id', 'module_id')
        indexes     = (
            (('plan_id', 'module_id'), True),  # Índice único compuesto
        )
