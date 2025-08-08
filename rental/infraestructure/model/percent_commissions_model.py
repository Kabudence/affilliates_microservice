# commissions/infrastructure/models/percent_commission_model.py
import datetime
from peewee import (
    Model, AutoField, IntegerField, FloatField, DateTimeField, CharField, Check
)

from rental.domain.entities.percent_comissions import CommissionType
from shared.infrastructure.database import db


class PercentCommissionModel(Model):
    id              = AutoField(primary_key=True)
    owner_id        = IntegerField(null=False)
    percent         = FloatField(null=False, constraints=[Check('percent >= 0')])
    commission_type = CharField(
        max_length=20,
        default=CommissionType.APPLICATION.value,
        choices=[(ct.value, ct.value) for ct in CommissionType],
        null=False
    )
    created_at      = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'percent_commissions'
        indexes    = (
            # ÚNICO por dueño y tipo de comisión (cambia a False si quieres permitir múltiples registros)
            (('owner_id', 'commission_type'), True),
        )
