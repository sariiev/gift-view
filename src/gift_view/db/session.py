from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker

from gift_view.db.engine import engine

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

@asynccontextmanager
async def get_session():
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
