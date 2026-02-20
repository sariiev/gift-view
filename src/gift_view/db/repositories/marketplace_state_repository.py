from typing import Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Marketplace, MarketplaceState


class MarketplaceStateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_marketplace(self, marketplace: Marketplace) -> Optional[MarketplaceState]:
        res = await self.session.execute(
            select(MarketplaceState)
            .where(MarketplaceState.marketplace_id== marketplace.id)
        )
        return res.scalar_one_or_none()


    async def upsert(
            self,
            marketplace: Marketplace,
            state: Dict
    ) -> MarketplaceState:
        existing = await self.get_by_marketplace(marketplace)

        if existing:
            existing.state = state
            return existing

        new_state = MarketplaceState(
            marketplace_id=Marketplace.id,
            state=state
        )
        self.session.add(new_state)
        await self.session.flush()
        return new_state

