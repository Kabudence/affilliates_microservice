from rental.domain.entities.plan_time import PlanTime
from rental.infraestructure.Repositories.plan_time_repository import PlanTimeRepository

class PlanTimeCommandService:
    def __init__(self, plan_time_repo: PlanTimeRepository):
        self.plan_time_repo = plan_time_repo

    def create(self, plan_id: int, duration: int, price: float) -> PlanTime:
        plan_time = PlanTime(plan_id=plan_id, duration=duration, price=price)
        return self.plan_time_repo.create(plan_time)

    def update(self, plan_time_id: int, duration: int, price: float) -> PlanTime:
        plan_time = self.plan_time_repo.get_by_id(plan_time_id)
        if not plan_time:
            raise ValueError("PlanTime not found.")
        plan_time.duration = duration
        plan_time.price = price
        return self.plan_time_repo.update(plan_time)

    def delete(self, plan_time_id: int) -> bool:
        return self.plan_time_repo.delete(plan_time_id)


