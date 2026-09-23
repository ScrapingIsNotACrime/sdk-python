from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode

import httpx
import pytest

from scrapingisnotacrime import AsyncPage, AsyncScrapingIsNotACrime, Page, ScrapingIsNotACrime

FIXTURES = Path(__file__).parent / "fixtures"


def normalize(request: str) -> str:
    path, _, query = request.partition("?")
    params = urlencode(parse_qsl(query, keep_blank_values=True))
    return f"{path}?{params}" if params else path


def fixture_data(fixture_id: str) -> Any:
    return json.loads((FIXTURES / f"{fixture_id}.json").read_text())["response"]["data"]


PLACEHOLDER: dict[str, Any] = {
    "instagram.media": {"id": "1", "shortcode": "C8xQz1aP9Kv"},
    "tiktok.video": {"id": "7300000000000000000"},
    "github.following": {"items": [], "total": None, "has_more": False},
    "hackernews.comments": {"items": [], "total": 0, "page": 0, "has_more": False},
}

# (namespace.method, positional args, keyword args, fixture id or None, expected request)
CASES: list[tuple[str, tuple[Any, ...], dict[str, Any], str | None, str]] = [
    ("instagram.profile", ("instagram",), {}, "ig-profile", "/instagram/profile/instagram"),
    ("instagram.contact", ("cafedaesquina",), {}, "ig-contact", "/instagram/profile/cafedaesquina/contact"),
    (
        "instagram.latest_posts",
        ("instagram",),
        {},
        "ig-timeline",
        "/instagram/profile/instagram/timeline/latest",
    ),
    (
        "instagram.posts",
        ("nasa",),
        {"count": 12, "cursor": "3950671748375397992_528817151"},
        "ig-timeline-paged",
        "/instagram/profile/nasa/timeline?count=12&cursor=3950671748375397992_528817151",
    ),
    ("instagram.highlights", ("nasa",), {}, "ig-highlights", "/instagram/profile/nasa/highlights"),
    (
        "instagram.highlight",
        ("highlight:18201653992314974",),
        {},
        "ig-highlight-content",
        "/instagram/highlights/highlight%3A18201653992314974",
    ),
    (
        "instagram.media_by_id",
        ("instagram", "3123456789012345678"),
        {},
        "ig-media-by-id",
        "/instagram/profile/instagram/media/3123456789012345678",
    ),
    ("instagram.media", ("C8xQz1aP9Kv",), {}, None, "/instagram/media/C8xQz1aP9Kv"),
    (
        "instagram.download",
        ("DbtErSrlB2J",),
        {},
        "ig-media-download",
        "/instagram/media/DbtErSrlB2J/download",
    ),
    (
        "instagram.shortcode_to_id",
        ("Dbn-XJhk0_-",),
        {},
        "ig-shortcode-to-id",
        "/instagram/media/Dbn-XJhk0_-/id",
    ),
    (
        "instagram.id_to_shortcode",
        ("3956405067326902270",),
        {},
        "ig-id-to-shortcode",
        "/instagram/media/id/3956405067326902270",
    ),
    ("instagram.reel", ("DyKlMnOpQrS",), {}, "ig-reels", "/instagram/reels/DyKlMnOpQrS"),
    ("tiktok.profile", ("tiktok",), {}, "tt-profile", "/tiktok/profile/tiktok"),
    ("tiktok.video", ("7300000000000000000",), {}, None, "/tiktok/video/7300000000000000000"),
    ("youtube.videos", ("youtube",), {}, "yt-channel-videos", "/youtube/channel/youtube/videos"),
    (
        "appstore.search",
        ("instagram",),
        {"country": "us", "limit": 1},
        "as-search",
        "/appstore/search?term=instagram&country=us&limit=1",
    ),
    (
        "appstore.reviews",
        ("389801252",),
        {"country": "us", "page": 1},
        "as-reviews",
        "/appstore/reviews?appId=389801252&country=us&page=1",
    ),
    ("github.profile", ("torvalds",), {}, "gh-profile", "/github/profiles/torvalds"),
    (
        "github.followers",
        ("torvalds",),
        {"limit": 30, "page": 1},
        "gh-followers",
        "/github/profiles/torvalds/followers?limit=30&page=1",
    ),
    (
        "github.following",
        ("torvalds",),
        {"limit": 5},
        None,
        "/github/profiles/torvalds/following?limit=5&page=1",
    ),
    (
        "github.repositories",
        ("torvalds",),
        {"limit": 30},
        "gh-repos",
        "/github/profiles/torvalds/repositories?limit=30&page=1",
    ),
    (
        "github.search_repositories",
        ("stars:>10000 language:php",),
        {"limit": 1},
        "gh-search-repos",
        "/github/repositories?q=stars:%3E10000+language:php&limit=1&page=1",
    ),
    (
        "github.trending",
        (),
        {"since": "weekly", "language": "php", "limit": 1},
        "gh-trending",
        "/github/trending/repositories?since=weekly&language=php&limit=1",
    ),
    (
        "hackernews.feed",
        ("top",),
        {"limit": 20, "page": 0},
        "hn-feed",
        "/hackernews/feeds/top?limit=20&page=0",
    ),
    ("hackernews.item", (8863,), {}, "hn-item", "/hackernews/items/8863"),
    (
        "hackernews.search",
        ("postgres",),
        {"limit": 20, "page": 0},
        "hn-search",
        "/hackernews/search?q=postgres&limit=20&page=0",
    ),
    ("hackernews.user", ("pg",), {}, "hn-user", "/hackernews/users/pg"),
    (
        "hackernews.submissions",
        ("pg",),
        {"limit": 20, "page": 0},
        "hn-user-submissions",
        "/hackernews/users/pg/submissions?limit=20&page=0",
    ),
    ("hackernews.comments", ("pg",), {"limit": 10}, None, "/hackernews/users/pg/comments?limit=10&page=0"),
    ("bluesky.profile", ("bsky.app",), {}, "bs-profile", "/bluesky/profiles/bsky.app"),
    ("bluesky.posts", ("bsky.app",), {"limit": 25}, "bs-posts", "/bluesky/profiles/bsky.app/posts?limit=25"),
    ("twitch.profile", ("ninja",), {}, "tw-profile", "/twitch/profiles/ninja"),
    ("twitch.videos", ("ninja",), {"limit": 20}, "tw-videos", "/twitch/profiles/ninja/videos?limit=20"),
    ("linktree.profile", ("linktree",), {}, "lt-profile", "/linktree/profiles/linktree"),
]


