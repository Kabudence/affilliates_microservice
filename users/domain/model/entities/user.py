from enum import Enum
from typing import Optional

class UserType(Enum):
    AFILIATE = "affiliate"
    BUYER = "buyer"

class User:
    def __init__(self,
                 id: Optional[int] = None,
                 account_id: Optional[int] = None,
                 app_id: Optional[int] = None,
                 user_owner_id: Optional[int] = None,
                 user_type: UserType = UserType.BUYER
                 ):
        self.id = id
        if account_id is None:
            raise ValueError("account_id cannot be None")
        self.account_id = account_id
        if app_id is None:
            raise ValueError("app_id cannot be None")
        self.app_id = app_id
        self.user_owner_id = user_owner_id  # Puede ser None
        if not isinstance(user_type, UserType):
            raise ValueError("user_type must be an instance of UserType Enum")
        self.user_type = user_type

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "app_id": self.app_id,
            "user_owner_id": self.user_owner_id,
            "user_type": self.user_type.value if isinstance(self.user_type, UserType) else self.user_type
        }
