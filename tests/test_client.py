from __future__ import annotations

import httpx
import pytest

from scrapingisnotacrime import AsyncScrapingIsNotACrime, ScrapingIsNotACrime

NAMESPACES = [
    "instagram",
    "tiktok",
    "youtube",
    "appstore",
    "github",
    "hackernews",
    "bluesky",
    "twitch",
    "linktree",
]


def test_missing_key_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SCRAPINGISNOTACRIME_API_KEY", raising=False)
    with pytest.raises(ValueError, match="SCRAPINGISNOTACRIME_API_KEY"):
        ScrapingIsNotACrime()
    with pytest.raises(ValueError, match="SCRAPINGISNOTACRIME_API_KEY"):
        AsyncScrapingIsNotACrime()


def test_namespaces() -> None:
    client = ScrapingIsNotACrime("sinac_test")
    for name in NAMESPACES:
        assert getattr(client, name) is not None
    client.close()


def test_close_leaves_user_client_open() -> None:
    user_client = httpx.Client()
    with ScrapingIsNotACrime("sinac_test", http_client=user_client):
        pass
    assert not user_client.is_closed
    user_client.close()
    owned = ScrapingIsNotACrime("sinac_test")
    owned.close()
    assert owned._http._client.is_closed


def test_sync_invalid_argument_raises_at_call() -> None:
    client = ScrapingIsNotACrime("sinac_test")
    with pytest.raises(ValueError, match="Invalid path segment"):
        client.instagram.profile("")
    client.close()


async def test_async_invalid_argument_raises_on_await() -> None:
    async with AsyncScrapingIsNotACrime("sinac_test") as client:
        coroutine = client.instagram.profile("")  # must not raise here
        with pytest.raises(ValueError, match="Invalid path segment"):
            await coroutine
        with pytest.raises(ValueError):
            await client.github.followers("..")
