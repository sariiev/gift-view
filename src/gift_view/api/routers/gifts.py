from datetime import datetime
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException
from fastapi import Query

from gift_view.db.repositories.aggregation import GiftPriceBarRepository, GiftModelPriceBarRepository
from gift_view.db.repositories.domain import GiftRepository, ModelRepository
from gift_view.db.resolvers import GiftResolver, ModelResolver
from gift_view.db.session import get_session

router = APIRouter(prefix="/gifts")

gift_resolver = GiftResolver()
model_resolver = ModelResolver()

@router.get("")
async def get_gifts():
    async with get_session() as session:
        repository = GiftRepository(session=session)

        gifts = await repository.get_all()

        return [
            {"name": gift.name}
            for gift in gifts
        ]

@router.get("/{gift_name}/models")
async def get_models(
        gift_name: str
):
    async with get_session() as session:
        gift_id = await gift_resolver.resolve_id(session=session, name=gift_name, create=False)
        if gift_id is None:
            raise HTTPException(status_code=404, detail="Gift not found")

        repository = ModelRepository(session=session)

        models = await repository.get_by_gift_id(gift_id=gift_id)

        return [
            {
                "name": model.name,
                "rarity_percent": model.rarity_percent
            }
            for model in models
        ]


@router.get("/{gift_name}/price-history")
async def get_price_history(
        gift_name: str,
        model_name: Optional[str] = None,
        interval: Literal["1h", "4h", "1d", "1w"] = "1h",
        limit: int = Query(200, ge=1, le=1000),
        before: Optional[datetime] = None
):
    async with get_session() as session:
        gift_id = await gift_resolver.resolve_id(session=session, name=gift_name, create=False)
        if gift_id is None:
            raise HTTPException(status_code=404, detail="Gift not found")

        if model_name:
            model_id = await model_resolver.resolve_id(session=session, gift_id=gift_id, name=model_name, create=False)
            if model_id is None:
                raise HTTPException(status_code=404, detail="Model not found")

            repository = GiftModelPriceBarRepository(session=session)

            bars = await repository.get_bars(
                gift_id=gift_id,
                model_id=model_id,
                interval=interval,
                limit=limit,
                before=before
            )
        else:
            repository = GiftPriceBarRepository(session=session)

            bars = await repository.get_bars(
                gift_id=gift_id,
                interval=interval,
                limit=limit,
                before=before
            )

        bars = list(reversed(bars))

        return [
            {
                "timestamp": bar.timestamp,
                "min_price": bar.min_price_usd,
                "median_price": bar.median_price_usd,
                "max_price": bar.max_price_usd,
                "volume": bar.volume_usd,
                "sales": bar.sales_count
            }
            for bar in bars
        ]
