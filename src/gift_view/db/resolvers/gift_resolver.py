from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.db.models.domain import Gift
from gift_view.db.repositories.domain import GiftRepository


class GiftResolver:
    def __init__(self):
        self.cache = {}


    async def resolve_id(self, session: AsyncSession, name: str, create: bool) -> Optional[int]:
        if name in self.cache:
            return self.cache[name]

        repository = GiftRepository(session=session)
        gift = await repository.get_by_name(name=name)

        if gift:
            self.cache[name] = gift.id
            return gift.id

        if not create:
            return None

        gift = Gift(name=name)

        repository.add(gift)

        await session.flush()

        self.cache[name] = gift.id
        return gift.id