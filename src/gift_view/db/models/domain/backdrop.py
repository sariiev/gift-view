from sqlalchemy import String, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class Backdrop(Base):
    __tablename__ = "backdrops"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    rarity_percent: Mapped[float] = mapped_column(Float)

    sales = relationship("Sale", back_populates="backdrop")
    gifts = relationship(
        "Gift",
        secondary="gifts_backdrops",
        back_populates="backdrops",
    )

    __table_args__ = (
        UniqueConstraint("name", "rarity_percent"),
    )
