from typing import List, Optional

from billing.domain.entities.Card import Card
from billing.infraestructure.model.card_model import CardModel


class CardRepository:

    def create(self,
               number: str,
               expiration_date: str,
               cvv: str,
               user_id: int) -> Card:

        rec = CardModel.create(
            number=number,
            expiration_date=expiration_date,
            cvv=cvv,
            user_id=user_id
        )
        return Card(
            id=rec.id,
            number=rec.number,
            expiration_date=rec.expiration_date,
            cvv=rec.cvv,
            user_id=rec.user_id
        )

    def get_by_id(self, card_id: int) -> Optional[Card]:
        rec = CardModel.get_or_none(CardModel.id == card_id)
        if not rec:
            return None
        return Card(
            id=rec.id,
            number=rec.number,
            expiration_date=rec.expiration_date,
            cvv=rec.cvv,
            user_id=rec.user_id
        )

    def list_all(self) -> List[Card]:
        return [
            Card(
                id=rec.id,
                number=rec.number,
                expiration_date=rec.expiration_date,
                cvv=rec.cvv,
                user_id=rec.user_id
            )
            for rec in CardModel.select()
        ]

    def list_by_user(self, user_id: int) -> List[Card]:
        return [
            Card(
                id=rec.id,
                number=rec.number,
                expiration_date=rec.expiration_date,
                cvv=rec.cvv,
                user_id=rec.user_id
            )
            for rec in CardModel.select().where(CardModel.user_id == user_id)
        ]

    def update(self,
               card_id: int,
               number: Optional[str] = None,
               expiration_date: Optional[str] = None,
               cvv: Optional[str] = None) -> Optional[Card]:
        """
        Actualiza sólo los campos provistos. Devuelve la tarjeta actualizada
        o None si el id no existe.
        """
        rec = CardModel.get_or_none(CardModel.id == card_id)
        if not rec:
            return None

        if number is not None:
            rec.number = number
        if expiration_date is not None:
            rec.expiration_date = expiration_date
        if cvv is not None:
            rec.cvv = cvv

        rec.save()  # actualiza updated_at
        return Card(
            id=rec.id,
            number=rec.number,
            expiration_date=rec.expiration_date,
            cvv=rec.cvv,
            user_id=rec.user_id
        )

    def delete(self, card_id: int) -> bool:
        rec = CardModel.get_or_none(CardModel.id == card_id)
        if not rec:
            return False
        rec.delete_instance()
        return True
