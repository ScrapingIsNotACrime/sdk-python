from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from ..types.youtube import YoutubeChannelVideos

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Youtube:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def videos(self, handle: str) -> YoutubeChannelVideos:
        """GET /youtube/channel/{handle}/videos"""
        return cast(YoutubeChannelVideos, self._http.get(routes.youtube_videos(handle)))


class AsyncYoutube:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def videos(self, handle: str) -> YoutubeChannelVideos:
        """GET /youtube/channel/{handle}/videos"""
        return cast(YoutubeChannelVideos, await self._http.get(routes.youtube_videos(handle)))
