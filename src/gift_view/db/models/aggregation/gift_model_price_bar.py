from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, Integer, Float, Index
from sqlalchemy.orm import Mapped, mapped_column

from gift_view.db.base import Base


class GiftModelPriceBar(Base):
    __tablename__ = "gift_model_price_bars"

    gift_id: Mapped[int] = mapped_column(
        ForeignKey("gifts.id"),
        primary_key=True
    )

    model_id: Mapped[int] = mapped_column(
        ForeignKey("models.id"),
        primary_key=True
    )

    interval: Mapped[str] = mapped_column(
        String(3),
        primary_key=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True
    )

    sales_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    volume_usd: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    min_price_usd: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    max_price_usd: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    median_price_usd: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    __table_args__ = (
        Index(
            "idx_gift_model_price_bars_lookup",
            "gift_id",
            "model_id",
            "interval",
            "timestamp"
        ),
    )
