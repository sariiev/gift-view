from sqlalchemy import ForeignKey, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True)
    gift_id: Mapped[int] = mapped_column(
        ForeignKey("gifts.id")
    )
    name: Mapped[str] = mapped_column(String(50))
    is_crafted: Mapped[bool] = mapped_column(Boolean)
    rarity_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    rarity_tier: Mapped[str | None] = mapped_column(String(20), nullable=True)

    gift = relationship("Gift", back_populates="models")
    sales = relationship("Sale", back_populates="model")

