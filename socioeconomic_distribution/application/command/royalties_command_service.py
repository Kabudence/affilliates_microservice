from socioeconomic_distribution.domain.entities.royalties import Royalties
from typing import Optional, List

from socioeconomic_distribution.infraestructure.repository.royalties_repository import RoyaltiesRepository


class RoyaltiesCommandService:
    def __init__(self, royalties_repo: RoyaltiesRepository):
        self.royalties_repo = royalties_repo

    def create(self, inscription_level_id: int, cost: float) -> Royalties:
        if inscription_level_id is None or inscription_level_id <= 0:
            raise ValueError("ID de nivel de inscripción inválido.")
        if cost is None or cost < 0:
            raise ValueError("El costo debe ser un valor no negativo.")
        return self.royalties_repo.create(inscription_level_id, cost)

    def update(self, id: int, inscription_level_id: Optional[int] = None, cost: Optional[float] = None) -> Optional[Royalties]:
        if id is None or id <= 0:
            raise ValueError("ID de royalties inválido.")
        if inscription_level_id is not None and inscription_level_id <= 0:
            raise ValueError("ID de nivel de inscripción inválido.")
        if cost is not None and cost < 0:
            raise ValueError("El costo debe ser un valor no negativo.")
        if inscription_level_id is None and cost is None:
            raise ValueError("Se debe proporcionar al menos un campo para actualizar.")
        return self.royalties_repo.update(id, inscription_level_id, cost)

    def delete(self, id: int) -> bool:
        if id is None or id <= 0:
            raise ValueError("ID de royalties inválido.")
        return self.royalties_repo.delete(id)