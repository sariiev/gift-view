from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Marketplace
from gift_view.db.repositories.domain import MarketplaceRepository


class MarketplaceResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, create: bool) -> Optional[int]:
        if name in self.cache:
            return self.cache[name]

        repository = MarketplaceRepository(session=session)
        marketplace = await repository.get_by_name(name=name)

        if marketplace:
            self.cache[name] = marketplace.id
            return marketplace.id

        if not create:
            return None

        marketplace = Marketplace(name=name)

        repository.add(marketplace)

        await session.flush()

        self.cache[name] = marketplace.id
        return marketplace.id
