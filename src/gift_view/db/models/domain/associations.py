from sqlalchemy import Table, Column, ForeignKey

from gift_view.db.base import Base

gifts_backdrops = Table(
    "gifts_backdrops",
    Base.metadata,
    Column("gift_id", ForeignKey("gifts.id"), primary_key=True),
    Column("backdrop_id", ForeignKey("backdrops.id"), primary_key=True)
)

gifts_symbols = Table(
    "gifts_symbols",
    Base.metadata,
    Column("gift_id", ForeignKey("gifts.id"), primary_key=True),
    Column("symbol_id", ForeignKey("symbols.id"), primary_key=True)
)