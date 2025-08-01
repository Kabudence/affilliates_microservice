class District:
    def __init__(self,
                 id: int = None,
                 name: str = "",
                 inscription_level_id: int = None,
                 ):
        self.id = id
        if name is None or name.strip() == "":
            raise ValueError("name cannot be None or empty")
        self.name = name
        if inscription_level_id is None or inscription_level_id == -1:
            raise ValueError("inscription_level_id cannot be None or -1")
        self.inscription_level_id = inscription_level_id
    def to_dict(self):
       return {
            "id": self.id,
            "name": self.name,
            "inscription_level_id": self.inscription_level_id
        }
