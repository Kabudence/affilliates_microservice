# rental/infraestructure/model/franchise_config_model.py
import datetime
from peewee import Model, AutoField, IntegerField, BooleanField, DateTimeField, Check
from shared.infrastructure.database import db

class FranchiseConfigModel(Model):
    id                   = AutoField(primary_key=True)
    franchise_owner_id   = IntegerField(null=False, constraints=[Check('franchise_owner_id > 0')])
    activate_commissions = BooleanField(default=False, null=False)
    created_at           = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'franchise_configs'
        indexes    = (
            # asumiendo 1 config por franquicia:
            (('franchise_owner_id',), True),
        )
