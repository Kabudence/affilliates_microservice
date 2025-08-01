from typing import List, Optional

from socioeconomic_distribution.domain.entities.district import District
from socioeconomic_distribution.infraestructure.model.district_model import DistrictModel


class DistrictRepository:
    def create(self, name: str, inscription_level_id: int) -> Optional[District]:
        try:
            district_model = DistrictModel.create(
                name=name,
                inscription_level_id=inscription_level_id
            )
            return District(
                id=district_model.id,
                name=district_model.name,
                inscription_level_id=district_model.inscription_level_id
            )
        except Exception as e:
            print(f"Error creating district: {e}")
            return None

    def get_by_id(self, district_id: int) -> Optional[District]:
        try:
            district_model = DistrictModel.get(DistrictModel.id == district_id)
            return District(
                id=district_model.id,
                name=district_model.name,
                inscription_level_id=district_model.inscription_level_id
            )
        except DistrictModel.DoesNotExist:
            return None

    def get_all(self) -> List[District]:
        districts = []
        for district_model in DistrictModel.select():
            districts.append(District(
                id=district_model.id,
                name=district_model.name,
                inscription_level_id=district_model.inscription_level_id
            ))
        return districts

    def update(self, district_id: int, name: Optional[str] = None, inscription_level_id: Optional[int] = None) -> bool:
        data = {}
        if name is not None:
            data['name'] = name
        if inscription_level_id is not None:
            data['inscription_level_id'] = inscription_level_id
        if not data:
            return False
        updated = DistrictModel.update(**data).where(DistrictModel.id == district_id).execute()
        return updated > 0

    def delete(self, district_id: int) -> bool:
        deleted = DistrictModel.delete().where(DistrictModel.id == district_id).execute()
        return deleted > 0
