from abc import ABC, abstractmethod
from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from gift_view.ingestion.clients import BaseMarketplaceClient
from gift_view.ingestion.parsers import BaseMarketplaceParser


class BaseMarketplaceRunner(ABC):
    def __init__(
            self,
            marketplace_client: BaseMarketplaceClient,
            marketplace_parser: BaseMarketplaceParser,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            delay: int
    ):
        self.marketplace_client = marketplace_client
        self.marketplace_parser = marketplace_parser
        self.session_factory = session_factory
        self.delay = delay


    @abstractmethod
    async def fetch_all(self):
        pass
