from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.repositories.domain import GiftRepository


class GiftResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str) -> int:
        if name in self.cache:
            return self.cache[name]

        repository = GiftRepository(session=session)
        gift = await repository.get_or_create(name=name)

        self.cache[name] = gift.id
        return gift.id
