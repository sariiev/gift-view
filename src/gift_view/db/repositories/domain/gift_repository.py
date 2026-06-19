from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Gift


class GiftRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_name(self, name: str) -> Optional[Gift]:
        res = await self.session.execute(
            select(Gift)
            .where(Gift.name == name)
        )
        return res.scalar_one_or_none()


    async def get_all(self) -> List[Gift]:
        res = await self.session.execute(
            select(Gift)
        )
        return list(res.scalars().all())


    def add(self, gift: Gift):
        self.session.add(gift)
