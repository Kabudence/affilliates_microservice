# rental/infraestructure/Repositories/franchise_discount_repository.py
from typing import Optional, List

from rental.domain.entities.franchise_discount import FranchiseDiscount
from rental.infraestructure.model.franchise_discount_model import FranchiseDiscountModel


class FranchiseDiscountRepository:
    def get_by_id(self, id_: int) -> Optional[FranchiseDiscount]:
        try:
            rec = FranchiseDiscountModel.get(FranchiseDiscountModel.id == id_)
            return FranchiseDiscount(id=rec.id, percent=rec.percent, app_id=rec.app_id)
        except FranchiseDiscountModel.DoesNotExist:
            return None

    def get_all(self) -> List[FranchiseDiscount]:
        return [
            FranchiseDiscount(id=rec.id, percent=rec.percent, app_id=rec.app_id)
            for rec in FranchiseDiscountModel.select()
        ]

    def create(self, fd: FranchiseDiscount) -> FranchiseDiscount:
        rec = FranchiseDiscountModel.create(
            percent=fd.percent,
            app_id=fd.app_id,
        )
        return FranchiseDiscount(id=rec.id, percent=rec.percent, app_id=rec.app_id)

    def update(self, fd: FranchiseDiscount) -> Optional[FranchiseDiscount]:
        try:
            rec = FranchiseDiscountModel.get(FranchiseDiscountModel.id == fd.id)
            rec.percent = fd.percent
            rec.app_id  = fd.app_id
            rec.save()
            return FranchiseDiscount(id=rec.id, percent=rec.percent, app_id=rec.app_id)
        except FranchiseDiscountModel.DoesNotExist:
            return None

    def delete(self, id_: int) -> bool:
        try:
            rec = FranchiseDiscountModel.get(FranchiseDiscountModel.id == id_)
            rec.delete_instance()
            return True
        except FranchiseDiscountModel.DoesNotExist:
            return False

    def get_by_app_id(self, app_id: int) -> Optional[FranchiseDiscount]:
        try:
            rec = FranchiseDiscountModel.get(FranchiseDiscountModel.app_id == app_id)
            return FranchiseDiscount(id=rec.id, percent=rec.percent, app_id=rec.app_id)
        except FranchiseDiscountModel.DoesNotExist:
            return None
