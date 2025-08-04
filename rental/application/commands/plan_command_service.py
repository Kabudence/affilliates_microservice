from rental.domain.entities.plan import Plan, PlanType
from rental.infraestructure.Repositories.module_plan_repository import PlanModuleRepository
from rental.infraestructure.Repositories.plan_repository import PlanRepository
from rental.infraestructure.Repositories.plan_time_repository import PlanTimeRepository
from rental.domain.entities.plan_time import PlanTime

class PlanCommandService:
    def __init__(self, plan_repo: PlanRepository, plan_module_repo: PlanModuleRepository, plan_time_repo: PlanTimeRepository):
        self.plan_repo = plan_repo
        self.plan_module_repo = plan_module_repo
        self.plan_time_repo = plan_time_repo

    def create(self, name: str, description: str, app_id: int, plan_type: PlanType, ids_modules: list[int], times: list[dict]) -> Plan:
        if not name or not description or app_id is None or plan_type is None or not times:
            raise ValueError("All fields are required (except modules).")
        plan = Plan(
            name=name,
            description=description,
            app_id=app_id,
            plan_type=plan_type
        )
        plan = self.plan_repo.create(plan)
        for module_id in ids_modules:
            self.plan_module_repo.add_module_to_plan(plan.id, module_id)
        for t in times:
            plan_time = PlanTime(
                plan_id=plan.id,
                duration=t["duration"],
                price=t["price"]
            )
            self.plan_time_repo.create(plan_time)
        return plan

    def update(self, plan_id: int, name: str, description: str, app_id: int, plan_type: PlanType, ids_modules: list[int] = None, times: list[dict] = None) -> Plan:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found.")
        plan.name = name
        plan.description = description
        plan.app_id = app_id
        plan.plan_type = plan_type
        updated_plan = self.plan_repo.update(plan)

        if ids_modules is not None:
            self.plan_module_repo.remove_all_modules_from_plan(plan_id)
            for module_id in ids_modules:
                self.plan_module_repo.add_module_to_plan(plan_id, module_id)

        if times is not None:
            self.plan_time_repo.delete_by_plan_id(plan_id)
            for t in times:
                plan_time = PlanTime(
                    plan_id=plan_id,
                    duration=t["duration"],
                    price=t["price"]
                )
                self.plan_time_repo.create(plan_time)

        return updated_plan

    def delete(self, plan_id: int) -> bool:
        self.plan_time_repo.delete_by_plan_id(plan_id)
        self.plan_module_repo.remove_all_modules_from_plan(plan_id)
        return self.plan_repo.delete(plan_id)

    def get_by_id(self, plan_id: int) -> Plan:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found.")
        return plan
