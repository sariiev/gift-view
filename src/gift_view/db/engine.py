from sqlalchemy.ext.asyncio import create_async_engine

from gift_view.config import build_postgres_dsn

engine = create_async_engine(
    url=build_postgres_dsn(),
    echo=False,
    future=True
)