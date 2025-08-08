# rental/application/queries/franchise_config_query_service.py
from typing import Optional, List
from rental.domain.entities.franchise_config import FranchiseConfig
from rental.infraestructure.Repositories.franchise_config_repository import FranchiseConfigRepository


class FranchiseConfigQueryService:
    def __init__(self, repo: FranchiseConfigRepository):
        self.repo = repo

    def get_by_id(self, id_: int) -> Optional[FranchiseConfig]:
        return self.repo.get_by_id(id_)

    def list_all(self) -> List[FranchiseConfig]:
        return self.repo.get_all()

    def get_by_franchise_owner_id(self, franchise_owner_id: int) -> Optional[FranchiseConfig]:
        return self.repo.get_by_franchise_owner_id(franchise_owner_id)
