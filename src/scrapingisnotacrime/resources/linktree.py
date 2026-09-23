from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .. import _routes as routes
from ..types.linktree import LinktreeProfile

if TYPE_CHECKING:
    from .._http import AsyncHttp, SyncHttp


class Linktree:
    def __init__(self, http: SyncHttp) -> None:
        self._http = http

    def profile(self, handle: str) -> LinktreeProfile:
        """GET /linktree/profiles/{handle}"""
        return cast(LinktreeProfile, self._http.get(routes.linktree_profile(handle)))


class AsyncLinktree:
    def __init__(self, http: AsyncHttp) -> None:
        self._http = http

    async def profile(self, handle: str) -> LinktreeProfile:
        """GET /linktree/profiles/{handle}"""
        return cast(LinktreeProfile, await self._http.get(routes.linktree_profile(handle)))
