from peewee import (
    Model, AutoField, CharField, BigIntegerField
)
from shared.infrastructure.database import db


class BusinessModel(Model):
    id = AutoField(primary_key=True)

    # Core
    name = CharField(max_length=150, null=False)
    ruc = CharField(max_length=11, null=False, unique=True)          # Peru RUC
    social_reasoning = CharField(max_length=255, null=False)         # legal name
    direction = CharField(max_length=255, null=False)                # address

    # Ownership (no FK)
    user_owner_id = BigIntegerField(null=False)                      # owner user id (no FK)

    # Optional references (no FK)
    district_id = BigIntegerField(null=True)
    sector_id = BigIntegerField(null=True)

    class Meta:
        database = db
        table_name = 'business'
        indexes = (
            (('user_owner_id',), False),     # filter by owner
        )
