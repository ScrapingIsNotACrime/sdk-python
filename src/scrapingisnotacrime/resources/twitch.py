from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from ..types.twitch import TwitchProfile, TwitchVideos

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Twitch:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, handle: str) -> TwitchProfile:
        """GET /twitch/profiles/{handle}"""
        return cast(TwitchProfile, self._http.get(routes.twitch_profile(handle)))

    def videos(self, handle: str, *, limit: int | None = None) -> TwitchVideos:
        """GET /twitch/profiles/{handle}/videos — not paginated; limit 1-100 (default 20)."""
        return cast(TwitchVideos, self._http.get(routes.twitch_videos(handle, limit)))


class AsyncTwitch:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, handle: str) -> TwitchProfile:
        """GET /twitch/profiles/{handle}"""
        return cast(TwitchProfile, await self._http.get(routes.twitch_profile(handle)))

    async def videos(self, handle: str, *, limit: int | None = None) -> TwitchVideos:
        """GET /twitch/profiles/{handle}/videos — not paginated; limit 1-100 (default 20)."""
        return cast(TwitchVideos, await self._http.get(routes.twitch_videos(handle, limit)))
