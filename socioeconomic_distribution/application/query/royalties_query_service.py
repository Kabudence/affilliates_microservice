from typing import Optional, List

from socioeconomic_distribution.domain.entities.royalties import Royalties
from socioeconomic_distribution.infraestructure.repository.royalties_repository import RoyaltiesRepository


class RoyaltiesQueryService:
    def __init__(self, royalties_repo: RoyaltiesRepository):
        self.royalties_repo = royalties_repo

    def get_by_id(self, id: int) -> Optional[Royalties]:
        if id is None or id <= 0:
            raise ValueError("ID de royalties inválido.")
        return self.royalties_repo.get_by_id(id)

    def list_all(self) -> List[Royalties]:
        return self.royalties_repo.list_all()