from datetime import datetime, timezone
from typing import Dict, List

from gift_view.db.models import AssetPrice


class BinancePriceParser:
    @staticmethod
    def parse_klines(klines: List[Dict], asset_id: int) -> List[AssetPrice]:
        result = []

        for kline in klines:
            open_time_ms = kline[0]
            open_price = float(kline[1])

            dt = datetime.fromtimestamp(
                open_time_ms / 1000,
                tz=timezone.utc
            )

            result.append(
                AssetPrice(
                    asset_id=asset_id,
                    timestamp=dt,
                    price_usd=open_price
                )
            )

        return result