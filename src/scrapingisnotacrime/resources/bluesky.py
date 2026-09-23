from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from .._pagination import AsyncPage, Page, afetch_page, fetch_page
from ..types.bluesky import BlueskyPost, BlueskyProfile

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Bluesky:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, handle: str) -> BlueskyProfile:
        """GET /bluesky/profiles/{handle} — full handle including the domain."""
        return cast(BlueskyProfile, self._http.get(routes.bluesky_profile(handle)))

    def posts(self, handle: str, *, limit: int | None = None, cursor: str | None = None) -> Page[BlueskyPost]:
        """GET /bluesky/profiles/{handle}/posts — limit 1-100 (default 25), cursor-paginated."""
        return fetch_page(self._http, routes.bluesky_posts(handle, limit, cursor))


class AsyncBluesky:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, handle: str) -> BlueskyProfile:
        """GET /bluesky/profiles/{handle} — full handle including the domain."""
        return cast(BlueskyProfile, await self._http.get(routes.bluesky_profile(handle)))

    async def posts(
        self, handle: str, *, limit: int | None = None, cursor: str | None = None
    ) -> AsyncPage[BlueskyPost]:
        """GET /bluesky/profiles/{handle}/posts — limit 1-100 (default 25), cursor-paginated."""
        return await afetch_page(self._http, routes.bluesky_posts(handle, limit, cursor))
