from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from .._pagination import AsyncPage, Page, afetch_page, fetch_page
from ..types.github import (
    GithubProfile,
    GithubRepository,
    GithubTrending,
    GithubUser,
)

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Github:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, handle: str) -> GithubProfile:
        """GET /github/profiles/{handle}"""
        return cast(GithubProfile, self._http.get(routes.github_profile(handle)))

    def followers(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[GithubUser]:
        """GET /github/profiles/{handle}/followers — limit 1-100 (default 30), 1-based pages."""
        return fetch_page(self._http, routes.github_followers(handle, limit, page))

    def following(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[GithubUser]:
        """GET /github/profiles/{handle}/following — limit 1-100 (default 30), 1-based pages."""
        return fetch_page(self._http, routes.github_following(handle, limit, page))

    def repositories(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[GithubRepository]:
        """GET /github/profiles/{handle}/repositories — limit 1-100 (default 30), 1-based pages."""
        return fetch_page(self._http, routes.github_repositories(handle, limit, page))

    def search_repositories(
        self, q: str, *, limit: int | None = None, page: int | None = None
    ) -> Page[GithubRepository]:
        """GET /github/repositories — q in GitHub search syntax; limit 1-100 (default 30), 1-based pages."""
        return fetch_page(self._http, routes.github_search_repositories(q, limit, page))

    def trending(
        self,
        *,
        since: routes.GithubTrendingSince | None = None,
        language: str | None = None,
        limit: int | None = None,
    ) -> GithubTrending:
        """GET /github/trending/repositories — not paginated; since defaults to "daily",
        limit 1-100 (default 30)."""
        return cast(GithubTrending, self._http.get(routes.github_trending(since, language, limit)))


class AsyncGithub:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, handle: str) -> GithubProfile:
        """GET /github/profiles/{handle}"""
        return cast(GithubProfile, await self._http.get(routes.github_profile(handle)))

    async def followers(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[GithubUser]:
        """GET /github/profiles/{handle}/followers — limit 1-100 (default 30), 1-based pages."""
        return await afetch_page(self._http, routes.github_followers(handle, limit, page))

    async def following(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[GithubUser]:
        """GET /github/profiles/{handle}/following — limit 1-100 (default 30), 1-based pages."""
        return await afetch_page(self._http, routes.github_following(handle, limit, page))

    async def repositories(
        self, handle: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[GithubRepository]:
        """GET /github/profiles/{handle}/repositories — limit 1-100 (default 30), 1-based pages."""
        return await afetch_page(self._http, routes.github_repositories(handle, limit, page))

    async def search_repositories(
        self, q: str, *, limit: int | None = None, page: int | None = None
    ) -> AsyncPage[GithubRepository]:
        """GET /github/repositories — q in GitHub search syntax; limit 1-100 (default 30), 1-based pages."""
        return await afetch_page(self._http, routes.github_search_repositories(q, limit, page))

    async def trending(
        self,
        *,
        since: routes.GithubTrendingSince | None = None,
        language: str | None = None,
        limit: int | None = None,
    ) -> GithubTrending:
        """GET /github/trending/repositories — not paginated; since defaults to "daily",
        limit 1-100 (default 30)."""
        return cast(GithubTrending, await self._http.get(routes.github_trending(since, language, limit)))
