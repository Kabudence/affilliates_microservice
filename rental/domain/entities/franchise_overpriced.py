class FranchiseOverpriced:
    def __init__(self,
                 id : int = None,
                 extra_price: float= 0.0,
                 franchise_id: int = None,
                 plan_id: int = None,
                 ):
        self.id = id
        if extra_price < 0:
            raise ValueError("Extra price cannot be negative.")
        self.extra_price = extra_price
        if franchise_id is not None:
            if franchise_id <= 0:
                raise ValueError("Franchise ID must be positive.")
        self.franchise_id = franchise_id
        if plan_id is not None:
            if plan_id <= 0:
                raise ValueError("Plan ID must be positive.")
        self.plan_id = plan_id
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "extra_price": self.extra_price,
            "franchise_id": self.franchise_id,
            "plan_id": self.plan_id
        }