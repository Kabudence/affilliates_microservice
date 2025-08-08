from typing import Optional, List
from rental.domain.entities.goal import Goal, GoalType
from rental.infraestructure.model.goal_model import GoalModel

class GoalRepository:
    def get_by_id(self, id: int) -> Optional[Goal]:
        try:
            r = GoalModel.get(GoalModel.id == id)
            return Goal(
                id=r.id,
                number_of_clients=r.number_of_clients,
                month=r.month,
                percentage_to_bonus=r.percentage_to_bonus,
                owner_id=r.owner_id,
                goal_type=GoalType(r.goal_type),
            )
        except GoalModel.DoesNotExist:
            return None

    def get_all(self) -> List[Goal]:
        return [
            Goal(
                id=r.id,
                number_of_clients=r.number_of_clients,
                month=r.month,
                percentage_to_bonus=r.percentage_to_bonus,
                owner_id=r.owner_id,
                goal_type=GoalType(r.goal_type),
            )
            for r in GoalModel.select()
        ]

    def create(self, goal: Goal) -> Goal:
        r = GoalModel.create(
            number_of_clients=goal.number_of_clients,
            month=goal.month,
            percentage_to_bonus=goal.percentage_to_bonus,
            owner_id=goal.owner_id,
            goal_type=goal.goal_type.value if isinstance(goal.goal_type, GoalType) else goal.goal_type,
        )
        return Goal(
            id=r.id,
            number_of_clients=r.number_of_clients,
            month=r.month,
            percentage_to_bonus=r.percentage_to_bonus,
            owner_id=r.owner_id,
            goal_type=GoalType(r.goal_type),
        )

    def update(self, goal: Goal) -> Optional[Goal]:
        try:
            r = GoalModel.get(GoalModel.id == goal.id)
            r.number_of_clients   = goal.number_of_clients
            r.month               = goal.month
            r.percentage_to_bonus = goal.percentage_to_bonus
            r.owner_id            = goal.owner_id
            r.goal_type           = goal.goal_type.value if isinstance(goal.goal_type, GoalType) else goal.goal_type
            r.save()
            return Goal(
                id=r.id,
                number_of_clients=r.number_of_clients,
                month=r.month,
                percentage_to_bonus=r.percentage_to_bonus,
                owner_id=r.owner_id,
                goal_type=GoalType(r.goal_type),
            )
        except GoalModel.DoesNotExist:
            return None

    def delete(self, goal_id: int) -> bool:
        try:
            r = GoalModel.get(GoalModel.id == goal_id)
            r.delete_instance()
            return True
        except GoalModel.DoesNotExist:
            return False

    # 🔄 NUEVO: reemplaza list_by_owner_id
    def get_by_owner_id_and_goal_type(self, owner_id: int, goal_type: GoalType) -> Optional[Goal]:
        try:
            r = GoalModel.get(
                (GoalModel.owner_id == owner_id) &
                (GoalModel.goal_type == (goal_type.value if isinstance(goal_type, GoalType) else goal_type))
            )
            return Goal(
                id=r.id,
                number_of_clients=r.number_of_clients,
                month=r.month,
                percentage_to_bonus=r.percentage_to_bonus,
                owner_id=r.owner_id,
                goal_type=GoalType(r.goal_type),
            )
        except GoalModel.DoesNotExist:
            return None
