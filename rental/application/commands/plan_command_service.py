

from rental.domain.entities.plan import Plan
from rental.infraestructure.Repositories.module_plan_repository import PlanModuleRepository
from rental.infraestructure.Repositories.plan_repository import PlanRepository

class PlanCommandService:
    def __init__(self, plan_repo: PlanRepository, plan_module_repo: PlanModuleRepository):
        self.plan_repo = plan_repo
        self.plan_module_repo = plan_module_repo

    def create(self, name: str, description: str, duration: int, price: float, app_id: int, ids_modules: list[int]) -> Plan:
        if not name or not description or duration is None or price is None or app_id is None:
            raise ValueError("All fields are required.")
        plan = Plan(
            name=name,
            description=description,
            duration=duration,
            price=price,
            app_id=app_id
        )
        plan = self.plan_repo.create(plan)
        for module_id in ids_modules:
            self.plan_module_repo.add_module_to_plan(plan.id, module_id)

        return plan

    def update(self, plan_id: int, name: str, description: str, duration: int, price: float, app_id: int, ids_modules: list[int] = None) -> Plan:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found.")
        plan.name = name
        plan.description = description
        plan.duration = duration
        plan.price = price
        plan.app_id = app_id
        updated_plan = self.plan_repo.update(plan)

        if ids_modules is not None:
            self.plan_module_repo.remove_all_modules_from_plan(plan_id)
            for module_id in ids_modules:
                self.plan_module_repo.add_module_to_plan(plan_id, module_id)

        return updated_plan

    def delete(self, plan_id: int) -> bool:
        return self.plan_repo.delete(plan_id)
