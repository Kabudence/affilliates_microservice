# rental/application/commands/franchise_config_command_service.py
from typing import Optional
from rental.domain.entities.franchise_config import FranchiseConfig
from rental.infraestructure.Repositories.franchise_config_repository import FranchiseConfigRepository


class FranchiseConfigCommandService:
    def __init__(self, repo: FranchiseConfigRepository):
        self.repo = repo

    @staticmethod
    def _validate(franchise_owner_id: int, activate_commissions: bool) -> None:
        if franchise_owner_id is None:
            raise ValueError("franchise_owner_id is required")
        if franchise_owner_id <= 0:
            raise ValueError("franchise_owner_id must be positive")
        if not isinstance(activate_commissions, bool):
            raise ValueError("activate_commissions must be a boolean")

    def create(self, franchise_owner_id: int, activate_commissions: bool) -> FranchiseConfig:
        self._validate(franchise_owner_id, activate_commissions)
        entity = FranchiseConfig(franchise_owner_id=franchise_owner_id, activate_commissions=activate_commissions)
        return self.repo.create(entity)

    def update(self, id_: int, franchise_owner_id: int, activate_commissions: bool) -> Optional[FranchiseConfig]:
        current = self.repo.get_by_id(id_)
        if not current:
            raise ValueError("FranchiseConfig not found")

        self._validate(franchise_owner_id, activate_commissions)
        current.franchise_owner_id   = franchise_owner_id
        current.activate_commissions = activate_commissions
        return self.repo.update(current)

    def delete(self, id_: int) -> bool:
        return self.repo.delete(id_)
