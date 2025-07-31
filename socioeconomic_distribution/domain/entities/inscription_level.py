class InscriptionLevel:
    def __init__(self,
                 id: int= None,
                 name_level: str = "",
                 registration_cost: float = 0.0,
                 ):
        self.id = id
        if name_level is None or name_level.strip() == "":
            raise ValueError("name_level cannot be None or empty")
        self.name_level = name_level
        if registration_cost is None or registration_cost < 0:
            raise ValueError("registration_cost cannot be None or negative")
        self.registration_cost = registration_cost
    def to_dict(self):
        return {
            "id": self.id,
            "name_level": self.name_level,
            "registration_cost": self.registration_cost
        }