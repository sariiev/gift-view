from datetime import datetime

from sqlalchemy import ForeignKey, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class AssetPrice(Base):
    __tablename__ = "assets_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        index=True
    )
    price_usd: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True
    )

    asset = relationship("Asset")

    __table_args__ = (
        UniqueConstraint("asset_id", "timestamp"),
    )