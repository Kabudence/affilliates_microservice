from peewee import Model, AutoField, IntegerField, FloatField
from shared.infrastructure.database import db

class PlanTimeModel(Model):
    id       = AutoField(primary_key=True)
    plan_id  = IntegerField(null=False)
    duration = IntegerField(null=False)     # meses
    price    = FloatField(null=False)

    class Meta:
        database   = db
        table_name = 'plan_times'
        indexes    = (
            (('plan_id', 'duration'), True),
        )
