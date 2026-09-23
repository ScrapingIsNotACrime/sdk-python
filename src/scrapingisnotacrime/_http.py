from __future__ import annotations

import asyncio
import json
import math
import random as _random
import re
import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote, urlencode

import httpx

from ._config import Config
from ._errors import APIError, ConnectionError, ScrapingIsNotACrimeError, error_from_status, is_retryable
from ._retry import retry_delay
from ._version import __version__

QueryValue = str | int | None


@dataclass(frozen=True)
class Route:
    path: str
    query: Mapping[str, QueryValue] = field(default_factory=dict)


def segment(value: str | int | float) -> str:
    """Encodes one path segment; rejects values that would drop or climb a path level."""
    if isinstance(value, bool) or (isinstance(value, float) and not math.isfinite(value)):
        raise ValueError(f"Invalid path segment: {value!r} is not a valid value.")
    text = str(value)
    if text in ("", ".", ".."):
        raise ValueError(f"Invalid path segment: {text!r}.")
    return quote(text, safe="")


def build_url(base_url: str, path: str, query: Mapping[str, QueryValue]) -> str:
    params = [(key, str(value)) for key, value in query.items() if value is not None]
    return f"{base_url}{path}" + (f"?{urlencode(params)}" if params else "")


def _headers(config: Config) -> dict[str, str]:
    return {
        "X-Api-Key": config.api_key,
        "Accept": "application/json",
        "User-Agent": f"scrapingisnotacrime-python/{__version__}",
    }


def _snippet(text: str) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    return f"{flat[:200]}…" if len(flat) > 200 else flat


@dataclass
class _Failure:
    error: ScrapingIsNotACrimeError
    retry_after: str | None = None


def _interpret(response: httpx.Response) -> tuple[bool, Any]:
    """(True, data) for a valid envelope; (False, _Failure) otherwise."""
    request_id = response.headers.get("x-request-id")
    text = response.text
    try:
        body = json.loads(text) if text else None
    except ValueError:
        body = None
    envelope = body if isinstance(body, dict) else None

    if response.is_success:
        if envelope is not None and "data" in envelope:
            return True, envelope["data"]
        unexpected_body_error = APIError(
            f"Unexpected response body (HTTP {response.status_code}): {_snippet(text)}",
            status=response.status_code,
            request_id=request_id,
        )
        return False, _Failure(unexpected_body_error)

    message = envelope.get("message") if envelope is not None else None
    if not isinstance(message, str):
        message = f"HTTP {response.status_code}: {_snippet(text)}"
    status_error = error_from_status(response.status_code, message, request_id)
    return False, _Failure(status_error, response.headers.get("retry-after"))


def _connection_failure(error: httpx.HTTPError, timeout: float) -> _Failure:
    if isinstance(error, httpx.TimeoutException):
        return _Failure(ConnectionError(f"Request timed out after {timeout:g} s"))
    return _Failure(ConnectionError(f"Network error: {error}"))


class SyncHttp:
    def __init__(
        self,
        config: Config,
        http_client: httpx.Client | None = None,
        *,
        sleep: Callable[[float], object] = time.sleep,
        random: Callable[[], float] = _random.random,
    ) -> None:
        self._config = config
        self._client = http_client or httpx.Client()
        self._owns_client = http_client is None
        self._sleep = sleep
        self._random = random

    def get(self, route: Route) -> Any:
        url = build_url(self._config.base_url, route.path, route.query)
        attempt = 0
        while True:
            try:
                response = self._client.get(url, headers=_headers(self._config), timeout=self._config.timeout)
                ok, value = _interpret(response)
            except httpx.HTTPError as error:
                ok, value = False, _connection_failure(error, self._config.timeout)
            if ok:
                return value
            failure: _Failure = value
            if attempt >= self._config.max_retries or not is_retryable(failure.error):
                raise failure.error
            self._sleep(retry_delay(attempt, failure.retry_after, self._random))
            attempt += 1

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


class AsyncHttp:
    def __init__(
        self,
        config: Config,
        http_client: httpx.AsyncClient | None = None,
        *,
        sleep: Callable[[float], Awaitable[object]] = asyncio.sleep,
        random: Callable[[], float] = _random.random,
    ) -> None:
        self._config = config
        self._client = http_client or httpx.AsyncClient()
        self._owns_client = http_client is None
        self._sleep = sleep
        self._random = random

    async def get(self, route: Route) -> Any:
        url = build_url(self._config.base_url, route.path, route.query)
        attempt = 0
        while True:
            try:
                response = await self._client.get(
                    url, headers=_headers(self._config), timeout=self._config.timeout
                )
                ok, value = _interpret(response)
            except httpx.HTTPError as error:
                ok, value = False, _connection_failure(error, self._config.timeout)
            if ok:
                return value
            failure: _Failure = value
            if attempt >= self._config.max_retries or not is_retryable(failure.error):
                raise failure.error
            await self._sleep(retry_delay(attempt, failure.retry_after, self._random))
            attempt += 1

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
