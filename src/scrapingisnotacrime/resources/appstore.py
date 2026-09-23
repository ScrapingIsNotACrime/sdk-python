from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from .._pagination import AsyncPage, Page, afetch_page, fetch_page
from ..types.appstore import AppstoreReview, AppstoreSearch

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Appstore:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def search(self, term: str, *, country: str | None = None, limit: int | None = None) -> AppstoreSearch:
        """GET /appstore/search — country defaults to "us", limit 1-200 (default 10)."""
        return cast(AppstoreSearch, self._http.get(routes.appstore_search(term, country, limit)))

    def reviews(
        self, app_id: str, *, country: str | None = None, page: int | None = None
    ) -> Page[AppstoreReview]:
        """GET /appstore/reviews — pages 1-10 (Apple's cap); the API returns 400 past page 10."""
        return fetch_page(self._http, routes.appstore_reviews(app_id, country, page))


class AsyncAppstore:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def search(
        self, term: str, *, country: str | None = None, limit: int | None = None
    ) -> AppstoreSearch:
        """GET /appstore/search — country defaults to "us", limit 1-200 (default 10)."""
        return cast(AppstoreSearch, await self._http.get(routes.appstore_search(term, country, limit)))

    async def reviews(
        self, app_id: str, *, country: str | None = None, page: int | None = None
    ) -> AsyncPage[AppstoreReview]:
        """GET /appstore/reviews — pages 1-10 (Apple's cap); the API returns 400 past page 10."""
        return await afetch_page(self._http, routes.appstore_reviews(app_id, country, page))
