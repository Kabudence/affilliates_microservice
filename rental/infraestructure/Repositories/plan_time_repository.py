from typing import Optional, List
from rental.domain.entities.plan_time import PlanTime
from rental.infraestructure.model.plan_time_model import PlanTimeModel

class PlanTimeRepository:
    def get_by_id(self, id: int) -> Optional[PlanTime]:
        try:
            record = PlanTimeModel.get(PlanTimeModel.id == id)
            return PlanTime(
                id=record.id,
                plan_id=record.plan_id,
                duration=record.duration,
                price=record.price
            )
        except PlanTimeModel.DoesNotExist:
            return None

    def get_by_plan_id(self, plan_id: int) -> List[PlanTime]:
        return [
            PlanTime(
                id=rec.id,
                plan_id=rec.plan_id,
                duration=rec.duration,
                price=rec.price
            )
            for rec in PlanTimeModel.select().where(PlanTimeModel.plan_id == plan_id)
        ]

    def create(self, plan_time: PlanTime) -> PlanTime:
        record = PlanTimeModel.create(
            plan_id=plan_time.plan_id,
            duration=plan_time.duration,
            price=plan_time.price
        )
        return PlanTime(
            id=record.id,
            plan_id=record.plan_id,
            duration=record.duration,
            price=record.price
        )

    def update(self, plan_time: PlanTime) -> Optional[PlanTime]:
        try:
            record = PlanTimeModel.get(PlanTimeModel.id == plan_time.id)
            record.plan_id = plan_time.plan_id
            record.duration = plan_time.duration
            record.price = plan_time.price
            record.save()
            return PlanTime(
                id=record.id,
                plan_id=record.plan_id,
                duration=record.duration,
                price=record.price
            )
        except PlanTimeModel.DoesNotExist:
            return None

    def delete(self, plan_time_id: int) -> bool:
        try:
            record = PlanTimeModel.get(PlanTimeModel.id == plan_time_id)
            record.delete_instance()
            return True
        except PlanTimeModel.DoesNotExist:
            return False
