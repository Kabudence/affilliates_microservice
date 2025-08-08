from rental.domain.entities.goal import Goal
from rental.infraestructure.Repositories.goal_repository import GoalRepository


class GoalCommandService:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    def create(self, number_of_clients: int, month: int, percentage_to_bonus: float, owner_id: int) -> Goal:
        if None in (number_of_clients, month, percentage_to_bonus, owner_id):
            raise ValueError("All fields are required.")
        if not (1 <= int(month) <= 12):
            raise ValueError("month must be between 1 and 12")
        if float(percentage_to_bonus) < 0:
            raise ValueError("percentage_to_bonus must be >= 0")

        goal = Goal(
            number_of_clients=number_of_clients,
            month=month,
            percentage_to_bonus=percentage_to_bonus,
            owner_id=owner_id
        )
        return self.goal_repo.create(goal)

    def update(self, goal_id: int, number_of_clients: int, month: int, percentage_to_bonus: float, owner_id: int) -> Goal:
        goal = self.goal_repo.get_by_id(goal_id)
        if not goal:
            raise ValueError("Goal not found")

        if None in (number_of_clients, month, percentage_to_bonus, owner_id):
            raise ValueError("All fields are required.")
        if not (1 <= int(month) <= 12):
            raise ValueError("month must be between 1 and 12")
        if float(percentage_to_bonus) < 0:
            raise ValueError("percentage_to_bonus must be >= 0")

        goal.number_of_clients = number_of_clients
        goal.month = month
        goal.percentage_to_bonus = percentage_to_bonus
        goal.owner_id = owner_id
        return self.goal_repo.update(goal)

    def delete(self, goal_id: int) -> bool:
        return self.goal_repo.delete(goal_id)
