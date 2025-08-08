from peewee import Model, AutoField, IntegerField, FloatField, CharField
from shared.infrastructure.database import db

class GoalModel(Model):
    id                  = AutoField(primary_key=True)
    number_of_clients   = IntegerField(null=False)
    month               = IntegerField(null=False)   # 1..12
    percentage_to_bonus = FloatField(null=False)
    owner_id            = IntegerField(null=False)
    goal_type           = CharField(max_length=32, null=False)  # Enum como string

    class Meta:
      database   = db
      table_name = 'goals'
      indexes    = (
          (('month',), False),
          (('owner_id', 'month'), False),
          (('owner_id', 'goal_type'), False),  # útil para la búsqueda por owner+tipo
      )
