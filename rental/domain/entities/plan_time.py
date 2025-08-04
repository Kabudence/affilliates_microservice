class PlanTime:
    def __init__(self,
                 id: int = None,
                 plan_id: int = None,
                 duration: int = None,    # meses
                 price: float = None
                 ):
        self.id = id
        self.plan_id = plan_id
        self.duration = duration
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "duration": self.duration,
            "price": self.price
        }
