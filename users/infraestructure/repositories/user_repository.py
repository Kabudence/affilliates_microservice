from typing import Optional, List

from users.domain.model.entities.user import User
from users.infraestructure.models.user_model import UserModel


class UserRepository:
    def get_by_id(self, id: int) -> Optional[User]:
        try:
            record = UserModel.get(UserModel.id == id)
            return User(
                id=record.id,
                account_id=record.account_id,
                app_id=record.app_id,

            )
        except UserModel.DoesNotExist:
            return None

    def get_all(self) -> List[User]:
        return [
            User(
                id=rec.id,
                account_id=rec.account_id,
                app_id=rec.app_id,

            )
            for rec in UserModel.select()
        ]

    def create(self, user: User) -> User:
        record = UserModel.create(
            account_id=user.account_id,
            app_id=user.app_id
            # created_at/updated_at lo gestiona MySQL
        )
        return User(
            id=record.id,
            account_id=record.account_id,
            app_id=record.app_id,

        )

    def update(self, user: User) -> Optional[User]:
        try:
            record = UserModel.get(UserModel.id == user.id)
            record.account_id = user.account_id
            record.app_id = user.app_id
            # No tocamos created_at
            record.save()
            return User(
                id=record.id,
                account_id=record.account_id,
                app_id=record.app_id,

            )
        except UserModel.DoesNotExist:
            return None

    def delete(self, user_id: int) -> bool:
        try:
            record = UserModel.get(UserModel.id == user_id)
            record.delete_instance()
            return True
        except UserModel.DoesNotExist:
            return False

    # Extra: Buscar por account_id y/o app_id
    def find_by_account_and_app(self, account_id: Optional[int] = None, app_id: Optional[int] = None) -> List[User]:
        query = UserModel.select()
        if account_id is not None:
            query = query.where(UserModel.account_id == account_id)
        if app_id is not None:
            query = query.where(UserModel.app_id == app_id)
        return [
            User(
                id=rec.id,
                account_id=rec.account_id,
                app_id=rec.app_id,

            )
            for rec in query
        ]
