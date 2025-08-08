# rental/infraestructure/Repositories/franchise_config_repository.py
from typing import Optional, List

from rental.domain.entities.franchise_config import FranchiseConfig
from rental.infraestructure.model.franchise_config_model import FranchiseConfigModel


class FranchiseConfigRepository:
    def get_by_id(self, id_: int) -> Optional[FranchiseConfig]:
        try:
            r = FranchiseConfigModel.get(FranchiseConfigModel.id == id_)
            return FranchiseConfig(id=r.id, franchise_owner_id=r.franchise_owner_id, activate_commissions=r.activate_commissions)
        except FranchiseConfigModel.DoesNotExist:
            return None

    def get_all(self) -> List[FranchiseConfig]:
        return [
            FranchiseConfig(id=r.id, franchise_owner_id=r.franchise_owner_id, activate_commissions=r.activate_commissions)
            for r in FranchiseConfigModel.select()
        ]

    def create(self, cfg: FranchiseConfig) -> FranchiseConfig:
        r = FranchiseConfigModel.create(
            franchise_owner_id=cfg.franchise_owner_id,
            activate_commissions=cfg.activate_commissions,
        )
        return FranchiseConfig(id=r.id, franchise_owner_id=r.franchise_owner_id, activate_commissions=r.activate_commissions)

    def update(self, cfg: FranchiseConfig) -> Optional[FranchiseConfig]:
        try:
            r = FranchiseConfigModel.get(FranchiseConfigModel.id == cfg.id)
            r.franchise_owner_id   = cfg.franchise_owner_id
            r.activate_commissions = cfg.activate_commissions
            r.save()
            return FranchiseConfig(id=r.id, franchise_owner_id=r.franchise_owner_id, activate_commissions=r.activate_commissions)
        except FranchiseConfigModel.DoesNotExist:
            return None

    def delete(self, id_: int) -> bool:
        try:
            r = FranchiseConfigModel.get(FranchiseConfigModel.id == id_)
            r.delete_instance()
            return True
        except FranchiseConfigModel.DoesNotExist:
            return False

    def get_by_franchise_owner_id(self, franchise_owner_id: int) -> Optional[FranchiseConfig]:
        try:
            r = FranchiseConfigModel.get(FranchiseConfigModel.franchise_owner_id == franchise_owner_id)
            return FranchiseConfig(id=r.id, franchise_owner_id=r.franchise_owner_id, activate_commissions=r.activate_commissions)
        except FranchiseConfigModel.DoesNotExist:
            return None
