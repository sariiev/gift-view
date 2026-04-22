from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Symbol


class SymbolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_name_and_rarity_percent(self, name: str, rarity_percent: float) -> Optional[Symbol]:
        res = await self.session.execute(
            select(Symbol)
            .where(Symbol.name == name)
            .where(Symbol.rarity_percent == rarity_percent)
        )
        return res.scalar_one_or_none()


    def add(self, symbol: Symbol):
        self.session.add(symbol)
