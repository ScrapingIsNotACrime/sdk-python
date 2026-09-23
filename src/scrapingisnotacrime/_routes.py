from __future__ import annotations

from typing import Literal

from ._http import Route, segment
from ._pagination import PageSpec

GithubTrendingSince = Literal["daily", "weekly", "monthly"]
HackernewsFeed = Literal["top", "new", "best", "ask", "show", "job"]


# Instagram
def instagram_profile(username: str) -> Route:
    return Route(f"/instagram/profile/{segment(username)}")


def instagram_contact(username: str) -> Route:
    return Route(f"/instagram/profile/{segment(username)}/contact")


def instagram_latest_posts(username: str) -> Route:
    return Route(f"/instagram/profile/{segment(username)}/timeline/latest")


def instagram_posts(username: str, count: int | None, cursor: str | None) -> PageSpec:
    return PageSpec(
        f"/instagram/profile/{segment(username)}/timeline", {"count": count}, "cursor", "medias", cursor
    )


def instagram_highlights(username: str) -> Route:
    return Route(f"/instagram/profile/{segment(username)}/highlights")


def instagram_highlight(highlight_id: str) -> Route:
    return Route(f"/instagram/highlights/{segment(highlight_id)}")


def instagram_media_by_id(username: str, media_id: str) -> Route:
    return Route(f"/instagram/profile/{segment(username)}/media/{segment(media_id)}")


def instagram_media(shortcode: str) -> Route:
    return Route(f"/instagram/media/{segment(shortcode)}")


def instagram_download(shortcode: str) -> Route:
    return Route(f"/instagram/media/{segment(shortcode)}/download")


def instagram_shortcode_to_id(shortcode: str) -> Route:
    return Route(f"/instagram/media/{segment(shortcode)}/id")


def instagram_id_to_shortcode(media_id: str) -> Route:
    return Route(f"/instagram/media/id/{segment(media_id)}")


def instagram_reel(shortcode: str) -> Route:
    return Route(f"/instagram/reels/{segment(shortcode)}")


# TikTok
def tiktok_profile(username: str) -> Route:
    return Route(f"/tiktok/profile/{segment(username)}")


def tiktok_video(video_id: str) -> Route:
    return Route(f"/tiktok/video/{segment(video_id)}")


# YouTube
def youtube_videos(handle: str) -> Route:
    return Route(f"/youtube/channel/{segment(handle)}/videos")


# App Store
def appstore_search(term: str, country: str | None, limit: int | None) -> Route:
    return Route("/appstore/search", {"term": term, "country": country, "limit": limit})


def appstore_reviews(app_id: str, country: str | None, page: int | None) -> PageSpec:
    # Apple's feed caps at 10 pages and the payload has no has_more flag.
    return PageSpec(
        "/appstore/reviews",
        {"appId": app_id, "country": country},
        "numbered",
        "reviews",
        page or 1,
        max_page=10,
    )


# GitHub (1-based pages)
def github_profile(handle: str) -> Route:
    return Route(f"/github/profiles/{segment(handle)}")


def _github_list(path: str, query: dict[str, str | int | None], page: int | None) -> PageSpec:
    return PageSpec(path, query, "numbered", "items", 1 if page is None else page)


def github_followers(handle: str, limit: int | None, page: int | None) -> PageSpec:
    return _github_list(f"/github/profiles/{segment(handle)}/followers", {"limit": limit}, page)


def github_following(handle: str, limit: int | None, page: int | None) -> PageSpec:
    return _github_list(f"/github/profiles/{segment(handle)}/following", {"limit": limit}, page)


def github_repositories(handle: str, limit: int | None, page: int | None) -> PageSpec:
    return _github_list(f"/github/profiles/{segment(handle)}/repositories", {"limit": limit}, page)


def github_search_repositories(q: str, limit: int | None, page: int | None) -> PageSpec:
    return _github_list("/github/repositories", {"q": q, "limit": limit}, page)


def github_trending(since: GithubTrendingSince | None, language: str | None, limit: int | None) -> Route:
    return Route("/github/trending/repositories", {"since": since, "language": language, "limit": limit})


# Hacker News (0-based pages)
def _hn_list(path: str, query: dict[str, str | int | None], page: int | None) -> PageSpec:
    return PageSpec(path, query, "numbered", "items", 0 if page is None else page)


def hackernews_feed(feed: HackernewsFeed, limit: int | None, page: int | None) -> PageSpec:
    return _hn_list(f"/hackernews/feeds/{segment(feed)}", {"limit": limit}, page)


def hackernews_item(item_id: int) -> Route:
    return Route(f"/hackernews/items/{segment(item_id)}")


def hackernews_search(q: str, limit: int | None, page: int | None) -> PageSpec:
    return _hn_list("/hackernews/search", {"q": q, "limit": limit}, page)


def hackernews_user(username: str) -> Route:
    return Route(f"/hackernews/users/{segment(username)}")


def hackernews_submissions(username: str, limit: int | None, page: int | None) -> PageSpec:
    return _hn_list(f"/hackernews/users/{segment(username)}/submissions", {"limit": limit}, page)


def hackernews_comments(username: str, limit: int | None, page: int | None) -> PageSpec:
    return _hn_list(f"/hackernews/users/{segment(username)}/comments", {"limit": limit}, page)


# Bluesky
def bluesky_profile(handle: str) -> Route:
    return Route(f"/bluesky/profiles/{segment(handle)}")


def bluesky_posts(handle: str, limit: int | None, cursor: str | None) -> PageSpec:
    return PageSpec(f"/bluesky/profiles/{segment(handle)}/posts", {"limit": limit}, "cursor", "posts", cursor)


# Twitch
def twitch_profile(handle: str) -> Route:
    return Route(f"/twitch/profiles/{segment(handle)}")


def twitch_videos(handle: str, limit: int | None) -> Route:
    return Route(f"/twitch/profiles/{segment(handle)}/videos", {"limit": limit})


# Linktree
def linktree_profile(handle: str) -> Route:
    return Route(f"/linktree/profiles/{segment(handle)}")
