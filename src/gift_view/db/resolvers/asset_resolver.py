from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories import AssetRepository


class AssetResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, symbol: str) -> int:
        symbol = symbol.upper().strip()

        if symbol in self.cache:
            return self.cache[symbol]

        repository = AssetRepository(session)
        asset = await repository.get_or_create(symbol=symbol)

        self.cache[symbol] = asset.id
        return asset.id
