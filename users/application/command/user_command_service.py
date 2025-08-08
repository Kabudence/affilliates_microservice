from rental.domain.entities.plan import Plan, _to_plan_type, PlanType
from users.domain.model.entities.user import User, UserType
from users.infraestructure.repositories.user_repository import UserRepository
from typing import Optional

class UserCommandService:
    def __init__(
            self,
            user_repo: UserRepository,
            user_query_service,  # inyectado
            subscription_query_service,  # inyectado
            plan_query_service  # inyectado
    ):
        self.user_repo = user_repo
        self.user_query_service = user_query_service
        self.subscription_query_service = subscription_query_service
        self.plan_query_service = plan_query_service

    def create(
            self,
            account_id: int,
            app_id: int,
            user_type: UserType,
            user_owner_id: Optional[int] = None
    ) -> User:
        if account_id is None or account_id <= 0:
            raise ValueError("El account_id es obligatorio y debe ser positivo.")
        if app_id is None or app_id <= 0:
            raise ValueError("El app_id es obligatorio y debe ser positivo.")
        if not isinstance(user_type, UserType):
            raise ValueError("user_type debe ser una instancia del Enum UserType.")
        if user_owner_id is not None and user_owner_id <= 0:
            raise ValueError("user_owner_id debe ser positivo si se proporciona.")

        # 🔁 Normaliza owner para evitar "nietos" de franquiciado
        owner_id_normalizado = self._resolve_owner_avoiding_franchise_grandchildren(user_owner_id)

        user = User(
            account_id=account_id,
            app_id=app_id,
            user_owner_id=owner_id_normalizado,
            user_type=user_type
        )
        return self.user_repo.create(user)

    def update(
        self,
        user_id: int,
        account_id: int,
        app_id: int,
        user_type: UserType,
        user_owner_id: Optional[int] = None
    ) -> Optional[User]:
        if user_id is None or user_id <= 0:
            raise ValueError("El id de usuario es obligatorio y debe ser positivo.")
        if account_id is None or account_id <= 0:
            raise ValueError("El account_id es obligatorio y debe ser positivo.")
        if app_id is None or app_id <= 0:
            raise ValueError("El app_id es obligatorio y debe ser positivo.")
        if not isinstance(user_type, UserType):
            raise ValueError("user_type debe ser una instancia del Enum UserType.")
        if user_owner_id is not None and user_owner_id <= 0:
            raise ValueError("user_owner_id debe ser positivo si se proporciona.")
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")
        user.account_id = account_id
        user.app_id = app_id
        user.user_owner_id = user_owner_id
        user.user_type = user_type
        return self.user_repo.update(user)

    def delete(self, user_id: int) -> bool:
        if user_id is None or user_id <= 0:
            raise ValueError("El id de usuario es obligatorio y debe ser positivo.")
        return self.user_repo.delete(user_id)

    def _resolve_owner_avoiding_franchise_grandchildren(self, user_owner_id: Optional[int]) -> Optional[int]:
        """
        Regla: un franquiciado NO puede tener nietos.
        Si user_owner_id apunta a un usuario cuyo padre es franquiciado,
        se reasigna el owner al franquiciado (abuelo).
        Si user_owner_id ya es franquiciado, se deja tal cual.
        """
        if not user_owner_id:
            return None

        owner = self.user_query_service.get_by_id(user_owner_id)
        if not owner:
            # si el owner no existe, devuelve tal cual y que lo valide otra capa si toca
            return user_owner_id

        # Caso 1: el owner indicado es franquiciado → ok, dejar como está
        is_owner_franchise, _ = self._is_franchise_user(owner.id)
        if is_owner_franchise:
            return owner.id

        # Caso 2: el owner NO es franquiciado, pero su padre SÍ lo es → re-asignar al franquiciado
        grand_owner_id = getattr(owner, "user_owner_id", None)
        if grand_owner_id:
            is_grand_franchise, _ = self._is_franchise_user(grand_owner_id)
            if is_grand_franchise:
                return grand_owner_id

        # Caso 3: nadie es franquiciado en la línea → dejar como llegó
        return user_owner_id

    def _is_franchise_user(self, user_id: int) -> tuple[bool, Optional[Plan]]:
        subscription = self.subscription_query_service.get_subscription_by_user_id(user_id)
        if not subscription:
            return False, None
        plan = self.plan_query_service.get_by_id(subscription.plan_id)
        if not plan:
            return False, None
        plan_type = _to_plan_type(plan.plan_type)
        return (plan_type == PlanType.FRANQUICIA_EXCLUSIVA), plan