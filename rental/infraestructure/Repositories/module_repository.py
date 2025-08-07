from typing import Optional, List

from rental.domain.entities.module import Module
from rental.infraestructure.model.module_model import ModuleModel
from rental.infraestructure.model.plan_model import PlanModuleModel


class ModuleRepository:
    def get_by_id(self, id: int) -> Optional[Module]:
        try:
            record = ModuleModel.get(ModuleModel.id == id)
            return Module(
                id=record.id,
                name=record.name,
                description=record.description
            )
        except ModuleModel.DoesNotExist:
            return None

    def get_all(self) -> List[Module]:
        return [
            Module(
                id=rec.id,
                name=rec.name,
                description=rec.description
            )
            for rec in ModuleModel.select()
        ]

    def create(self, module: Module) -> Module:
        record = ModuleModel.create(
            name=module.name,
            description=module.description
        )
        return Module(
            id=record.id,
            name=record.name,
            description=record.description
        )

    def update(self, module: Module) -> Optional[Module]:
        try:
            record = ModuleModel.get(ModuleModel.id == module.id)
            record.name = module.name
            record.description = module.description
            record.save()
            return Module(
                id=record.id,
                name=record.name,
                description=record.description
            )
        except ModuleModel.DoesNotExist:
            return None

    def delete(self, module_id: int) -> bool:
        try:
            record = ModuleModel.get(ModuleModel.id == module_id)
            record.delete_instance()
            return True
        except ModuleModel.DoesNotExist:
            return False

    def get_modules_by_plan_id(self, plan_id: int) -> List[Module]:
        print(f"[get_modules_by_plan_id] Recibido plan_id: {plan_id}")

        query = (
            ModuleModel
            .select()
            .join(
                PlanModuleModel,
                on=(ModuleModel.id == PlanModuleModel.module_id)
            )
            .where(PlanModuleModel.plan_id == plan_id)
        )

        modules_list = [
            Module(id=mod.id, name=mod.name, description=mod.description)
            for mod in query
        ]

        print(f"[get_modules_by_plan_id] Módulos encontrados ({len(modules_list)}):")
        for m in modules_list:
            print(f"  - id: {m.id}, name: {m.name}, description: {m.description}")

        return modules_list
