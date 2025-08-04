from typing import Optional, List
from users.domain.model.entities.user import User, UserType
from users.infraestructure.models.user_model import UserModel

class UserRepository:
    def get_by_id(self, id: int) -> Optional[User]:
        try:
            record = UserModel.get(UserModel.id == id)
            return User(
                id=record.id,
                account_id=record.account_id,
                app_id=record.app_id,
                user_owner_id=record.user_owner_id,
                user_type=UserType(record.user_type)
            )
        except UserModel.DoesNotExist:
            return None

    def get_by_account_id(self, account_id: int) -> Optional[User]:
        try:
            record = UserModel.get(UserModel.account_id == account_id)
            return User(
                id=record.id,
                account_id=record.account_id,
                app_id=record.app_id,
                user_owner_id=record.user_owner_id,
                user_type=UserType(record.user_type)
            )
        except UserModel.DoesNotExist:
            return None


    def get_all(self) -> List[User]:
        return [
            User(
                id=rec.id,
                account_id=rec.account_id,
                app_id=rec.app_id,
                user_owner_id=rec.user_owner_id,
                user_type=UserType(rec.user_type)
            )
            for rec in UserModel.select()
        ]

    def create(self, user: User) -> User:
        record = UserModel.create(
            account_id=user.account_id,
            app_id=user.app_id,
            user_owner_id=user.user_owner_id,  # Puede ser None y se guarda como NULL
            user_type=user.user_type.value
        )
        return User(
            id=record.id,
            account_id=record.account_id,
            app_id=record.app_id,
            user_owner_id=record.user_owner_id,
            user_type=UserType(record.user_type)
        )

    def update(self, user: User) -> Optional[User]:
        try:
            record = UserModel.get(UserModel.id == user.id)
            record.account_id = user.account_id
            record.app_id = user.app_id
            record.user_owner_id = user.user_owner_id
            record.user_type = user.user_type.value
            record.save()
            return User(
                id=record.id,
                account_id=record.account_id,
                app_id=record.app_id,
                user_owner_id=record.user_owner_id,
                user_type=UserType(record.user_type)
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

    def find_by_account_and_app(self, account_id: Optional[int] = None, app_id: Optional[int] = None) -> Optional[User]:
        query = UserModel.select()
        if account_id is not None:
            query = query.where(UserModel.account_id == account_id)
        if app_id is not None:
            query = query.where(UserModel.app_id == app_id)
        rec = query.first()  # Devuelve el primer registro o None

        if rec:
            return User(
                id=rec.id,
                account_id=rec.account_id,
                app_id=rec.app_id,
                user_owner_id=rec.user_owner_id,
                user_type=UserType(rec.user_type)
            )
        else:
            return None
