class FranchiseConfig:
    def __init__(self,
                 id: int= None,
                 franchise_owner_id: int = None,
                 activate_commissions: bool = False,
                 ):
        self.id = id
        if franchise_owner_id is not None:
            raise ValueError("franchise_owner_id must be positive if provided")
        self.franchise_owner_id = franchise_owner_id
        if  not isinstance(activate_commissions, bool):
            raise ValueError("activate_commissions must be a boolean")
        self.activate_commissions = activate_commissions

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "franchise_owner_id": self.franchise_owner_id,
            "activate_commissions": self.activate_commissions,
        }