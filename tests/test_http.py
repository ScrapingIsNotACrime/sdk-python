from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from scrapingisnotacrime import __version__
from scrapingisnotacrime._config import resolve_config
from scrapingisnotacrime._errors import (
    APIError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ScrapingIsNotACrimeError,
    UpstreamError,
)
from scrapingisnotacrime._http import AsyncHttp, Route, SyncHttp, build_url, segment

Reply = tuple[int, Any, dict[str, str]] | Exception


class Recorder:
    """httpx transport handler answering with scripted replies, recording requests."""

    def __init__(self, replies: list[Reply]) -> None:
        self.replies = replies
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        status, body, headers = reply
        content = body if isinstance(body, str) else json.dumps(body)
        return httpx.Response(status, content=content, headers=headers)


def ok(data: Any) -> Reply:
    return (200, {"message": "ok", "data": data}, {})


def sync_http(replies: list[Reply], **options: Any) -> tuple[SyncHttp, Recorder, list[float]]:
    recorder = Recorder(replies)
    sleeps: list[float] = []
    config = resolve_config(api_key="sinac_test", env={}, **options)
    http = SyncHttp(
        config,
        httpx.Client(transport=httpx.MockTransport(recorder)),
        sleep=sleeps.append,
        random=lambda: 0.5,
    )
    return http, recorder, sleeps


def async_http(replies: list[Reply], **options: Any) -> tuple[AsyncHttp, Recorder, list[float]]:
    recorder = Recorder(replies)
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    config = resolve_config(api_key="sinac_test", env={}, **options)
    http = AsyncHttp(
        config,
        httpx.AsyncClient(transport=httpx.MockTransport(recorder)),
        sleep=sleep,
        random=lambda: 0.5,
    )
    return http, recorder, sleeps


def test_segment_encodes_and_rejects() -> None:
    assert segment("a/b") == "a%2Fb"
    assert segment("josé#1") == "jos%C3%A9%231"
    assert segment("highlight:1") == "highlight%3A1"
    assert segment(8863) == "8863"
    for bad in ("", ".", "..", float("nan"), float("inf"), True):
        with pytest.raises(ValueError, match="Invalid path segment"):
            segment(bad)


def test_build_url() -> None:
    query: dict[str, str | int | None] = {"q": "stars:>10 language:php", "limit": 5, "page": None}
    assert (
        build_url("https://x.test/v1", "/github/repositories", query)
        == "https://x.test/v1/github/repositories?q=stars%3A%3E10+language%3Aphp&limit=5"
    )
    assert build_url("https://x.test/v1", "/x", {}) == "https://x.test/v1/x"


def test_sends_headers_and_unwraps_data() -> None:
    http, recorder, _ = sync_http([ok({"a": 1})])
    assert http.get(Route("/linktree/profiles/x")) == {"a": 1}
    request = recorder.requests[0]
    assert request.method == "GET"
    assert str(request.url) == "https://api.scrapingisnotacrime.com/v1/linktree/profiles/x"
    assert request.headers["x-api-key"] == "sinac_test"
    assert request.headers["accept"] == "application/json"
    assert request.headers["user-agent"] == f"scrapingisnotacrime-python/{__version__}"


def test_error_mapping_keeps_message_and_request_id() -> None:
    http, _, _ = sync_http([(404, {"message": "Profile not found."}, {"x-request-id": "r-9"})])
    with pytest.raises(NotFoundError) as info:
        http.get(Route("/x"))
    assert info.value.status == 404
    assert info.value.message == "Profile not found."
    assert info.value.request_id == "r-9"


@pytest.mark.parametrize("status", [400, 401, 402, 404])
def test_no_retry_for_client_errors(status: int) -> None:
    http, recorder, _ = sync_http([(status, {"message": "no"}, {}), ok(1)])
    with pytest.raises(ScrapingIsNotACrimeError):
        http.get(Route("/x"))
    assert len(recorder.requests) == 1


def test_retries_429_and_502_then_raises_last() -> None:
    http, recorder, sleeps = sync_http(
        [(429, {"message": "rl"}, {}), (502, {"message": "up"}, {}), (429, {"message": "rl"}, {})]
    )
    with pytest.raises(RateLimitError):
        http.get(Route("/x"))
    assert len(recorder.requests) == 3
    assert sleeps == [0.25, 0.5]


def test_retry_after_and_success_after_retry() -> None:
    http, recorder, sleeps = sync_http([(502, {"message": "up"}, {"retry-after": "2"}), ok("done")])
    assert http.get(Route("/x")) == "done"
    assert sleeps == [2.0]
    assert len(recorder.requests) == 2


def test_max_retries_zero() -> None:
    http, recorder, _ = sync_http([(502, {"message": "x"}, {}), ok(1)], max_retries=0)
    with pytest.raises(UpstreamError):
        http.get(Route("/x"))
    assert len(recorder.requests) == 1


def test_network_errors_and_timeouts_become_connection_error() -> None:
    http, recorder, _ = sync_http([httpx.ConnectError("refused"), ok(1)])
    assert http.get(Route("/x")) == 1
    assert len(recorder.requests) == 2
    http, _, _ = sync_http([httpx.ReadTimeout("slow")] * 3)
    with pytest.raises(ConnectionError, match="timed out after 30 s") as info:
        http.get(Route("/x"))
    assert info.value.status is None


def test_2xx_without_envelope_is_api_error() -> None:
    http, _, _ = sync_http([(200, "<html>proxy</html>", {})])
    with pytest.raises(APIError, match="Unexpected response body"):
        http.get(Route("/x"))
    http, _, _ = sync_http([(200, {"message": "ok"}, {})])
    with pytest.raises(APIError):
        http.get(Route("/x"))


def test_non_json_error_body_keeps_status_class() -> None:
    http, _, _ = sync_http([(502, "<html>Bad Gateway</html>", {})] * 3)
    with pytest.raises(UpstreamError, match=r"HTTP 502: <html>Bad Gateway</html>"):
        http.get(Route("/x"))
    http, _, _ = sync_http([(500, "Internal Server Error", {})])
    with pytest.raises(APIError, match="HTTP 500: Internal Server Error"):
        http.get(Route("/x"))


def test_does_not_close_a_user_client() -> None:
    client = httpx.Client(transport=httpx.MockTransport(Recorder([ok(1)])))
    http = SyncHttp(resolve_config(api_key="k", env={}), client)
    http.close()
    assert not client.is_closed


async def test_async_core_mirrors_sync() -> None:
    http, recorder, sleeps = async_http([(429, {"message": "rl"}, {}), ok({"b": 2})])
    assert await http.get(Route("/y", {"limit": 3})) == {"b": 2}
    assert str(recorder.requests[0].url) == "https://api.scrapingisnotacrime.com/v1/y?limit=3"
    assert sleeps == [0.25]
    http, _, _ = async_http([(401, {"message": "Invalid API key."}, {})])
    with pytest.raises(AuthenticationError):
        await http.get(Route("/y"))
    await http.aclose()
