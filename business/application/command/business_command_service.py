from typing import Optional

from business.domain.entities.business import BusinessData
from business.infraestructure.repositories.business_repository import BusinessRepository


class BusinessCommandService:
    def __init__(self, repo: BusinessRepository):
        self.repo = repo

    # --------------------------
    # Validation helpers (required + format)
    # --------------------------
    @staticmethod
    def _require_non_empty(value: str, field: str, max_len: int | None = None) -> str:
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field} is required and cannot be empty")
        v = str(value).strip()
        if max_len is not None and len(v) > max_len:
            raise ValueError(f"{field} must be at most {max_len} characters")
        return v

    @staticmethod
    def _require_positive_int(value: Optional[int], field: str, allow_none: bool = False) -> Optional[int]:
        if value is None:
            if allow_none:
                return None
            raise ValueError(f"{field} is required")
        try:
            iv = int(value)
        except Exception:
            raise ValueError(f"{field} must be an integer")
        if iv <= 0:
            raise ValueError(f"{field} must be > 0")
        return iv

    @staticmethod
    def _validate_ruc(ruc: str) -> str:
        r = BusinessCommandService._require_non_empty(ruc, "ruc")
        if len(r) != 11 or not r.isdigit():
            raise ValueError("ruc must be exactly 11 numeric digits")
        return r

    # --------------------------
    # Commands
    # --------------------------
    def create(
        self,
        name: str,
        ruc: str,
        social_reasoning: str,
        direction: str,
        user_owner_id: int,
        district_id: Optional[int] = None,
        sector_id: Optional[int] = None,
    ) -> BusinessData:
        # Required fields
        name = self._require_non_empty(name, "name", max_len=150)
        ruc = self._validate_ruc(ruc)
        social_reasoning = self._require_non_empty(social_reasoning, "social_reasoning", max_len=255)
        direction = self._require_non_empty(direction, "direction", max_len=255)

        # Required numeric fields
        user_owner_id = self._require_positive_int(user_owner_id, "user_owner_id")

        # Optional numeric fields (if provided, must be > 0)
        district_id = self._require_positive_int(district_id, "district_id", allow_none=True)
        sector_id = self._require_positive_int(sector_id, "sector_id", allow_none=True)

        # Uniqueness rule (common in business entities)
        existing = self.repo.find_by_ruc(ruc)
        if existing is not None:
            raise ValueError("A business with this ruc already exists")

        entity = BusinessData(
            name=name,
            ruc=ruc,
            social_reasoning=social_reasoning,
            direction=direction,
            user_owner_id=user_owner_id,
            district_id=district_id,
            sector_id=sector_id,
        )
        return self.repo.create(entity)

    def update(
        self,
        id_: int,
        name: str,
        ruc: str,
        social_reasoning: str,
        direction: str,
        user_owner_id: int,
        district_id: Optional[int] = None,
        sector_id: Optional[int] = None,
    ) -> Optional[BusinessData]:
        # Required ID
        id_ = self._require_positive_int(id_, "id_")

        # Read current
        current = self.repo.get_by_id(id_)
        if not current:
            raise ValueError("Business not found.")

        # Required fields
        name = self._require_non_empty(name, "name", max_len=150)
        ruc = self._validate_ruc(ruc)
        social_reasoning = self._require_non_empty(social_reasoning, "social_reasoning", max_len=255)
        direction = self._require_non_empty(direction, "direction", max_len=255)

        # Required numeric fields
        user_owner_id = self._require_positive_int(user_owner_id, "user_owner_id")

        # Optional numeric fields (if provided, must be > 0)
        district_id = self._require_positive_int(district_id, "district_id", allow_none=True)
        sector_id = self._require_positive_int(sector_id, "sector_id", allow_none=True)

        # Uniqueness rule for RUC (allow same record)
        existing = self.repo.find_by_ruc(ruc)
        if existing is not None and existing.id != current.id:
            raise ValueError("Another business with this ruc already exists")

        current.name = name
        current.ruc = ruc
        current.social_reasoning = social_reasoning
        current.direction = direction
        current.user_owner_id = user_owner_id
        current.district_id = district_id
        current.sector_id = sector_id

        return self.repo.update(current)

    def delete(self, id_: int) -> bool:
        id_ = self._require_positive_int(id_, "id_")
        return self.repo.delete(id_)
