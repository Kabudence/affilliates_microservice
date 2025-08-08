# commissions/infrastructure/repositories/percent_commission_repository.py
from typing import Optional, List

from rental.domain.entities.percent_comissions import PercentCommissions, CommissionType
from rental.infraestructure.model.percent_commissions_model import PercentCommissionModel


class PercentCommissionRepository:
    def get_by_id(self, id: int) -> Optional[PercentCommissions]:
        try:
            record = PercentCommissionModel.get(PercentCommissionModel.id == id)
            return PercentCommissions(
                id=record.id,
                percent=record.percent,
                owner_id=record.owner_id,
                commission_type=CommissionType(record.commission_type)
            )
        except PercentCommissionModel.DoesNotExist:
            return None

    def get_all(self) -> List[PercentCommissions]:
        return [
            PercentCommissions(
                id=rec.id,
                percent=rec.percent,
                owner_id=rec.owner_id,
                commission_type=CommissionType(rec.commission_type)
            )
            for rec in PercentCommissionModel.select()
        ]

    def create(self, commission: PercentCommissions) -> PercentCommissions:
        record = PercentCommissionModel.create(
            percent=commission.percent,
            owner_id=commission.owner_id,
            commission_type=commission.commission_type.value
        )
        return PercentCommissions(
            id=record.id,
            percent=record.percent,
            owner_id=record.owner_id,
            commission_type=CommissionType(record.commission_type)
        )

    def update(self, commission: PercentCommissions) -> Optional[PercentCommissions]:
        try:
            record = PercentCommissionModel.get(PercentCommissionModel.id == commission.id)
            record.percent = commission.percent
            record.owner_id = commission.owner_id
            record.commission_type = commission.commission_type.value
            record.save()
            return PercentCommissions(
                id=record.id,
                percent=record.percent,
                owner_id=record.owner_id,
                commission_type=CommissionType(record.commission_type)
            )
        except PercentCommissionModel.DoesNotExist:
            return None

    def delete(self, commission_id: int) -> bool:
        try:
            record = PercentCommissionModel.get(PercentCommissionModel.id == commission_id)
            record.delete_instance()
            return True
        except PercentCommissionModel.DoesNotExist:
            return False

    def get_by_owner_and_type(
        self, owner_id: int, commission_type: CommissionType
    ) -> Optional[PercentCommissions]:
        try:
            record = PercentCommissionModel.get(
                (PercentCommissionModel.owner_id == owner_id) &
                (PercentCommissionModel.commission_type == commission_type.value)
            )
            return PercentCommissions(
                id=record.id,
                percent=record.percent,
                owner_id=record.owner_id,
                commission_type=CommissionType(record.commission_type)
            )
        except PercentCommissionModel.DoesNotExist:
            return None

    def list_by_owner_id(self, owner_id: int) -> List[PercentCommissions]:
        q = PercentCommissionModel.select().where(PercentCommissionModel.owner_id == owner_id)
        return [
            PercentCommissions(
                id=r.id, percent=r.percent, owner_id=r.owner_id, commission_type=CommissionType(r.commission_type)
            ) for r in q
        ]