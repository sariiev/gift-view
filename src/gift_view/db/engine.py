from sqlalchemy import create_engine

from gift_view.config import build_postgres_dsn

engine = create_engine(
    url=build_postgres_dsn(),
    echo=True,
    future=True
)