from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Marketplace


class MarketplaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_name(self, name: str) -> Optional[Marketplace]:
        res = await self.session.execute(
            select(Marketplace)
            .where(Marketplace.name == name)
        )
        return res.scalar_one_or_none()


    def add(self, marketplace: Marketplace):
        self.session.add(marketplace)
