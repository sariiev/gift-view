from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Backdrop
from gift_view.db.repositories.domain import BackdropRepository


class BackdropResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, rarity_percent: float, create: bool) -> Optional[int]:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        repository = BackdropRepository(session=session)
        backdrop = await repository.get_by_name_and_rarity_percent(name=name, rarity_percent=rarity_percent)

        if backdrop:
            self.cache[key] = backdrop.id
            return backdrop.id

        if not create:
            return

        backdrop = Backdrop(name=name, rarity_percent=rarity_percent)

        repository.add(backdrop)

        await session.flush()

        self.cache[key] = backdrop.id
        return backdrop.id
