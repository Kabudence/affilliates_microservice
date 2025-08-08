class FranchiseDiscount:
    def __init__(self,
                 id :int = None,
                 percent: float = 0.0,
                 app_id: int = None,
                 ):
        self.id = id
        if percent is None or percent < 0:
            raise ValueError("percent cannot be None or negative")
        self.percent = percent
        if app_id is None:
            raise ValueError("app_id cannot be None")
        self.app_id = app_id
    def to_dict(self):
        return {
            "id": self.id,
            "percent": self.percent,
            "app_id": self.app_id,
        }