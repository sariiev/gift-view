from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class RarityTier(Base):
    __tablename__ = "rarity_tiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    models = relationship("Model", back_populates="rarity_tier")
