from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from .._pagination import AsyncPage, Page, afetch_page, fetch_page
from ..types.hackernews import (
    HackernewsFeed,
    HackernewsItem,
    HackernewsStory,
    HackernewsUser,
    HackernewsUserComment,
)

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Hackernews:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def feed(
        self, feed: HackernewsFeed, *, limit: int | None = None, page: int | None = None
    ) -> Page[HackernewsStory]:
        """GET /hackernews/feeds/{feed} — limit 1-50 (default 20), 0-based pages."""
        return fetch_page(self._http, routes.hackernews_feed(feed, limit, page))

    def item(self, item_id: int) -> HackernewsItem:
        """GET /hackernews/items/{id} — the item with its full comment tree."""
        return cast(HackernewsItem, self._http.get(routes.hackernews_item(item_id)))

    def search(self, q: str, *, limit: int | None = None, page: int | None = None) -> Page[HackernewsStory]:
        """GET /hackernews/search — limit 1-50 (default 20), 0-based pages."""
        return fetch_page(self._http, routes.hackernews_search(q, limit, page))

    def user(self, username: str) -> HackernewsUser:
        """GET /hackernews/users/{username}"""
        return cast(HackernewsUser, self._http.get(routes.hackernews_user(username)))

    def submissions(
        self, username: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[HackernewsStory]:
        """GET /hackernews/users/{username}/submissions — limit 1-50 (default 20), 0-based pages."""
        return fetch_page(self._http, routes.hackernews_submissions(username, limit, page))

    def comments(
        self, username: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[HackernewsUserComment]:
        """GET /hackernews/users/{username}/comments — limit 1-50 (default 20), 0-based pages."""
        return fetch_page(self._http, routes.hackernews_comments(username, limit, page))


class AsyncHackernews:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def feed(
        self, feed: HackernewsFeed, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[HackernewsStory]:
        """GET /hackernews/feeds/{feed} — limit 1-50 (default 20), 0-based pages."""
        return await afetch_page(self._http, routes.hackernews_feed(feed, limit, page))

    async def item(self, item_id: int) -> HackernewsItem:
        """GET /hackernews/items/{id} — the item with its full comment tree."""
        return cast(HackernewsItem, await self._http.get(routes.hackernews_item(item_id)))

    async def search(
        self, q: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[HackernewsStory]:
        """GET /hackernews/search — limit 1-50 (default 20), 0-based pages."""
        return await afetch_page(self._http, routes.hackernews_search(q, limit, page))

    async def user(self, username: str) -> HackernewsUser:
        """GET /hackernews/users/{username}"""
        return cast(HackernewsUser, await self._http.get(routes.hackernews_user(username)))

    async def submissions(
        self, username: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[HackernewsStory]:
        """GET /hackernews/users/{username}/submissions — limit 1-50 (default 20), 0-based pages."""
        return await afetch_page(self._http, routes.hackernews_submissions(username, limit, page))

    async def comments(
        self, username: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[HackernewsUserComment]:
        """GET /hackernews/users/{username}/comments — limit 1-50 (default 20), 0-based pages."""
        return await afetch_page(self._http, routes.hackernews_comments(username, limit, page))
