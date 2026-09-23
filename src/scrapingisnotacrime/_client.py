from __future__ import annotations

from types import TracebackType

import httpx

from ._config import resolve_config
from ._http import AsyncHttp, SyncHttp
from .resources import (
    Appstore,
    AsyncAppstore,
    AsyncBluesky,
    AsyncGithub,
    AsyncHackernews,
    AsyncInstagram,
    AsyncLinktree,
    AsyncTiktok,
    AsyncTwitch,
    AsyncYoutube,
    Bluesky,
    Github,
    Hackernews,
    Instagram,
    Linktree,
    Tiktok,
    Twitch,
    Youtube,
)


class ScrapingIsNotACrime:
    """Synchronous client. Use as a context manager, or call close() when done."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
    ) -> None:
        config = resolve_config(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._http = SyncHttp(config, http_client)
        self.instagram = Instagram(self._http)
        self.tiktok = Tiktok(self._http)
        self.youtube = Youtube(self._http)
        self.appstore = Appstore(self._http)
        self.github = Github(self._http)
        self.hackernews = Hackernews(self._http)
        self.bluesky = Bluesky(self._http)
        self.twitch = Twitch(self._http)
        self.linktree = Linktree(self._http)

    def close(self) -> None:
        """Closes the underlying HTTP client (unless you passed your own)."""
        self._http.close()

    def __enter__(self) -> ScrapingIsNotACrime:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()


class AsyncScrapingIsNotACrime:
    """Asynchronous client. Use with `async with`, or await aclose() when done."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        config = resolve_config(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries)
        self._http = AsyncHttp(config, http_client)
        self.instagram = AsyncInstagram(self._http)
        self.tiktok = AsyncTiktok(self._http)
        self.youtube = AsyncYoutube(self._http)
        self.appstore = AsyncAppstore(self._http)
        self.github = AsyncGithub(self._http)
        self.hackernews = AsyncHackernews(self._http)
        self.bluesky = AsyncBluesky(self._http)
        self.twitch = AsyncTwitch(self._http)
        self.linktree = AsyncLinktree(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncScrapingIsNotACrime:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        await self.aclose()
