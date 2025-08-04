from typing import List, Optional
from rental.domain.entities.plan_time import PlanTime
from rental.infraestructure.Repositories.plan_time_repository import PlanTimeRepository

class PlanTimeQueryService:
    def __init__(self, plan_time_repo: PlanTimeRepository):
        self.plan_time_repo = plan_time_repo

    def get_by_id(self, plan_time_id: int) -> Optional[PlanTime]:
        return self.plan_time_repo.get_by_id(plan_time_id)

    def list_by_plan_id(self, plan_id: int) -> List[PlanTime]:
        return self.plan_time_repo.get_by_plan_id(plan_id)
