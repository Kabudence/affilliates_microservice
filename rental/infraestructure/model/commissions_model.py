import datetime

from peewee import Model, AutoField, IntegerField, FloatField, CharField, DateTimeField
from shared.infrastructure.database import db

class CommissionModel(Model):
    id               = AutoField(primary_key=True)
    user_id          = IntegerField(null=False)
    subscription_id  = IntegerField(null=True)
    amount           = FloatField(null=False)
    type             = CharField(
        max_length=20,
        null=False,
        default="direct",
        choices=[("direct", "direct"), ("referred", "referred")]
    )
    created_at = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'commissions'
        indexes    = (
            (('user_id', 'subscription_id'), False),
        )
