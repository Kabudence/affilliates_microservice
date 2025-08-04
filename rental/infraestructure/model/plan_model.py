import datetime
from peewee import Model, AutoField, CharField, IntegerField, DateTimeField

from rental.domain.entities.plan import PlanType
from shared.infrastructure.database import db

class PlanModel(Model):
    id          = AutoField(primary_key=True)
    name        = CharField(null=False)
    description = CharField(null=False)
    app_id      = IntegerField(null=False)
    plan_type   = CharField(
        max_length=32,
        null=False,
        choices=[(plan_type.value, plan_type.value) for plan_type in PlanType]
    )
    created_at  = DateTimeField(default=datetime.datetime.now, null=False)
    updated_at  = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'plans'
        indexes    = (
            (('name',), False),
        )


from peewee import Model, IntegerField, CompositeKey

class PlanModuleModel(Model):
    plan_id   = IntegerField()
    module_id = IntegerField()

    class Meta:
        database    = db
        table_name  = 'plan_modules'
        primary_key = CompositeKey('plan_id', 'module_id')
        indexes     = (
            (('plan_id', 'module_id'), True),
        )
