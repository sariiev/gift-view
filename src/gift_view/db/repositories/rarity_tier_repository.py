from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import RarityTier


class RarityTierRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_name(self, name: str) -> Optional[RarityTier]:
        res = await self.session.execute(
            select(RarityTier)
            .where(RarityTier.name == name)
        )
        return res.scalar_one_or_none()


    def add(self, rarity_tier: RarityTier):
        self.session.add(rarity_tier)
