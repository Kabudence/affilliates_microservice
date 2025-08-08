# rental/infraestructure/model/goal_model.py
from peewee import Model, AutoField, IntegerField, FloatField
from shared.infrastructure.database import db

class GoalModel(Model):
    id                  = AutoField(primary_key=True)
    number_of_clients   = IntegerField(null=False)
    month               = IntegerField(null=False)   # 1..12
    percentage_to_bonus = FloatField(null=False)
    owner_id            = IntegerField(null=False)

    class Meta:
        database   = db
        table_name = 'goals'
        indexes    = (
            (('month',), False),
            (('owner_id', 'month'), False),  # cambia a True si quieres 1 goal por owner/mes
        )
