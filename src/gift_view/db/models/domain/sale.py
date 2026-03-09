from datetime import datetime

from sqlalchemy import ForeignKey, Float, DateTime, UniqueConstraint, String, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gift_view.db.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    marketplace_id: Mapped[int] = mapped_column(
        ForeignKey("marketplaces.id"),
        index=True
    )
    marketplace_sale_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    gift_id: Mapped[int] = mapped_column(
        ForeignKey("gifts.id"),
        index=True
    )
    gift_number: Mapped[int]
    model_id: Mapped[int] = mapped_column(
        ForeignKey("models.id"),
        index=True
    )
    backdrop_id: Mapped[int] = mapped_column(
        ForeignKey("backdrops.id"),
        index=True
    )
    symbol_id: Mapped[int] = mapped_column(
        ForeignKey("symbols.id"),
        index=True
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id"),
        index=True
    )
    price_native: Mapped[float] = mapped_column(Float)
    price_usd: Mapped[float] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True
    )

    marketplace = relationship("Marketplace", back_populates="sales")
    gift = relationship("Gift", back_populates="sales")
    model = relationship("Model", back_populates="sales")
    backdrop = relationship("Backdrop", back_populates="sales")
    symbol = relationship("Symbol", back_populates="sales")

    __table_args__ = (
        UniqueConstraint("marketplace_id", "marketplace_sale_id"),
        Index(
            "idx_sales_price_usd_null_timestamp",
            "timestamp",
            postgresql_where=text("price_usd IS NULL")
        )
    )
