from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models import Symbol


class SymbolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_or_create(self, name: str, rarity_percent: float) -> Symbol:
        stmt = (
            insert(Symbol)
            .values(name=name, rarity_percent=rarity_percent)
            .on_conflict_do_nothing(index_elements=["name", "rarity_percent"])
        )

        await self.session.execute(stmt)

        res = await self.session.execute(
            select(Symbol)
            .where(Symbol.name == name)
            .where(Symbol.rarity_percent == rarity_percent)
        )
        return res.scalar_one()
