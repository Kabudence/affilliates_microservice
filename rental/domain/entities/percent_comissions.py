from enum import Enum


class CommissionType(Enum):
    APPLICATION = "application"
    FRANCHISE = "franchise"

class PercentCommissions:
    def __init__(self,
                 id :int = None,
                 percent: float = 0.0,
                 owner_id: int = None,
                 commission_type: CommissionType = CommissionType.APPLICATION,
                 ):
        self.id = id
        if percent is None or percent < 0:
            raise ValueError("percent cannot be None or negative")
        self.percent = percent
        if owner_id is None:
            raise ValueError("owner_id cannot be None")
        self.owner_id = owner_id
        if not isinstance(commission_type, CommissionType):
            raise ValueError("commission_type must be an instance of CommissionType Enum")
        self.commission_type = commission_type if isinstance(commission_type, CommissionType) else CommissionType(commission_type)

    def to_dict(self):
        return {
            "id": self.id,
            "percent": self.percent,
            "owner_id": self.owner_id,
            "commission_type": self.commission_type.value if isinstance(self.commission_type, CommissionType) else self.commission_type
        }