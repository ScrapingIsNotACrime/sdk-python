# ScrapingIsNotACrime Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scrapingisnotacrime.svg)](https://pypi.org/project/scrapingisnotacrime/)
[![license](https://img.shields.io/pypi/l/scrapingisnotacrime.svg)](./LICENSE)

Official Python SDK for the [ScrapingIsNotACrime](https://scrapingisnotacrime.com) public data API — typed access to Instagram, TikTok, YouTube, App Store, GitHub, Hacker News, Bluesky, Twitch and Linktree, with sync and async clients.

## Install

```bash
pip install scrapingisnotacrime
```

Requires Python 3.11+.

## Quick start

Sync:

```python
from scrapingisnotacrime import ScrapingIsNotACrime

with ScrapingIsNotACrime() as client:
    profile = client.instagram.profile("nasa")
    print(profile["username"], profile["followers"])
```

Async:

```python
import asyncio

from scrapingisnotacrime import AsyncScrapingIsNotACrime


async def main() -> None:
    async with AsyncScrapingIsNotACrime() as client:
        profile = await client.instagram.profile("nasa")
        print(profile["username"], profile["followers"])


asyncio.run(main())
```

Both clients read the API key from the `SCRAPINGISNOTACRIME_API_KEY` environment variable, or take it as `api_key=`. Get a key at [scrapingisnotacrime.com/dashboard/api-keys](https://scrapingisnotacrime.com/dashboard/api-keys). Keys start with `sinac_`.

More runnable examples are in [`examples/`](./examples): [`profile.py`](./examples/profile.py), [`paginate_followers.py`](./examples/paginate_followers.py) and [`async_posts.py`](./examples/async_posts.py).

## Configuration

```python
ScrapingIsNotACrime(
    api_key="sinac_...",
    base_url="https://api.scrapingisnotacrime.com/v1",
    timeout=30.0,
    max_retries=2,
    http_client=None,
)
```

`AsyncScrapingIsNotACrime` takes the same arguments (`http_client` accepts an `httpx.AsyncClient` instead).

| Option | Default | Description |
|---|---|---|
| `api_key` | `SCRAPINGISNOTACRIME_API_KEY` env var | Your API key (`sinac_…`). Raises `ValueError` at construction if missing. |
| `base_url` | `https://api.scrapingisnotacrime.com/v1` | API base URL. |
| `timeout` | `30.0` | Per-attempt timeout, in seconds. |
| `max_retries` | `2` | Extra attempts for 429, 502 and network errors. `0` disables retries. |
| `http_client` | a new `httpx.Client` (or `httpx.AsyncClient`) | Bring your own httpx client — for tests, proxies or connection pooling. Only closed by `client.close()` / `await client.aclose()` when the SDK created it. |

## Methods

Every method returns the response envelope's `data`, typed as a `TypedDict`. Methods marked `→ Page` / `→ AsyncPage` return a lazily-iterable page (see [Pagination](#pagination)). Optional arguments are keyword-only.

| Platform | Method | Route |
|---|---|---|
| Instagram | `instagram.profile(username)` | `/instagram/profile/{username}` |
| Instagram | `instagram.contact(username)` | `/instagram/profile/{username}/contact` |
| Instagram | `instagram.latest_posts(username)` | `/instagram/profile/{username}/timeline/latest` |
| Instagram | `instagram.posts(username, *, count=None, cursor=None)` → `Page` | `/instagram/profile/{username}/timeline` |
| Instagram | `instagram.highlights(username)` | `/instagram/profile/{username}/highlights` |
| Instagram | `instagram.highlight(highlight_id)` | `/instagram/highlights/{highlightId}` |
| Instagram | `instagram.media_by_id(username, media_id)` | `/instagram/profile/{username}/media/{mediaId}` |
| Instagram | `instagram.media(shortcode)` | `/instagram/media/{shortcode}` |
| Instagram | `instagram.download(shortcode)` | `/instagram/media/{shortcode}/download` |
| Instagram | `instagram.shortcode_to_id(shortcode)` | `/instagram/media/{shortcode}/id` |
| Instagram | `instagram.id_to_shortcode(media_id)` | `/instagram/media/id/{mediaId}` |
| Instagram | `instagram.reel(shortcode)` | `/instagram/reels/{shortcode}` |
| TikTok | `tiktok.profile(username)` | `/tiktok/profile/{username}` |
| TikTok | `tiktok.video(video_id)` | `/tiktok/video/{videoId}` |
| YouTube | `youtube.videos(handle)` | `/youtube/channel/{handle}/videos` |
| App Store | `appstore.search(term, *, country=None, limit=None)` | `/appstore/search` |
| App Store | `appstore.reviews(app_id, *, country=None, page=None)` → `Page` | `/appstore/reviews` |
| GitHub | `github.profile(handle)` | `/github/profiles/{handle}` |
| GitHub | `github.followers(handle, *, limit=None, page=None)` → `Page` | `/github/profiles/{handle}/followers` |
| GitHub | `github.following(handle, *, limit=None, page=None)` → `Page` | `/github/profiles/{handle}/following` |
| GitHub | `github.repositories(handle, *, limit=None, page=None)` → `Page` | `/github/profiles/{handle}/repositories` |
| GitHub | `github.search_repositories(q, *, limit=None, page=None)` → `Page` | `/github/repositories` |
| GitHub | `github.trending(*, since=None, language=None, limit=None)` | `/github/trending/repositories` |
| Hacker News | `hackernews.feed(feed, *, limit=None, page=None)` → `Page` | `/hackernews/feeds/{feed}` |
| Hacker News | `hackernews.item(item_id)` | `/hackernews/items/{id}` |
| Hacker News | `hackernews.search(q, *, limit=None, page=None)` → `Page` | `/hackernews/search` |
| Hacker News | `hackernews.user(username)` | `/hackernews/users/{username}` |
| Hacker News | `hackernews.submissions(username, *, limit=None, page=None)` → `Page` | `/hackernews/users/{username}/submissions` |
| Hacker News | `hackernews.comments(username, *, limit=None, page=None)` → `Page` | `/hackernews/users/{username}/comments` |
| Bluesky | `bluesky.profile(handle)` | `/bluesky/profiles/{handle}` |
| Bluesky | `bluesky.posts(handle, *, limit=None, cursor=None)` → `Page` | `/bluesky/profiles/{handle}/posts` |
| Twitch | `twitch.profile(handle)` | `/twitch/profiles/{handle}` |
| Twitch | `twitch.videos(handle, *, limit=None)` | `/twitch/profiles/{handle}/videos` |
| Linktree | `linktree.profile(handle)` | `/linktree/profiles/{handle}` |

The async client (`AsyncScrapingIsNotACrime`) exposes the same namespaces and methods as `await`able coroutines.

Path arguments are validated before any request: an empty string, `"."`, `".."`, a `bool`, or a non-finite number (`nan`, `inf`) raises `ValueError`. On the async client this is raised by the awaited coroutine, never at call time.

## Pagination

Methods marked `→ Page` return a `Page[T]` (or `AsyncPage[T]` on the async client):

```python
class Page(Generic[T]):
    data: Any  # the full response of this page
    items: list[T]  # this page's items
    has_more: bool
    next_cursor: str | None  # cursor endpoints
    next_page: int | None  # page-number endpoints

    def next(self) -> Page[T] | None: ...  # the following page, or None
    def __iter__(self) -> Iterator[T]: ...  # every item, fetching further pages lazily
```

Iterate every item, fetching further pages lazily as they're needed. Iterating fetches every remaining page; each page is one billed request, so bound the loop:

```python
page = client.github.followers("torvalds", limit=100)
for count, user in enumerate(page, start=1):
    print(user["username"])
    if count >= 100:
        break  # stop early; no further pages are fetched
```

Async, with `async for`:

```python
page = await client.bluesky.posts("bsky.app", limit=25)
count = 0
async for post in page:
    print(post)
    count += 1
    if count >= 100:
        break  # stop early; no further pages are fetched
```

`page.data` gives you the untouched response of the current page, so fields such as `total` stay reachable. Breaking out of the loop early stops fetching — no further pages are requested once you `break`.

## Types

Responses are plain `dict`s typed with `TypedDict`, importable from `scrapingisnotacrime.types`:

```python
from scrapingisnotacrime.types import InstagramProfile
```

Field names are kept exactly as the API sends them (snake_case, or `camelCase` for the App Store endpoints). Fields the upstream platforms routinely leave empty — descriptions, bios, captions, languages, last-broadcast info — are typed `NotRequired[T | None]`, so they may be missing from the dict entirely or present as `None`; check before use.

## Errors

Every failure raises a subclass of `ScrapingIsNotACrimeError`, carrying `status` (the HTTP status, or `None` for network errors), `message` and `request_id` (when the API returns one).

| Class | Status | Retried |
|---|---|---|
| `BadRequestError` | 400 | no |
| `AuthenticationError` | 401 | no |
| `QuotaExceededError` | 402 | no |
| `NotFoundError` | 404 | no |
| `RateLimitError` | 429 | yes |
| `UpstreamError` | 502 | yes |
| `ConnectionError` | network failure or timeout | yes |
| `APIError` | any other non-2xx | no |

`ConnectionError` here is the SDK's own class — import it from `scrapingisnotacrime`, not the builtin `ConnectionError`.

```python
from scrapingisnotacrime import (
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ScrapingIsNotACrime,
)

client = ScrapingIsNotACrime(max_retries=3)

try:
    client.tiktok.profile("this-user-does-not-exist-123")
except NotFoundError:
    print("No such profile.")
except QuotaExceededError as error:
    print("Out of credits:", error.message)
except RateLimitError:
    print("TikTok is rate limiting; try again later.")
```

## Retries

`RateLimitError` (429), `UpstreamError` (502) and `ConnectionError` (network failure or timeout) are retried automatically, up to `max_retries` additional attempts (default 2). These failures don't consume credits, so retrying them costs you nothing.

The delay before each retry uses the `Retry-After` header when the API sends one (seconds or an HTTP date); otherwise it's exponential backoff with full jitter, starting at 500 ms and doubling per attempt. Every wait is capped at 10 seconds. Set `max_retries=0` to disable retries entirely.

## Releases and changelog

Every merge to `main` is released automatically: the version comes from the commit messages since the last release, following [Conventional Commits](https://www.conventionalcommits.org/).

| Commits since the last release | New version (while in 0.x) |
|---|---|
| only `docs:`, `chore:`, `test:`, `ci:`, `build:`, `refactor:` | none |
| at least one `fix:` | patch (`0.1.0` → `0.1.1`) |
| at least one `feat:` | minor (`0.1.1` → `0.2.0`) |
| `feat!:` or a `BREAKING CHANGE:` footer | minor while in 0.x |

The pipeline tags `vX.Y.Z`, publishes the GitHub Release with the notes, and publishes to PyPI through Trusted Publishing. The changelog is the [Releases page](https://github.com/ScrapingIsNotACrime/sdk-python/releases); the version is resolved from git tags at build time (`hatch-vcs`), so no version number is written into the repository.

## Links

- Docs: https://scrapingisnotacrime.com/docs
- Pricing: https://scrapingisnotacrime.com/#pricing
- Releases: https://github.com/ScrapingIsNotACrime/sdk-python/releases
- Node.js SDK: https://github.com/ScrapingIsNotACrime/sdk-nodejs
- MCP server: https://github.com/ScrapingIsNotACrime/mcp
- License: [MIT](./LICENSE)
