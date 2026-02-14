from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from gift_view.db.models import Symbol


class SymbolRepository:
    def __init__(self, session: Session):
        self.session = session


    def get_by_name_and_rarity_percent(self, name: str, rarity_percent: float) -> Optional[Symbol]:
        return self.session.execute(
            select(Symbol)
            .where(Symbol.name == name)
            .where(Symbol.rarity_percent == rarity_percent)
        ).scalar_one_or_none()


    def add(self, symbol: Symbol):
        self.session.add(symbol)
