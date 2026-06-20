from contextlib import asynccontextmanager

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import gift_view.db.models

from gift_view.db.base import Base


@pytest_asyncio.fixture
async def session(session_factory):
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@pytest_asyncio.fixture
async def session_factory():
    engine = create_async_engine(
        "sqlite+aiosqlite:///file::memory:?cache=shared",
        connect_args={"uri": True},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(bind=engine, expire_on_commit=False)

    @asynccontextmanager
    async def _session_factory():
        async with Session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    yield _session_factory

    await engine.dispose()