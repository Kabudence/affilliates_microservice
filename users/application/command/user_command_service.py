from users.domain.model.entities.user import User, UserType
from users.infraestructure.repositories.user_repository import UserRepository
from typing import Optional

class UserCommandService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

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
        user = User(
            account_id=account_id,
            app_id=app_id,
            user_owner_id=user_owner_id,
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
