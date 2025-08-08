# rental/infraestructure/Repositories/franchise_overpriced_repository.py
from typing import Optional, List

from rental.domain.entities.franchise_overpriced import FranchiseOverpriced
from rental.infraestructure.model.franchise_overpriced_model import FranchiseOverpricedModel


class FranchiseOverpricedRepository:
    def get_by_id(self, id_: int) -> Optional[FranchiseOverpriced]:
        try:
            r = FranchiseOverpricedModel.get(FranchiseOverpricedModel.id == id_)
            return FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)
        except FranchiseOverpricedModel.DoesNotExist:
            return None

    def get_all(self) -> List[FranchiseOverpriced]:
        return [
            FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)
            for r in FranchiseOverpricedModel.select()
        ]

    def create(self, fo: FranchiseOverpriced) -> FranchiseOverpriced:
        r = FranchiseOverpricedModel.create(
            extra_price=fo.extra_price,
            franchise_id=fo.franchise_id,
            plan_id=fo.plan_id,
        )
        return FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)

    def update(self, fo: FranchiseOverpriced) -> Optional[FranchiseOverpriced]:
        try:
            r = FranchiseOverpricedModel.get(FranchiseOverpricedModel.id == fo.id)
            r.extra_price  = fo.extra_price
            r.franchise_id = fo.franchise_id
            r.plan_id      = fo.plan_id
            r.save()
            return FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)
        except FranchiseOverpricedModel.DoesNotExist:
            return None

    def delete(self, id_: int) -> bool:
        try:
            r = FranchiseOverpricedModel.get(FranchiseOverpricedModel.id == id_)
            r.delete_instance()
            return True
        except FranchiseOverpricedModel.DoesNotExist:
            return False

    # === Extras solicitados ===
    def get_by_franchise_and_plan(self, franchise_id: int, plan_id: int) -> Optional[FranchiseOverpriced]:
        try:
            r = FranchiseOverpricedModel.get(
                (FranchiseOverpricedModel.franchise_id == franchise_id) &
                (FranchiseOverpricedModel.plan_id == plan_id)
            )
            return FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)
        except FranchiseOverpricedModel.DoesNotExist:
            return None

    def list_by_franchise_id(self, franchise_id: int) -> List[FranchiseOverpriced]:
        q = FranchiseOverpricedModel.select().where(FranchiseOverpricedModel.franchise_id == franchise_id)
        return [
            FranchiseOverpriced(id=r.id, extra_price=r.extra_price, franchise_id=r.franchise_id, plan_id=r.plan_id)
            for r in q
        ]
