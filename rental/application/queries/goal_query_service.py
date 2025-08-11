from typing import List, Optional
from rental.domain.entities.goal import Goal, GoalType
from rental.infraestructure.Repositories.goal_repository import GoalRepository


class GoalQueryService:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    def get_by_id(self, goal_id: int) -> Optional[Goal]:
        return self.goal_repo.get_by_id(goal_id)

    def list_all(self) -> List[Goal]:
        return self.goal_repo.get_all()

    def get_by_owner_id_and_goal_type(self, owner_id: int, goal_type: GoalType | str) -> Optional[Goal]:
        gt = goal_type if isinstance(goal_type, GoalType) else GoalType(goal_type)
        return self.goal_repo.get_by_owner_id_and_goal_type(owner_id, gt)

    def list_by_owner_id_and_goal_type(self, owner_id: int, goal_type: GoalType | str) -> List[Goal]:
        gt = goal_type if isinstance(goal_type, GoalType) else GoalType(goal_type)
        return self.goal_repo.list_by_owner_id_and_goal_type(owner_id, gt)