class Royalties:
    def __init__(self,
                 id: int = None,
                 inscription_level_id: int = None,
                 cost: float = None,
                 ):
        self.id = id
        if inscription_level_id is None:
            raise ValueError("inscription_level_id cannot be None")
        self.inscription_level_id = inscription_level_id
        if cost is None:
            raise ValueError("cost cannot be None")
        self.cost = cost
    def to_dict(self):
        return {
            "id": self.id,
            "inscription_level_id": self.inscription_level_id,
            "cost": self.cost
        }
        