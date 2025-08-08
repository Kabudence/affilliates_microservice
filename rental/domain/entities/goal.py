from enum import Enum


class GoalType(Enum):
    APPLICATION = "application"
    FRANCHISE = "franchise"


class Goal:
    def __init__ (self,
                  id : int = None,
                  number_of_clients: int = None,
                  month:int = None,
                  percentage_to_bonus: float = None,
                  owner_id: int = None,
                  goal_type: GoalType = GoalType.APPLICATION

                ):
        self.id = id
        if number_of_clients is None:
            raise ValueError("number_of_clients cannot be None")
        self.number_of_clients = number_of_clients
        if month is None:
            raise ValueError("month cannot be None")
        self.month = month
        if percentage_to_bonus is None:
            raise ValueError("percentage_to_bonus cannot be None")
        self.percentage_to_bonus = percentage_to_bonus
        if owner_id is None:
            raise ValueError("owner_id cannot be None")
        self.owner_id = owner_id
        if goal_type is None:
            raise ValueError("goal_type cannot be None")
        self.goal_type = goal_type

    def to_dict(self):
        return {
            "id": self.id,
            "number_of_clients": self.number_of_clients,
            "month": self.month,
            "percentage_to_bonus": self.percentage_to_bonus,
            "owner_id": self.owner_id,
            "goal_type": self.goal_type.value
        }