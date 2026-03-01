from typing import Optional, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import MarketplaceState


class MarketplaceStateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_marketplace_id(self, marketplace_id: int) -> Optional[MarketplaceState]:
        res = await self.session.execute(
            select(MarketplaceState)
            .where(MarketplaceState.marketplace_id== marketplace_id)
        )
        return res.scalar_one_or_none()


    async def upsert(
            self,
            marketplace_id: int,
            state: Dict
    ):
        existing = await self.get_by_marketplace_id(marketplace_id)

        if existing:
            existing.state = state
            return existing

        new_state = MarketplaceState(
            marketplace_id=marketplace_id,
            state=state
        )
        self.session.add(new_state)
