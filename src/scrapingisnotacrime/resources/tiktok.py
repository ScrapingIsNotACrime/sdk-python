from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from ..types.tiktok import TiktokProfile, TiktokVideo

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Tiktok:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, username: str) -> TiktokProfile:
        """GET /tiktok/profile/{username}"""
        return cast(TiktokProfile, self._http.get(routes.tiktok_profile(username)))

    def video(self, video_id: str) -> TiktokVideo:
        """GET /tiktok/video/{videoId}"""
        return cast(TiktokVideo, self._http.get(routes.tiktok_video(video_id)))


class AsyncTiktok:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, username: str) -> TiktokProfile:
        """GET /tiktok/profile/{username}"""
        return cast(TiktokProfile, await self._http.get(routes.tiktok_profile(username)))

    async def video(self, video_id: str) -> TiktokVideo:
        """GET /tiktok/video/{videoId}"""
        return cast(TiktokVideo, await self._http.get(routes.tiktok_video(video_id)))
