import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import gift_view.db.models

from gift_view.db.base import Base


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with Session() as session:
        yield session

    await engine.dispose()
