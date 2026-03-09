from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Model


class ModelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_or_create(
            self,
            gift_id: int,
            name: str,
            is_crafted: bool,
            rarity_percent: float
    ) -> Model:
        stmt = (
            insert(Model)
            .values(gift_id=gift_id, name=name, is_crafted=is_crafted, rarity_percent=rarity_percent)
            .on_conflict_do_nothing(index_elements=["gift_id", "name", "is_crafted"])
        )

        await self.session.execute(stmt)

        res = await self.session.execute(
            select(Model)
            .where(Model.gift_id == gift_id)
            .where(Model.name == name)
            .where(Model.is_crafted == is_crafted)
            .where(Model.rarity_percent == rarity_percent)
        )
        return res.scalar_one()
