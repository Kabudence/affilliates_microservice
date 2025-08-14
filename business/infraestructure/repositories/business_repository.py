from typing import Optional, List

from business.domain.entities.business import BusinessData
from business.infraestructure.model.business_model import BusinessModel


class BusinessRepository:
    def _to_entity(self, rec: BusinessModel) -> BusinessData:
        return BusinessData(
            id=rec.id,
            name=rec.name,
            ruc=rec.ruc,
            social_reasoning=rec.social_reasoning,
            direction=rec.direction,
            user_owner_id=rec.user_owner_id,
            district_id=rec.district_id,
            sector_id=rec.sector_id,
        )

    # CRUD
    def get_by_id(self, id_: int) -> Optional[BusinessData]:
        try:
            rec = BusinessModel.get(BusinessModel.id == id_)
            return self._to_entity(rec)
        except BusinessModel.DoesNotExist:
            return None

    def get_all(self) -> List[BusinessData]:
        return [self._to_entity(rec) for rec in BusinessModel.select()]

    def list_by_owner(self, user_owner_id: int) -> List[BusinessData]:
        q = BusinessModel.select().where(BusinessModel.user_owner_id == user_owner_id)
        return [self._to_entity(rec) for rec in q]

    def create(self, entity: BusinessData) -> BusinessData:
        rec = BusinessModel.create(
            name=entity.name,
            ruc=entity.ruc,
            social_reasoning=entity.social_reasoning,
            direction=entity.direction,
            user_owner_id=entity.user_owner_id,
            district_id=entity.district_id,
            sector_id=entity.sector_id,
        )
        return self._to_entity(rec)

    def update(self, entity: BusinessData) -> Optional[BusinessData]:
        try:
            rec = BusinessModel.get(BusinessModel.id == entity.id)
            rec.name = entity.name
            rec.ruc = entity.ruc
            rec.social_reasoning = entity.social_reasoning
            rec.direction = entity.direction
            rec.user_owner_id = entity.user_owner_id
            rec.district_id = entity.district_id
            rec.sector_id = entity.sector_id
            rec.save()
            return self._to_entity(rec)
        except BusinessModel.DoesNotExist:
            return None

    def delete(self, id_: int) -> bool:
        try:
            rec = BusinessModel.get(BusinessModel.id == id_)
            rec.delete_instance()
            return True
        except BusinessModel.DoesNotExist:
            return False

    def find_by_ruc(self, ruc: str) -> Optional[BusinessData]:
        if not ruc:
            return None
        try:
            rec = BusinessModel.get(BusinessModel.ruc == ruc.strip())
            return self._to_entity(rec)
        except BusinessModel.DoesNotExist:
            return None
