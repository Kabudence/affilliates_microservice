# rental/infraestructure/model/franchise_overpriced_model.py
import datetime
from peewee import Model, AutoField, IntegerField, FloatField, DateTimeField, Check
from shared.infrastructure.database import db

class FranchiseOverpricedModel(Model):
    id            = AutoField(primary_key=True)
    extra_price   = FloatField(null=False, constraints=[Check('extra_price >= 0')])
    franchise_id  = IntegerField(null=True)  # puede ser None según tu entidad
    plan_id       = IntegerField(null=True)  # puede ser None según tu entidad
    created_at    = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'franchise_overpriced'
        indexes    = (
            # Si quieres 1 registro por (franchise_id, plan_id) hazlo único=True
            (('franchise_id', 'plan_id'), True),
            (('franchise_id',), False),
        )
