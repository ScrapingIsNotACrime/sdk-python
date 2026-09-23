from __future__ import annotations

from typing import Any

from scrapingisnotacrime._http import Route
from scrapingisnotacrime._pagination import PageSpec, afetch_page, fetch_page


class FakeSync:
    def __init__(self, pages: dict[Any, Any], param: str) -> None:
        self.pages = pages
        self.param = param
        self.calls: list[Any] = []

    def get(self, route: Route) -> Any:
        position = route.query.get(self.param)
        self.calls.append(position)
        return self.pages[position]


class FakeAsync(FakeSync):
    async def get(self, route: Route) -> Any:
        return FakeSync.get(self, route)


CURSOR_PAGES = {
    None: {"posts": [1, 2], "next_cursor": "c2", "has_more": True},
    "c2": {"posts": [3], "next_cursor": "c3", "has_more": True},
    "c3": {"posts": [4], "next_cursor": None, "has_more": False},
}
CURSOR_SPEC = PageSpec("/p", {"limit": 2}, "cursor", "posts", None)


def test_cursor_first_page_and_iteration() -> None:
    http = FakeSync(CURSOR_PAGES, "cursor")
    page = fetch_page(http, CURSOR_SPEC)  # type: ignore[arg-type]
    assert page.items == [1, 2]
    assert page.has_more is True
    assert page.next_cursor == "c2"
    assert page.next_page is None
    assert page.data is CURSOR_PAGES[None]
    assert list(page) == [1, 2, 3, 4]
    assert http.calls == [None, "c2", "c3"]


def test_break_does_not_fetch_next_page() -> None:
    http = FakeSync(CURSOR_PAGES, "cursor")
    page = fetch_page(http, CURSOR_SPEC)  # type: ignore[arg-type]
    for item in page:
        assert item == 1
        break
    assert http.calls == [None]


def test_cursor_without_next_cursor_or_empty_string_stops() -> None:
    for cursor in (None, ""):
        http = FakeSync({None: {"posts": [1], "next_cursor": cursor, "has_more": True}}, "cursor")
        page = fetch_page(http, CURSOR_SPEC)  # type: ignore[arg-type]
        assert page.has_more is False
        assert page.next() is None
        assert list(page) == [1]


def test_numbered_one_based_and_zero_based() -> None:
    one = FakeSync({1: {"items": [1], "has_more": True}, 2: {"items": [2], "has_more": False}}, "page")
    page = fetch_page(one, PageSpec("/n", {}, "numbered", "items", 1))  # type: ignore[arg-type]
    assert page.next_page == 2
    assert list(page) == [1, 2]
    assert one.calls == [1, 2]
    zero = FakeSync({0: {"items": [0], "has_more": True}, 1: {"items": [1], "has_more": False}}, "page")
    assert list(fetch_page(zero, PageSpec("/n", {}, "numbered", "items", 0))) == [0, 1]  # type: ignore[arg-type]


def test_numbered_stops_on_empty_page() -> None:
    http = FakeSync({1: {"items": [1], "has_more": True}, 2: {"items": [], "has_more": True}}, "page")
    assert list(fetch_page(http, PageSpec("/n", {}, "numbered", "items", 1))) == [1]  # type: ignore[arg-type]
    assert http.calls == [1, 2]


def test_max_page_cap_ignores_missing_flag() -> None:
    http = FakeSync({9: {"reviews": [9]}, 10: {"reviews": [10]}}, "page")
    page = fetch_page(http, PageSpec("/r", {}, "numbered", "reviews", 9, max_page=10))  # type: ignore[arg-type]
    assert page.has_more is True
    assert list(page) == [9, 10]
    assert http.calls == [9, 10]


async def test_async_page_mirrors_sync() -> None:
    http = FakeAsync(CURSOR_PAGES, "cursor")
    page = await afetch_page(http, CURSOR_SPEC)  # type: ignore[arg-type]
    assert page.items == [1, 2]
    collected = [item async for item in page]
    assert collected == [1, 2, 3, 4]
    nxt = await (await afetch_page(FakeAsync(CURSOR_PAGES, "cursor"), CURSOR_SPEC)).next()  # type: ignore[arg-type]
    assert nxt is not None and nxt.items == [3]
