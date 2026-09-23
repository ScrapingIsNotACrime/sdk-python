from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from .._pagination import AsyncPage, Page, afetch_page, fetch_page
from ..types.instagram import (
    InstagramContact,
    InstagramDownload,
    InstagramHighlight,
    InstagramHighlights,
    InstagramLatestPosts,
    InstagramMedia,
    InstagramMediaDetail,
    InstagramProfile,
    InstagramReel,
    InstagramShortcodeId,
)

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Instagram:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, username: str) -> InstagramProfile:
        """GET /instagram/profile/{username} — username without @."""
        return cast(InstagramProfile, self._http.get(routes.instagram_profile(username)))

    def contact(self, username: str) -> InstagramContact:
        """GET /instagram/profile/{username}/contact — public business contact (email, phone, address)."""
        return cast(InstagramContact, self._http.get(routes.instagram_contact(username)))

    def latest_posts(self, username: str) -> InstagramLatestPosts:
        """GET /instagram/profile/{username}/timeline/latest — the first page of posts."""
        return cast(InstagramLatestPosts, self._http.get(routes.instagram_latest_posts(username)))

    def posts(
        self, username: str, *, count: int | None = None, cursor: str | None = None
    ) -> Page[InstagramMedia]:
        """GET /instagram/profile/{username}/timeline — full history, cursor-paginated;
        count 1-50 (default 12)."""
        return fetch_page(self._http, routes.instagram_posts(username, count, cursor))

    def highlights(self, username: str) -> InstagramHighlights:
        """GET /instagram/profile/{username}/highlights"""
        return cast(InstagramHighlights, self._http.get(routes.instagram_highlights(username)))

    def highlight(self, highlight_id: str) -> InstagramHighlight:
        """GET /instagram/highlights/{highlightId}"""
        return cast(InstagramHighlight, self._http.get(routes.instagram_highlight(highlight_id)))

    def media_by_id(self, username: str, media_id: str) -> InstagramMediaDetail:
        """GET /instagram/profile/{username}/media/{mediaId}"""
        return cast(InstagramMediaDetail, self._http.get(routes.instagram_media_by_id(username, media_id)))

    def media(self, shortcode: str) -> InstagramMediaDetail:
        """GET /instagram/media/{shortcode} — shortcode from instagram.com/p/{shortcode}/."""
        return cast(InstagramMediaDetail, self._http.get(routes.instagram_media(shortcode)))

    def download(self, shortcode: str) -> InstagramDownload:
        """GET /instagram/media/{shortcode}/download — assets[0] is the best primary asset."""
        return cast(InstagramDownload, self._http.get(routes.instagram_download(shortcode)))

    def shortcode_to_id(self, shortcode: str) -> InstagramShortcodeId:
        """GET /instagram/media/{shortcode}/id"""
        return cast(InstagramShortcodeId, self._http.get(routes.instagram_shortcode_to_id(shortcode)))

    def id_to_shortcode(self, media_id: str) -> InstagramShortcodeId:
        """GET /instagram/media/id/{mediaId}"""
        return cast(InstagramShortcodeId, self._http.get(routes.instagram_id_to_shortcode(media_id)))

    def reel(self, shortcode: str) -> InstagramReel:
        """GET /instagram/reels/{shortcode}"""
        return cast(InstagramReel, self._http.get(routes.instagram_reel(shortcode)))


class AsyncInstagram:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, username: str) -> InstagramProfile:
        """GET /instagram/profile/{username} — username without @."""
        return cast(InstagramProfile, await self._http.get(routes.instagram_profile(username)))

    async def contact(self, username: str) -> InstagramContact:
        """GET /instagram/profile/{username}/contact — public business contact (email, phone, address)."""
        return cast(InstagramContact, await self._http.get(routes.instagram_contact(username)))

    async def latest_posts(self, username: str) -> InstagramLatestPosts:
        """GET /instagram/profile/{username}/timeline/latest — the first page of posts."""
        return cast(InstagramLatestPosts, await self._http.get(routes.instagram_latest_posts(username)))

    async def posts(
        self, username: str, *, count: int | None = None, cursor: str | None = None
    ) -> AsyncPage[InstagramMedia]:
        """GET /instagram/profile/{username}/timeline — full history, cursor-paginated;
        count 1-50 (default 12)."""
        return await afetch_page(self._http, routes.instagram_posts(username, count, cursor))

    async def highlights(self, username: str) -> InstagramHighlights:
        """GET /instagram/profile/{username}/highlights"""
        return cast(InstagramHighlights, await self._http.get(routes.instagram_highlights(username)))

    async def highlight(self, highlight_id: str) -> InstagramHighlight:
        """GET /instagram/highlights/{highlightId}"""
        return cast(InstagramHighlight, await self._http.get(routes.instagram_highlight(highlight_id)))

    async def media_by_id(self, username: str, media_id: str) -> InstagramMediaDetail:
        """GET /instagram/profile/{username}/media/{mediaId}"""
        return cast(
            InstagramMediaDetail, await self._http.get(routes.instagram_media_by_id(username, media_id))
        )

    async def media(self, shortcode: str) -> InstagramMediaDetail:
        """GET /instagram/media/{shortcode} — shortcode from instagram.com/p/{shortcode}/."""
        return cast(InstagramMediaDetail, await self._http.get(routes.instagram_media(shortcode)))

    async def download(self, shortcode: str) -> InstagramDownload:
        """GET /instagram/media/{shortcode}/download — assets[0] is the best primary asset."""
        return cast(InstagramDownload, await self._http.get(routes.instagram_download(shortcode)))

    async def shortcode_to_id(self, shortcode: str) -> InstagramShortcodeId:
        """GET /instagram/media/{shortcode}/id"""
        return cast(InstagramShortcodeId, await self._http.get(routes.instagram_shortcode_to_id(shortcode)))

    async def id_to_shortcode(self, media_id: str) -> InstagramShortcodeId:
        """GET /instagram/media/id/{mediaId}"""
        return cast(InstagramShortcodeId, await self._http.get(routes.instagram_id_to_shortcode(media_id)))

    async def reel(self, shortcode: str) -> InstagramReel:
        """GET /instagram/reels/{shortcode}"""
        return cast(InstagramReel, await self._http.get(routes.instagram_reel(shortcode)))
