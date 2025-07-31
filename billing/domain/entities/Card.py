class Card:
    def __init__(self,
                 id: int = None,
                 number: str = "",
                 expiration_date: str = "",
                 cvv: str = "",
                 user_id: int = None,
                 ):
        self.id = id
        if number is None or number.strip() == "":
            raise ValueError("number cannot be None or empty")
        self.number = number
        if expiration_date is None or expiration_date.strip() == "":
            raise ValueError("expiration_date cannot be None or empty")
        self.expiration_date = expiration_date
        if cvv is None or cvv.strip() == "":
            raise ValueError("cvv cannot be None or empty")
        self.cvv = cvv
        if user_id is None:
            raise ValueError("user_id cannot be None")
        self.user_id = user_id