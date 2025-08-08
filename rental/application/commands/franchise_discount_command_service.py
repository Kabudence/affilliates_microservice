# rental/application/commands/franchise_discount_command_service.py
from typing import Optional
from rental.domain.entities.franchise_discount import FranchiseDiscount
from rental.infraestructure.Repositories.franchise_discount_repository import FranchiseDiscountRepository


class FranchiseDiscountCommandService:
    def __init__(self, repo: FranchiseDiscountRepository):
        self.repo = repo

    def create(self, percent: float, app_id: int) -> FranchiseDiscount:
        if percent is None or app_id is None:
            raise ValueError("percent and app_id are required")
        if percent < 0:
            raise ValueError("percent must be >= 0")

        entity = FranchiseDiscount(percent=percent, app_id=app_id)
        return self.repo.create(entity)

    def update(self, id_: int, percent: float, app_id: int) -> Optional[FranchiseDiscount]:
        current = self.repo.get_by_id(id_)
        if not current:
            raise ValueError("FranchiseDiscount not found")

        if percent is None or app_id is None:
            raise ValueError("percent and app_id are required")
        if percent < 0:
            raise ValueError("percent must be >= 0")

        current.percent = percent
        current.app_id  = app_id
        return self.repo.update(current)

    def delete(self, id_: int) -> bool:
        return self.repo.delete(id_)
