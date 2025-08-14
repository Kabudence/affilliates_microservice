from typing import List, Optional

from business.domain.entities.business import BusinessData
from business.infraestructure.repositories.business_repository import BusinessRepository


class BusinessQueryService:
    def __init__(self, repo: BusinessRepository):
        self.repo = repo

    def get_by_id(self, id_: int) -> Optional[BusinessData]:
        return self.repo.get_by_id(id_)

    def list_all(self) -> List[BusinessData]:
        return self.repo.get_all()

    def list_by_owner(self, user_owner_id: int) -> List[BusinessData]:
        return self.repo.list_by_owner(user_owner_id)

    def find_by_ruc(self, ruc: str) -> Optional[BusinessData]:
        return self.repo.find_by_ruc(ruc)
