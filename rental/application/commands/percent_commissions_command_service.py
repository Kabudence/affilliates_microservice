from typing import Optional

from rental.domain.entities.percent_comissions import (
    PercentCommissions
)
from rental.infraestructure.Repositories.percent_commission_repository import PercentCommissionRepository
from rental.infraestructure.model.utilities.percent_commission_utils import validate_owner_and_percent, \
    coerce_commission_type


class PercentCommissionCommandService:
    def __init__(self, repo: PercentCommissionRepository):
        self.repo = repo

    def create(self, owner_id: int, percent: float, commission_type) -> PercentCommissions:
        validate_owner_and_percent(owner_id, percent)
        ct = coerce_commission_type(commission_type)
        return self.repo.create(PercentCommissions(owner_id=owner_id, percent=percent, commission_type=ct))

    def update(self, id_: int, owner_id: int, percent: float, commission_type) -> Optional[PercentCommissions]:
        current = self.repo.get_by_id(id_)
        if not current:
            raise ValueError("Percent commission not found")
        validate_owner_and_percent(owner_id, percent)
        ct = coerce_commission_type(commission_type)
        current.owner_id, current.percent, current.commission_type = owner_id, percent, ct
        return self.repo.update(current)


    def delete(self, percent_commission_id: int) -> bool:
        return self.repo.delete(percent_commission_id)
