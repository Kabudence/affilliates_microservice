# rental/infraestructure/model/franchise_discount_model.py
import datetime
from peewee import Model, AutoField, IntegerField, FloatField, DateTimeField, Check
from shared.infrastructure.database import db

class FranchiseDiscountModel(Model):
    id         = AutoField(primary_key=True)
    percent    = FloatField(null=False, constraints=[Check('percent >= 0')])
    app_id     = IntegerField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now, null=False)

    class Meta:
        database   = db
        table_name = 'franchise_discounts'
        indexes    = (
            (('app_id',), False),  # cambia a True si quieres 1 descuento por app
        )
