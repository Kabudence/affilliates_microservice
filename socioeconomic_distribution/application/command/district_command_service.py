from typing import Optional

from socioeconomic_distribution.domain.entities.district import District
from socioeconomic_distribution.infraestructure.repository.district_repository import DistrictRepository


class DistrictCommandService:
    def __init__(self, district_repo: DistrictRepository):
        self.district_repo = district_repo

    def create(self, name: str, inscription_level: str) -> Optional[District]:
        if not name or name.strip() == "":
            raise ValueError("El nombre del distrito es obligatorio y no puede estar vacío.")
        if not inscription_level or inscription_level.strip() == "":
            raise ValueError("El nivel de inscripción es obligatorio y no puede estar vacío.")
        # Si necesitas validar unicidad del nombre, deberías buscarlo aquí antes de crear
        return self.district_repo.create(name, inscription_level)

    def update(self, district_id: int, name: Optional[str] = None, inscription_level: Optional[str] = None) -> bool:
        if name is not None and name.strip() == "":
            raise ValueError("El nombre del distrito no puede estar vacío.")
        if inscription_level is not None and inscription_level.strip() == "":
            raise ValueError("El nivel de inscripción no puede estar vacío.")
        if name is None and inscription_level is None:
            raise ValueError("Se debe proporcionar al menos un campo para actualizar.")
        return self.district_repo.update(district_id, name, inscription_level)

    def delete(self, district_id: int) -> bool:
        if district_id is None or district_id <= 0:
            raise ValueError("ID de distrito inválido.")
        return self.district_repo.delete(district_id)