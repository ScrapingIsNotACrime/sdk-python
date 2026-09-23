from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Mapping
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

from ._http import Route

if TYPE_CHECKING:
    from ._http import AsyncHttp, SyncHttp

T = TypeVar("T")


@dataclass(frozen=True)
class PageSpec:
    path: str
    query: Mapping[str, str | int | None]
    kind: Literal["cursor", "numbered"]
    items_key: str
    start: str | int | None
    # Numbered endpoints with no has_more flag (App Store reviews): more while
    # the page is non-empty and below this cap.
    max_page: int | None = None

    @property
    def param(self) -> str:
        return "cursor" if self.kind == "cursor" else "page"

    def route(self) -> Route:
        return Route(self.path, {**self.query, self.param: self.start})


@dataclass(frozen=True)
class _State:
    items: list[Any]
    has_more: bool
    next_cursor: str | None
    next_page: int | None


def _state(spec: PageSpec, data: Any) -> _State:
    raw_items = data.get(spec.items_key) if isinstance(data, dict) else None
    items: list[Any] = list(raw_items) if isinstance(raw_items, list) else []
    if spec.kind == "cursor":
        cursor = data.get("next_cursor") if isinstance(data, dict) else None
        next_cursor = cursor if isinstance(cursor, str) and cursor else None
        has_more = bool(data.get("has_more")) and next_cursor is not None
        return _State(items, has_more, next_cursor, None)
    page = int(spec.start) if spec.start is not None else 0
    if spec.max_page is not None:
        has_more = bool(items) and page < spec.max_page
    else:
        has_more = bool(data.get("has_more")) if isinstance(data, dict) else False
    return _State(items, has_more, None, page + 1 if has_more else None)


def _next_spec(spec: PageSpec, state: _State) -> PageSpec | None:
    if not state.has_more or not state.items:
        return None
    return replace(spec, start=state.next_cursor if spec.kind == "cursor" else state.next_page)


class Page(Generic[T]):
    """One page of results. Iterating yields every item from here on, fetching lazily."""

    def __init__(self, http: SyncHttp, spec: PageSpec, data: Any) -> None:
        self._http = http
        self._spec = spec
        state = _state(spec, data)
        self.data: Any = data
        self.items: list[T] = state.items
        self.has_more = state.has_more
        self.next_cursor = state.next_cursor
        self.next_page = state.next_page
        self._next = _next_spec(spec, state)

    def next(self) -> Page[T] | None:
        """The following page, or None when there is none."""
        return fetch_page(self._http, self._next) if self._next is not None else None

    def __iter__(self) -> Iterator[T]:
        page: Page[T] | None = self
        while page is not None:
            yield from page.items
            page = page.next()


class AsyncPage(Generic[T]):
    """Async counterpart of Page: `async for item in page`."""

    def __init__(self, http: AsyncHttp, spec: PageSpec, data: Any) -> None:
        self._http = http
        self._spec = spec
        state = _state(spec, data)
        self.data: Any = data
        self.items: list[T] = state.items
        self.has_more = state.has_more
        self.next_cursor = state.next_cursor
        self.next_page = state.next_page
        self._next = _next_spec(spec, state)

    async def next(self) -> AsyncPage[T] | None:
        return await afetch_page(self._http, self._next) if self._next is not None else None

    async def __aiter__(self) -> AsyncIterator[T]:
        page: AsyncPage[T] | None = self
        while page is not None:
            for item in page.items:
                yield item
            page = await page.next()


def fetch_page(http: SyncHttp, spec: PageSpec) -> Page[Any]:
    return Page(http, spec, http.get(spec.route()))


async def afetch_page(http: AsyncHttp, spec: PageSpec) -> AsyncPage[Any]:
    return AsyncPage(http, spec, await http.get(spec.route()))
