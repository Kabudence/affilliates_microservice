from typing import Optional, List

from socioeconomic_distribution.domain.entities.district import District
from socioeconomic_distribution.infraestructure.repository.district_repository import DistrictRepository


class DistrictQueryService:
    def __init__(self, district_repo: DistrictRepository):
        self.district_repo = district_repo

    def get_by_id(self, district_id: int) -> Optional[District]:
        if district_id is None or district_id <= 0:
            raise ValueError("ID de distrito inválido.")
        return self.district_repo.get_by_id(district_id)

    def list_all(self) -> List[District]:
        return self.district_repo.get_all()