import asyncio
from datetime import timedelta, datetime

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG


default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


def ingest_tonnel():
    from gift_view.config import load_tonnel_config, setup_logging
    from gift_view.db.resolvers import (
        MarketplaceResolver, GiftResolver, ModelResolver,
        BackdropResolver, SymbolResolver, AssetResolver
    )
    from gift_view.db.session import get_session
    from gift_view.ingestion.clients import TonnelClient
    from gift_view.ingestion.parsers import TonnelParser
    from gift_view.ingestion.runners import TonnelRunner

    setup_logging()

    async def _run():
        client = TonnelClient(
            config=load_tonnel_config()
        )
        parser = TonnelParser(
            marketplace_resolver=MarketplaceResolver(),
            gift_resolver=GiftResolver(),
            model_resolver=ModelResolver(),
            backdrop_resolver=BackdropResolver(),
            symbol_resolver=SymbolResolver(),
            asset_resolver=AssetResolver()
        )
        runner = TonnelRunner(
            marketplace_client=client,
            marketplace_parser=parser,
            session_factory=get_session
        )
        await runner.init()
        await runner.fetch_all()

    asyncio.run(_run())


fetch_token_prices_interval = "1h"

def fetch_tokens_prices():
    from gift_view.config import setup_logging
    from gift_view.db.session import get_session
    from gift_view.ingestion.clients import BinanceClient
    from gift_view.ingestion.parsers import BinancePriceParser
    from gift_view.ingestion.runners import BinanceRunner

    setup_logging()

    async def _run():
        client = BinanceClient()
        parser = BinancePriceParser()
        runner = BinanceRunner(
            client=client,
            parser=parser,
            session_factory=get_session,
            interval=fetch_token_prices_interval
        )
        await runner.run_once()

    asyncio.run(_run())


sync_usd_prices_interval = "1h"
sync_usd_prices_batch_size = 1000

def sync_usd_prices():
    from gift_view.config import setup_logging
    from gift_view.db.session import get_session
    from gift_view.sync.syncers import UsdPriceSyncer
    from gift_view.utils import to_interval_seconds

    setup_logging()

    async def _run():
        syncer = UsdPriceSyncer(
            session_factory=get_session,
            interval=to_interval_seconds(sync_usd_prices_interval),
            batch_size=sync_usd_prices_batch_size
        )

        await syncer.sync_all()

    asyncio.run(_run())


def run_aggregations():
    from gift_view.aggregation.aggregators import GiftPriceBarAggregator, GiftModelPriceBarAggregator
    from gift_view.config import setup_logging
    from gift_view.db.session import get_session

    setup_logging()

    async def _run():
        gift_price_bar_aggregator = GiftPriceBarAggregator(
        session_factory=get_session
        )

        gift_model_price_bar_aggregator = GiftModelPriceBarAggregator(
            session_factory=get_session
        )

        await asyncio.gather(
            gift_price_bar_aggregator.aggregate_all(),
            gift_model_price_bar_aggregator.aggregate_all()
        )

    asyncio.run(_run())

with DAG(
    dag_id="ingest_marketplaces",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    max_active_runs=1
) as ingest_dag:
    PythonOperator(
        task_id="ingest_tonnel",
        python_callable=ingest_tonnel
    )

with DAG(
    dag_id="sync_prices_run_aggregations",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="0 * * * *",
    catchup=False,
    max_active_runs=1
) as dag:
    t1_fetch_tokens_prices = PythonOperator(
        task_id="fetch_tokens_prices",
        python_callable=fetch_tokens_prices
    )

    t2_sync_usd_prices = PythonOperator(
        task_id="sync_usd_prices",
        python_callable=sync_usd_prices
    )

    t3_run_aggregations = PythonOperator(
        task_id="run_aggregations",
        python_callable=run_aggregations
    )

    t1_fetch_tokens_prices >> t2_sync_usd_prices >> t3_run_aggregations
