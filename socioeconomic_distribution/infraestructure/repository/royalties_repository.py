from typing import Optional, List
from socioeconomic_distribution.domain.entities.royalties import Royalties
from socioeconomic_distribution.infraestructure.model.royalties_model import RoyaltiesModel

class RoyaltiesRepository:
    def create(self, inscription_level_id: int, cost: float) -> Royalties:
        record = RoyaltiesModel.create(
            inscription_level_id=inscription_level_id,
            cost=cost
        )
        return Royalties(
            id=record.id,
            inscription_level_id=record.inscription_level_id,
            cost=record.cost
        )

    def get_by_id(self, id: int) -> Optional[Royalties]:
        record = RoyaltiesModel.get_or_none(RoyaltiesModel.id == id)
        if not record:
            return None
        return Royalties(
            id=record.id,
            inscription_level_id=record.inscription_level_id,
            cost=record.cost
        )

    def list_all(self) -> List[Royalties]:
        return [
            Royalties(
                id=rec.id,
                inscription_level_id=rec.inscription_level_id,
                cost=rec.cost
            ) for rec in RoyaltiesModel.select()
        ]

    def update(self, id: int, inscription_level_id: Optional[int] = None, cost: Optional[float] = None) -> Optional[Royalties]:
        record = RoyaltiesModel.get_or_none(RoyaltiesModel.id == id)
        if not record:
            return None
        if inscription_level_id is not None:
            record.inscription_level_id = inscription_level_id
        if cost is not None:
            record.cost = cost
        record.save()
        return Royalties(
            id=record.id,
            inscription_level_id=record.inscription_level_id,
            cost=record.cost
        )

    def delete(self, id: int) -> bool:
        record = RoyaltiesModel.get_or_none(RoyaltiesModel.id == id)
        if not record:
            return False
        record.delete_instance()
        return True
