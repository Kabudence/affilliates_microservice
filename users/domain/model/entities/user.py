class User:
    def __init__(self,
                 id: int = None,
                 account_id: int = None,
                 app_id: int = None,
                 ):
        self.id = id
        if account_id is None:
            raise ValueError("account_id cannot be None")
        self.account_id = account_id
        if app_id is None:
            raise ValueError("app_id cannot be None")
        self.app_id = app_id
    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "app_id": self.app_id
        }