def _transport(data: Any, urls: list[str]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode().removeprefix("/v1")
        urls.append(normalize(path))
        return httpx.Response(200, json={"message": "ok", "data": data})

    return httpx.MockTransport(handler)


def _data(name: str, fixture_id: str | None) -> Any:
    return fixture_data(fixture_id) if fixture_id else PLACEHOLDER[name]


def test_cases_cover_34_methods() -> None:
    assert len({name for name, *_ in CASES}) == 34


@pytest.mark.parametrize(("name", "args", "kwargs", "fixture_id", "request_path"), CASES)
def test_sync_contract(
    name: str, args: tuple[Any, ...], kwargs: dict[str, Any], fixture_id: str | None, request_path: str
) -> None:
    data = _data(name, fixture_id)
    urls: list[str] = []
    client = ScrapingIsNotACrime(
        "sinac_test", http_client=httpx.Client(transport=_transport(data, urls)), max_retries=0
    )
    namespace, method = name.split(".")
    result = getattr(getattr(client, namespace), method)(*args, **kwargs)
    assert urls == [normalize(request_path)]
    if isinstance(result, Page):
        assert result.data == data
    else:
        assert result == data


@pytest.mark.parametrize(("name", "args", "kwargs", "fixture_id", "request_path"), CASES)
async def test_async_contract(
    name: str, args: tuple[Any, ...], kwargs: dict[str, Any], fixture_id: str | None, request_path: str
) -> None:
    data = _data(name, fixture_id)
    urls: list[str] = []
    async with httpx.AsyncClient(transport=_transport(data, urls)) as http_client:
        client = AsyncScrapingIsNotACrime("sinac_test", http_client=http_client, max_retries=0)
        namespace, method = name.split(".")
        result = await getattr(getattr(client, namespace), method)(*args, **kwargs)
    assert urls == [normalize(request_path)]
    if isinstance(result, AsyncPage):
        assert result.data == data
    else:
        assert result == data


def test_sync_pagination_follows_next_page() -> None:
    first = fixture_data("gh-followers")
    last: dict[str, Any] = {"items": [], "total": None, "has_more": False}
    urls: list[str] = []
    replies = [first, last]

    def handler(request: httpx.Request) -> httpx.Response:
        urls.append(normalize(request.url.raw_path.decode().removeprefix("/v1")))
        return httpx.Response(200, json={"message": "ok", "data": replies.pop(0)})

    client = ScrapingIsNotACrime(
        "sinac_test", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )
    page = client.github.followers("torvalds", limit=30, page=3)
    assert page.next_page == 4
    assert list(page) == first["items"]
    assert urls[1] == "/github/profiles/torvalds/followers?limit=30&page=4"
