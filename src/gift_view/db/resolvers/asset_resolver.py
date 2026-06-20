from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Asset
from gift_view.db.repositories.domain import AssetRepository


class AssetResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, symbol: str, create: bool) -> Optional[int]:
        symbol = symbol.upper().strip()

        if symbol in self.cache:
            return self.cache[symbol]

        repository = AssetRepository(session)
        asset = await repository.get_by_symbol(symbol=symbol)

        if asset:
            self.cache[symbol] = asset.id
            return asset.id

        if not create:
            return None

        asset = Asset(symbol=symbol)

        repository.add(asset)

        await session.flush()

        self.cache[symbol] = asset.id
        return asset.id
