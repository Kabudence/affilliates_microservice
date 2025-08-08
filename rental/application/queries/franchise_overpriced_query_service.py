# rental/application/queries/franchise_overpriced_query_service.py
from typing import Optional, List
from rental.domain.entities.franchise_overpriced import FranchiseOverpriced
from rental.infraestructure.Repositories.franchise_overpriced_repository import FranchiseOverpricedRepository


class FranchiseOverpricedQueryService:
    def __init__(self, repo: FranchiseOverpricedRepository):
        self.repo = repo

    def get_by_id(self, id_: int) -> Optional[FranchiseOverpriced]:
        return self.repo.get_by_id(id_)

    def list_all(self) -> List[FranchiseOverpriced]:
        return self.repo.get_all()

    def get_by_franchise_and_plan(self, franchise_id: int, plan_id: int) -> Optional[FranchiseOverpriced]:
        return self.repo.get_by_franchise_and_plan(franchise_id, plan_id)

    def list_by_franchise_id(self, franchise_id: int) -> List[FranchiseOverpriced]:
        return self.repo.list_by_franchise_id(franchise_id)
