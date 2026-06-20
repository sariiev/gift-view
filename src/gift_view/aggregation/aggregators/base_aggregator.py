from abc import ABC, abstractmethod
from datetime import timedelta
from logging import getLogger
from typing import Callable, AsyncContextManager, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class BaseAggregator(ABC):
    def __init__(
            self,
            session_factory: Callable[[], AsyncContextManager[AsyncSession]],
            intervals: Optional[List[str]] = None
    ):
        self.session_factory = session_factory
        self.intervals = intervals or ["1h", "4h", "1d", "1w"]
        self.logger = getLogger(self.__class__.__name__)

    @abstractmethod
    async def aggregate_all(self):
        pass

    def interval_delta(self, interval: str) -> timedelta:
        if interval == "1h":
            return timedelta(hours=1)
        if interval == "4h":
            return timedelta(hours=4)
        if interval == "1d":
            return timedelta(days=1)
        if interval == "1w":
            return timedelta(weeks=1)
        raise ValueError(f"Unsupported interval: {interval}")