from typing import Optional, List

from socioeconomic_distribution.domain.entities.inscription_level import InscriptionLevel
from socioeconomic_distribution.infraestructure.repository.inscription_level_repository import \
    InscriptionLevelRepository


class InscriptionLevelQueryService:
    def __init__(self, inscription_level_repo: InscriptionLevelRepository):
        self.inscription_level_repo = inscription_level_repo

    def get_by_id(self, inscription_level_id: int) -> Optional[InscriptionLevel]:
        if inscription_level_id is None or inscription_level_id <= 0:
            raise ValueError("ID de nivel de inscripción inválido.")
        return self.inscription_level_repo.get_by_id(inscription_level_id)

    def list_all(self) -> List[InscriptionLevel]:
        return self.inscription_level_repo.get_all()