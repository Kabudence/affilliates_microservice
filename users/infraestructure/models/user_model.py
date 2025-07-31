from peewee import (
    Model, AutoField, IntegerField, CharField, DateTimeField
)
from shared.infrastructure.database import db

class UserModel(Model):
    id             = AutoField(primary_key=True)
    account_id     = IntegerField(null=False)
    app_id         = IntegerField(null=False)
    user_owner_id  = IntegerField(null=True)
    user_type      = CharField(null=False)
    created_at     = DateTimeField(constraints=[db.SQL("DEFAULT CURRENT_TIMESTAMP")], null=False)
    updated_at     = DateTimeField(constraints=[db.SQL(
        "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")], null=False)

    class Meta:
        database   = db
        table_name = 'users'
        indexes    = (
            (('account_id', 'app_id'), False),
        )
