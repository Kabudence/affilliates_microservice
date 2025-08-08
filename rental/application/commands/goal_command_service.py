from typing import Optional
from rental.domain.entities.goal import Goal, GoalType
from rental.infraestructure.Repositories.goal_repository import GoalRepository

class GoalCommandService:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    @staticmethod
    def _validate(number_of_clients: int, month: int, percentage_to_bonus: float, owner_id: int, goal_type) -> None:
        if None in (number_of_clients, month, percentage_to_bonus, owner_id, goal_type):
            raise ValueError("All fields are required.")
        if not (1 <= int(month) <= 12):
            raise ValueError("month must be between 1 and 12")
        if float(percentage_to_bonus) < 0:
            raise ValueError("percentage_to_bonus must be >= 0")
        # coerce goal_type early
        GoalType(goal_type) if not isinstance(goal_type, GoalType) else goal_type

    def create(self, number_of_clients: int, month: int, percentage_to_bonus: float, owner_id: int, goal_type: GoalType | str) -> Goal:
        self._validate(number_of_clients, month, percentage_to_bonus, owner_id, goal_type)
        gt = goal_type if isinstance(goal_type, GoalType) else GoalType(goal_type)
        goal = Goal(
            number_of_clients=number_of_clients,
            month=month,
            percentage_to_bonus=percentage_to_bonus,
            owner_id=owner_id,
            goal_type=gt,
        )
        return self.goal_repo.create(goal)

    def update(self, goal_id: int, number_of_clients: int, month: int, percentage_to_bonus: float, owner_id: int, goal_type: GoalType | str) -> Goal:
        existing = self.goal_repo.get_by_id(goal_id)
        if not existing:
            raise ValueError("Goal not found")

        self._validate(number_of_clients, month, percentage_to_bonus, owner_id, goal_type)
        gt = goal_type if isinstance(goal_type, GoalType) else GoalType(goal_type)

        existing.number_of_clients   = number_of_clients
        existing.month               = month
        existing.percentage_to_bonus = percentage_to_bonus
        existing.owner_id            = owner_id
        existing.goal_type           = gt
        return self.goal_repo.update(existing)

    def delete(self, goal_id: int) -> bool:
        return self.goal_repo.delete(goal_id)
