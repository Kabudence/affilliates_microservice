from typing import Optional, List
from users.domain.model.entities.user import User
from users.infraestructure.repositories.user_repository import UserRepository

class UserQueryService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_by_id(self, user_id: int) -> Optional[User]:
        if user_id is None or user_id <= 0:
            raise ValueError("El id de usuario debe ser positivo.")
        return self.user_repo.get_by_id(user_id)

    def list_all(self) -> List[User]:
        return self.user_repo.get_all()

    def find_by_account_and_app(
        self,
        account_id: Optional[int] = None,
        app_id: Optional[int] = None
    ) -> List[User]:
        if account_id is None and app_id is None:
            raise ValueError("Debe proporcionar al menos account_id o app_id para filtrar.")
        if account_id is not None and account_id <= 0:
            raise ValueError("El account_id debe ser positivo si se proporciona.")
        if app_id is not None and app_id <= 0:
            raise ValueError("El app_id debe ser positivo si se proporciona.")
        return self.user_repo.find_by_account_and_app(account_id, app_id)
