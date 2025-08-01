from enum import Enum


class PlanType(Enum):
 RENTAL = "rental"
 UNIC_FRANCHISE = "unic_franchise"
 EXCLUSIVE_FRANCHISE = "exclusive_franchise"

class Plan:
    def __init__(self,
                 id: int= None,
                name :str = "",
                description: str = "",
                duration: int = None,
                price: float = None,
                plan_type: PlanType = PlanType,
                app_id: int = None
                 ):
        self.id = id
        if name is None or name.strip() == "":
            raise ValueError("name cannot be none or empty")
        self.name = name
        if description is None or description.strip() == "":
            raise ValueError("description cannot be none or empty")
        self.description = description
        if duration is None or duration <= 0:
            raise ValueError("duration must be a positive integer")
        self.duration = duration
        if price is None or price < 0:
            raise ValueError("price cannot be None or negative")
        self.price = price
        if plan_type is None:
            raise ValueError("plan_type cannot be None")
        self.plan_type = plan_type if isinstance(plan_type, PlanType) else PlanType(plan_type)
        if app_id is None:
            raise ValueError("app_id cannot be None")
        self.app_id = app_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }