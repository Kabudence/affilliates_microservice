from typing import List, Optional

from socioeconomic_distribution.domain.entities.inscription_level import InscriptionLevel
from socioeconomic_distribution.infraestructure.model.inscription_level_model import InscriptionLevelModel


class InscriptionLevelRepository:
    def create(self, name_level: str, registration_cost: float) -> Optional[InscriptionLevel]:
        try:
            il_model = InscriptionLevelModel.create(
                name_level=name_level,
                registration_cost=registration_cost
            )
            return InscriptionLevel(
                id=il_model.id,
                name_level=il_model.name_level,
                registration_cost=il_model.registration_cost
            )
        except Exception as e:
            print(f"Error creating InscriptionLevel: {e}")
            return None

    def get_by_id(self, inscription_level_id: int) -> Optional[InscriptionLevel]:
        try:
            il_model = InscriptionLevelModel.get(InscriptionLevelModel.id == inscription_level_id)
            return InscriptionLevel(
                id=il_model.id,
                name_level=il_model.name_level,
                registration_cost=il_model.registration_cost
            )
        except InscriptionLevelModel.DoesNotExist:
            return None

    def get_all(self) -> List[InscriptionLevel]:
        return [
            InscriptionLevel(
                id=il.id,
                name_level=il.name_level,
                registration_cost=il.registration_cost
            )
            for il in InscriptionLevelModel.select()
        ]

    def update(self, inscription_level_id: int, name_level: Optional[str] = None, registration_cost: Optional[float] = None) -> bool:
        data = {}
        if name_level is not None:
            data['name_level'] = name_level
        if registration_cost is not None:
            data['registration_cost'] = registration_cost
        if not data:
            return False
        updated = InscriptionLevelModel.update(**data).where(InscriptionLevelModel.id == inscription_level_id).execute()
        return updated > 0

    def delete(self, inscription_level_id: int) -> bool:
        deleted = InscriptionLevelModel.delete().where(InscriptionLevelModel.id == inscription_level_id).execute()
        return deleted > 0
