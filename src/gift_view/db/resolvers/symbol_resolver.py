from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import SymbolRepository


class SymbolResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, rarity_percent: float) -> int:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        repository = SymbolRepository(session=session)
        symbol = await repository.get_or_create(name=name, rarity_percent=rarity_percent)

        self.cache[key] = symbol.id
        return symbol.id
