import asyncio

from gift_view.db.base import Base
from gift_view.db.engine import engine

import gift_view.db.models.domain
import gift_view.db.models.aggregation


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
   asyncio.run(create_tables())