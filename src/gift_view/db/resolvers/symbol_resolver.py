from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Symbol
from gift_view.db.repositories.domain import SymbolRepository


class SymbolResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, rarity_percent: float, create: bool) -> Optional[int]:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        repository = SymbolRepository(session=session)
        symbol = await repository.get_by_name_and_rarity_percent(name=name, rarity_percent=rarity_percent)

        if symbol:
            self.cache[key] = symbol.id
            return symbol.id

        if not create:
            return None

        symbol = Symbol(name=name, rarity_percent=rarity_percent)

        repository.add(symbol)

        await session.flush()

        self.cache[key] = symbol.id
        return symbol.id
