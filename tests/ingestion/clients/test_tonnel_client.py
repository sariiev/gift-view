import pytest

from gift_view.config import TonnelConfig, load_tonnel_config
from gift_view.ingestion.clients import TonnelClient


class TestableTonnelClient(TonnelClient):
    def __init__(self, config):
        super().__init__(config=config)
        self.called_with = None


    async def post(self, **kwargs):
        self.called_with = kwargs
        return [{"sale_id": "1"}]


@pytest.mark.asyncio
async def test_fetch_sales_builds_correct_request():
    client = TestableTonnelClient(config=TonnelConfig(auth_data="123"))

    state = {"page": 10, "limit": 25}

    result = await client.fetch_sales(state=state)

    assert result == [{"sale_id": "1"}]

    payload = client.called_with["json"]

    assert payload["page"] == 10
    assert payload["limit"] == 25
    assert payload["authData"] == "123"
    assert payload["sort"] == {"timestamp": 1}
    assert payload["type"] == ["SALE", "INTERNAL_SALE"]

    assert client.called_with["timeout"] == 10


@pytest.mark.asyncio
async def test_fetch_sales_uses_defaults():
    client = TestableTonnelClient(config=TonnelConfig(auth_data="123"))

    await client.fetch_sales(state={})

    payload = client.called_with["json"]

    assert payload["page"] == 1
    assert payload["limit"] == 50


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_tonnel_api():
    config = load_tonnel_config()
    client = TonnelClient(config=config)

    result = await client.fetch_sales({"page": 1, "limit": 5})

    assert isinstance(result, list)
    assert len(result) == 5

    sale = result[0]

    assert sale["_id"] is not None
    assert sale["gift_id"] is not None
    assert sale["gift_num"] is not None
    assert sale["gift_name"] is not None
    assert sale["price"] is not None
    assert sale["timestamp"] is not None
    assert sale["model"] is not None
    assert sale["symbol"] is not None
    assert sale["backdrop"] is not None
    assert sale["asset"] is not None