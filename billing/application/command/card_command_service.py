from billing.domain.entities.Card import Card
from typing import Optional

from billing.infraestructure.repository.card_repository import CardRepository


class CardCommandService:
    def __init__(self, card_repo: CardRepository):
        self.card_repo = card_repo

    def create(self, number: str, expiration_date: str, cvv: str, user_id: int) -> Card:
        if not number or not expiration_date or not cvv or user_id is None:
            raise ValueError("All fields are required.")
        return self.card_repo.create(number, expiration_date, cvv, user_id)

    def update(self, card_id: int, number: Optional[str] = None, expiration_date: Optional[str] = None, cvv: Optional[str] = None) -> Optional[Card]:
        card = self.card_repo.get_by_id(card_id)
        if not card:
            raise ValueError("Card not found.")
        return self.card_repo.update(card_id, number, expiration_date, cvv)

    def delete(self, card_id: int) -> bool:
        return self.card_repo.delete(card_id)
