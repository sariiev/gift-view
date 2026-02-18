import asyncio
from abc import ABC
from typing import Optional, Dict, Any

from curl_cffi import requests
from curl_cffi.requests.exceptions import Timeout, DNSError, ConnectionError as CurlConnectionError


class BaseClient(ABC):
    def __init__(
            self,
            base_url: str,
            max_retries: int = 5,
            retry_delay: int = 5,
            rate_limit_delay: int = 900,
            impersonate: str = "chrome136"
    ):
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self.impersonate = impersonate


    async def _request(
            self,
            method: str,
            path: str,
            headers: Optional[Dict] = None,
            json: Optional[Dict] = None,
            params: Optional[Dict] = None,
            timeout: int = 10,
            **kwargs
    ) -> Optional[Any]:
        url = f"{self.base_url}/{path.lstrip("/")}"
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await asyncio.to_thread(
                    requests.request,
                    method=method,
                    url=url,
                    headers=headers,
                    json=json,
                    params=params,
                    impersonate=self.impersonate,
                    timeout = timeout,
                    **kwargs
                )

                status_code = response.status_code

                if status_code == 200:
                    return response.json()
                elif status_code == 403:
                    raise RuntimeError(f"403 Forbidden: {url}")
                elif status_code == 429:
                    await asyncio.sleep(self.rate_limit_delay)
                elif 500 <= status_code < 600:
                    if attempt == self.max_retries:
                        raise RuntimeError(f"Server error: {status_code}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise RuntimeError(f"Unexpected status ({status_code}): {url}")
            except (Timeout, DNSError, CurlConnectionError):
                if attempt == self.max_retries:
                    raise
                await asyncio.sleep(self.retry_delay)
        return None


    async def get(
            self,
            path: str,
            headers: Optional[Dict] = None,
            json: Optional[Dict] = None,
            params: Optional[Dict] = None,
            timeout: int = 10,
            **kwargs
    ):
        return await self._request(
            "GET",
            path=path,
            headers=headers,
            json=json,
            params=params,
            timeout=timeout,
            **kwargs
        )


    async def post(
            self,
            path: str,
            headers: Optional[Dict] = None,
            json: Optional[Dict] = None,
            params: Optional[Dict] = None,
            timeout: int = 10,
            **kwargs
    ):
        return await self._request(
            "POST",
            path=path,
            headers=headers,
            json=json,
            params=params,
            timeout=timeout,
            **kwargs
        )