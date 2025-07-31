from typing import List, Optional
from billing.domain.entities.Card import Card
from billing.infraestructure.repository.card_repository import CardRepository


class CardQueryService:
    def __init__(self, card_repo: CardRepository):
        self.card_repo = card_repo

    def get_by_id(self, card_id: int) -> Optional[Card]:
        return self.card_repo.get_by_id(card_id)

    def list_all(self) -> List[Card]:
        return self.card_repo.list_all()

    def list_by_user(self, user_id: int) -> List[Card]:
        return self.card_repo.list_by_user(user_id)
