# rental/application/queries/franchise_discount_query_service.py
from typing import Optional, List
from rental.domain.entities.franchise_discount import FranchiseDiscount
from rental.infraestructure.Repositories.franchise_discount_repository import FranchiseDiscountRepository


class FranchiseDiscountQueryService:
    def __init__(self, repo: FranchiseDiscountRepository):
        self.repo = repo

    def get_by_id(self, id_: int) -> Optional[FranchiseDiscount]:
        return self.repo.get_by_id(id_)

    def list_all(self) -> List[FranchiseDiscount]:
        return self.repo.get_all()

    def get_by_app_id(self, app_id: int) -> Optional[FranchiseDiscount]:
        return self.repo.get_by_app_id(app_id)

