from typing import List, Optional

from socioeconomic_distribution.domain.entities.district import District
from socioeconomic_distribution.infraestructure.model.district_model import DistrictModel


class DistrictRepository:
    def create(self, name: str, inscription_level: str) -> Optional[District]:
        try:
            district_model = DistrictModel.create(name=name, inscription_level=inscription_level)
            return District(
                id=district_model.id,
                name=district_model.name,
                inscription_level=district_model.inscription_level
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
                inscription_level=district_model.inscription_level
            )
        except DistrictModel.DoesNotExist:
            return None

    def get_all(self) -> List[District]:
        districts = []
        for district_model in DistrictModel.select():
            districts.append(District(
                id=district_model.id,
                name=district_model.name,
                inscription_level=district_model.inscription_level
            ))
        return districts

    def update(self, district_id: int, name: Optional[str] = None, inscription_level: Optional[str] = None) -> bool:
        data = {}
        if name is not None:
            data['name'] = name
        if inscription_level is not None:
            data['inscription_level'] = inscription_level
        if not data:
            return False
        updated = DistrictModel.update(**data).where(DistrictModel.id == district_id).execute()
        return updated > 0

    def delete(self, district_id: int) -> bool:
        deleted = DistrictModel.delete().where(DistrictModel.id == district_id).execute()
        return deleted > 0
