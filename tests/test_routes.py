from scrapingisnotacrime import _routes as routes
from scrapingisnotacrime._http import Route, build_url


def url(route: Route) -> str:
    return build_url("", route.path, route.query)


def test_paths_and_query_order_match_documented_requests() -> None:
    assert (
        url(routes.instagram_highlight("highlight:18201653992314974"))
        == "/instagram/highlights/highlight%3A18201653992314974"
    )
    assert (
        url(routes.appstore_search("instagram", "us", 1))
        == "/appstore/search?term=instagram&country=us&limit=1"
    )
    assert (
        url(routes.appstore_reviews("389801252", "us", None).route())
        == "/appstore/reviews?appId=389801252&country=us&page=1"
    )
    assert (
        url(routes.github_followers("torvalds", 30, None).route())
        == "/github/profiles/torvalds/followers?limit=30&page=1"
    )
    assert url(routes.hackernews_feed("top", 20, None).route()) == "/hackernews/feeds/top?limit=20&page=0"
    assert (
        url(routes.instagram_posts("nasa", 12, None).route()) == "/instagram/profile/nasa/timeline?count=12"
    )
    assert url(routes.hackernews_item(8863)) == "/hackernews/items/8863"


def test_appstore_reviews_page_zero_is_sent_as_is() -> None:
    assert url(routes.appstore_reviews("1", None, 0).route()) == "/appstore/reviews?appId=1&page=0"
    assert url(routes.appstore_reviews("1", None, None).route()) == "/appstore/reviews?appId=1&page=1"
