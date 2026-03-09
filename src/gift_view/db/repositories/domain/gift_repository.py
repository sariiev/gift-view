from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Gift


class GiftRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_or_create(self, name: str) -> Gift:
        stmt = insert(Gift).values(name=name).on_conflict_do_nothing(index_elements=["name"])

        await self.session.execute(stmt)

        res = await self.session.execute(
            select(Gift)
            .where(Gift.name == name)
        )
        return res.scalar_one()
