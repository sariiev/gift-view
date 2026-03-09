from sqlalchemy import String, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    rarity_percent: Mapped[float] = mapped_column(Float)

    sales = relationship("Sale", back_populates="symbol")
    gifts = relationship(
        "Gift",
        secondary="gifts_symbols",
        back_populates="symbols",
    )

    __table_args__ = (
        UniqueConstraint("name", "rarity_percent"),
    )
