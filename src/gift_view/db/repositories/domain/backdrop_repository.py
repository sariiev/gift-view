from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Backdrop


class BackdropRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_or_create(
            self,
            name: str,
            rarity_percent: float
    ) -> Backdrop:
        stmt = (
            insert(Backdrop)
            .values(name=name, rarity_percent=rarity_percent)
            .on_conflict_do_nothing(index_elements=["name", "rarity_percent"])
        )

        await self.session.execute(stmt)

        res = await self.session.execute(
            select(Backdrop)
            .where(Backdrop.name == name)
            .where(Backdrop.rarity_percent == rarity_percent)
        )
        return res.scalar_one()
