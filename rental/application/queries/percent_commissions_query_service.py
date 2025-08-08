# commissions/application/queries/percent_commission_query_service.py
from typing import Optional, List
from rental.domain.entities.percent_comissions import PercentCommissions, CommissionType
from rental.infraestructure.Repositories.percent_commission_repository import PercentCommissionRepository
from rental.infraestructure.model.utilities.percent_commission_utils import coerce_commission_type


class PercentCommissionQueryService:
    def __init__(self, repo: PercentCommissionRepository):
        self.repo = repo

    def get_by_id(self, id_: int) -> Optional[PercentCommissions]:
        return self.repo.get_by_id(id_)

    def list_all(self) -> List[PercentCommissions]:
        return self.repo.get_all()

    def list_by_owner_id(self, owner_id: int) -> List[PercentCommissions]:
        return self.repo.list_by_owner_id(owner_id)

    def get_by_owner_and_type(self, owner_id: int, commission_type) -> Optional[PercentCommissions]:
        return self.repo.get_by_owner_and_type(owner_id, coerce_commission_type(commission_type))
