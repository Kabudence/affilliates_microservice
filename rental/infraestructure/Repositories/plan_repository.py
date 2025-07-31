from typing import Optional, List
from rental.domain.entities.plan import Plan
from rental.infraestructure.model.plan_model import PlanModel


class PlanRepository:
    def get_by_id(self, id: int) -> Optional[Plan]:
        try:
            record = PlanModel.get(PlanModel.id == id)
            return Plan(
                id=record.id,
                name=record.name,
                description=record.description,
                duration=record.duration,        # Nuevo campo
                price=record.price,
                app_id=record.app_id             # Nuevo campo
            )
        except PlanModel.DoesNotExist:
            return None

    def get_all(self) -> List[Plan]:
        return [
            Plan(
                id=rec.id,
                name=rec.name,
                description=rec.description,
                duration=rec.duration,
                price=rec.price,
                app_id=rec.app_id
            )
            for rec in PlanModel.select()
        ]

    def create(self, plan: Plan) -> Plan:
        record = PlanModel.create(
            name=plan.name,
            description=plan.description,
            duration=plan.duration,
            price=plan.price,
            app_id=plan.app_id
        )
        return Plan(
            id=record.id,
            name=record.name,
            description=record.description,
            duration=record.duration,
            price=record.price,
            app_id=record.app_id
        )

    def update(self, plan: Plan) -> Optional[Plan]:
        try:
            record = PlanModel.get(PlanModel.id == plan.id)
            record.name = plan.name
            record.description = plan.description
            record.duration = plan.duration
            record.price = plan.price
            record.app_id = plan.app_id
            record.save()
            return Plan(
                id=record.id,
                name=record.name,
                description=record.description,
                duration=record.duration,
                price=record.price,
                app_id=record.app_id
            )
        except PlanModel.DoesNotExist:
            return None

    def delete(self, plan_id: int) -> bool:
        try:
            record = PlanModel.get(PlanModel.id == plan_id)
            record.delete_instance()
            return True
        except PlanModel.DoesNotExist:
            return False

    def get_by_app_id(self, app_id: Optional[int] = None) -> List[Plan]:
        query = PlanModel.select()
        if app_id is not None:
            query = query.where(PlanModel.app_id == app_id)
        return [
            Plan(
                id=rec.id,
                name=rec.name,
                description=rec.description,
                duration=rec.duration,
                price=rec.price,
                app_id=rec.app_id
            )
            for rec in query
        ]
