from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories import BackdropRepository


class BackdropResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, rarity_percent: float) -> int:
        key = (name, rarity_percent)
        if key in self.cache:
            return self.cache[key]

        repository = BackdropRepository(session=session)
        backdrop = await repository.get_or_create(name=name, rarity_percent=rarity_percent)

        self.cache[key] = backdrop.id
        return backdrop.id
