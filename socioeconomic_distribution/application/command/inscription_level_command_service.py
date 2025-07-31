from socioeconomic_distribution.domain.entities.inscription_level import InscriptionLevel
from typing import Optional, List

from socioeconomic_distribution.infraestructure.repository.inscription_level_repository import \
    InscriptionLevelRepository


class InscriptionLevelCommandService:
    def __init__(self, inscription_level_repo: InscriptionLevelRepository):
        self.inscription_level_repo = inscription_level_repo

    def create(self, name_level: str, registration_cost: float) -> Optional[InscriptionLevel]:
        if not name_level or name_level.strip() == "":
            raise ValueError("El nombre del nivel es obligatorio y no puede estar vacío.")
        if registration_cost is None or registration_cost < 0:
            raise ValueError("El costo de registro es obligatorio y no puede ser negativo.")
        return self.inscription_level_repo.create(name_level, registration_cost)

    def update(self, inscription_level_id: int, name_level: Optional[str] = None, registration_cost: Optional[float] = None) -> bool:
        if inscription_level_id is None or inscription_level_id <= 0:
            raise ValueError("ID de nivel de inscripción inválido.")
        if name_level is not None and name_level.strip() == "":
            raise ValueError("El nombre del nivel no puede estar vacío.")
        if registration_cost is not None and registration_cost < 0:
            raise ValueError("El costo de registro no puede ser negativo.")
        if name_level is None and registration_cost is None:
            raise ValueError("Se debe proporcionar al menos un campo para actualizar.")
        return self.inscription_level_repo.update(inscription_level_id, name_level, registration_cost)

    def delete(self, inscription_level_id: int) -> bool:
        if inscription_level_id is None or inscription_level_id <= 0:
            raise ValueError("ID de nivel de inscripción inválido.")
        return self.inscription_level_repo.delete(inscription_level_id)
