# rental/application/commands/franchise_overpriced_command_service.py
from typing import Optional
from rental.domain.entities.franchise_overpriced import FranchiseOverpriced
from rental.infraestructure.Repositories.franchise_overpriced_repository import FranchiseOverpricedRepository


class FranchiseOverpricedCommandService:
    def __init__(self, repo: FranchiseOverpricedRepository):
        self.repo = repo

    @staticmethod
    def _validate_parameters(extra_price: float, franchise_id: Optional[int], plan_id: Optional[int]) -> None:
        if extra_price is None:
            raise ValueError("extra_price is required")
        if extra_price < 0:
            raise ValueError("extra_price must be >= 0")
        if franchise_id is not None and franchise_id <= 0:
            raise ValueError("franchise_id must be positive if provided")
        if plan_id is not None and plan_id <= 0:
            raise ValueError("plan_id must be positive if provided")


    def create(self, extra_price: float, franchise_id: Optional[int], plan_id: Optional[int]) -> FranchiseOverpriced:
        self._validate_parameters(extra_price, franchise_id, plan_id)
        entity = FranchiseOverpriced(extra_price=extra_price, franchise_id=franchise_id, plan_id=plan_id)
        return self.repo.create(entity)

    def update(self, id_: int, extra_price: float, franchise_id: Optional[int], plan_id: Optional[int]) -> Optional[FranchiseOverpriced]:
        current = self.repo.get_by_id(id_)
        if not current:
            raise ValueError("FranchiseOverpriced not found")

        self._validate_parameters(extra_price, franchise_id, plan_id)

        current.extra_price  = extra_price
        current.franchise_id = franchise_id
        current.plan_id      = plan_id
        return self.repo.update(current)

    def delete(self, id_: int) -> bool:
        return self.repo.delete(id_)
