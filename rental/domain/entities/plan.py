
from enum import Enum

class PlanType(Enum):
    ALQUILER_SIMPLE = "alquiler_simple"
    ALQUILER_SIMPLE_PRO = "alquiler_simple_pro"
    INTERMEDIO = "intermedio"
    INTERMEDIO_PRO = "intermedio_pro"
    PREMIUM = "premium"
    FRANQUICIA_INDIVIDUAL = "franquicia_individual"
    FRANQUICIA_INDIVIDUAL_PRO = "franquicia_individual_pro"
    FRANQUICIA_EXCLUSIVA = "franquicia_exclusiva"


    SIMPLE_PRO_COM = "simple_pro_com"
    SIMPLE_PRO_GYM = "simple_pro_gym"
    INTERMEDIO_PRO_COM = "intermedio_pro_com"
    INTERMEDIO_PRO_GYM = "intermedio_pro_gym"
    FRANQUICIA_INDIVIDUAL_pro_COM = "franquicia_individual_pro_com"

class Plan:
    def __init__(self,
                 id: int = None,
                 name: str = "",
                 description: str = "",
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
            "plan_type": self.plan_type.value if isinstance(self.plan_type, PlanType) else self.plan_type,
            "app_id": self.app_id
        }
