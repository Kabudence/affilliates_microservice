from peewee import (
    Model, AutoField, IntegerField, DateTimeField
)
from shared.infrastructure.database import db

class UserModel(Model):
    id         = AutoField(primary_key=True)
    account_id = IntegerField(null=False)
    app_id     = IntegerField(null=False)
    created_at = DateTimeField(constraints=[db.SQL("DEFAULT CURRENT_TIMESTAMP")], null=False)
    updated_at = DateTimeField(constraints=[db.SQL(
        "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")], null=False)

    class Meta:
        database   = db
        table_name = 'users'
        # Puedes agregar un índice si es necesario
        indexes    = (
            (('account_id', 'app_id'), False),
        )
