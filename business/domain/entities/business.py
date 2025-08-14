from typing import Optional
from dataclasses import dataclass


@dataclass
class BusinessData:
    id: Optional[int] = None
    name: str = ""
    ruc: str = ""
    social_reasoning: str = ""   # legal name
    direction: str = ""          # address
    user_owner_id: int = 0       # REQUIRED
    district_id: Optional[int] = None
    sector_id: Optional[int] = None

    def __post_init__(self):
        if self.name is None or self.name.strip() == "":
            raise ValueError("name cannot be None or empty")
        if self.ruc is None or self.ruc.strip() == "":
            raise ValueError("ruc cannot be None or empty")
        if self.social_reasoning is None or self.social_reasoning.strip() == "":
            raise ValueError("social_reasoning cannot be None or empty")
        if self.direction is None or self.direction.strip() == "":
            raise ValueError("direction cannot be None or empty")
        if self.user_owner_id is None or int(self.user_owner_id) <= 0:
            raise ValueError("user_owner_id must be a positive integer")

        self.name = self.name.strip()
        self.ruc = self.ruc.strip()
        self.social_reasoning = self.social_reasoning.strip()
        self.direction = self.direction.strip()
        self.user_owner_id = int(self.user_owner_id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ruc": self.ruc,
            "social_reasoning": self.social_reasoning,
            "direction": self.direction,
            "user_owner_id": self.user_owner_id,
            "district_id": self.district_id,
            "sector_id": self.sector_id,
        }
