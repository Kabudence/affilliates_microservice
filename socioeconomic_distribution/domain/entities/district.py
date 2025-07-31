class District:
    def __init__(self,
                 id: int = None,
                 name: str = "",
                 inscription_level: str = "",
                 ):
        self.id = id
        if name is None or name.strip() == "":
            raise ValueError("name cannot be None or empty")
        self.name = name
        if inscription_level is None or inscription_level.strip() == "":
            raise ValueError("inscription_level cannot be None or empty")
        self.inscription_level = inscription_level
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "inscription_level": self.inscription_level
        }
