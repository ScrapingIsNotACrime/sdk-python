import json
from pathlib import Path
from typing import Any, get_args

import pytest

from scrapingisnotacrime import types as t

from .typecheck import check

FIXTURES = Path(__file__).parent / "fixtures"

GATES: dict[str, Any] = {
    "ig-profile": t.InstagramProfile,
    "ig-contact": t.InstagramContact,
    "ig-timeline": t.InstagramLatestPosts,
    "ig-timeline-paged": t.InstagramTimelinePage,
    "ig-highlights": t.InstagramHighlights,
    "ig-highlight-content": t.InstagramHighlight,
    "ig-media-by-id": t.InstagramMediaDetail,
    "ig-media-download": t.InstagramDownload,
    "ig-shortcode-to-id": t.InstagramShortcodeId,
    "ig-id-to-shortcode": t.InstagramShortcodeId,
    "ig-reels": t.InstagramReel,
    "tt-profile": t.TiktokProfile,
    "yt-channel-videos": t.YoutubeChannelVideos,
    "as-search": t.AppstoreSearch,
    "as-reviews": t.AppstoreReviewPage,
    "gh-profile": t.GithubProfile,
    "gh-followers": t.GithubUserPage,
    "gh-repos": t.GithubRepositoryPage,
    "gh-search-repos": t.GithubRepositorySearchPage,
    "gh-trending": t.GithubTrending,
    "hn-feed": t.HackernewsStoryPage,
    "hn-item": t.HackernewsItem,
    "hn-search": t.HackernewsStoryPage,
    "hn-user": t.HackernewsUser,
    "hn-user-submissions": t.HackernewsStoryPage,
    "bs-profile": t.BlueskyProfile,
    "bs-posts": t.BlueskyPostPage,
    "tw-profile": t.TwitchProfile,
    "tw-videos": t.TwitchVideos,
    "lt-profile": t.LinktreeProfile,
}


def test_every_fixture_has_a_gate() -> None:
    assert sorted(GATES) == sorted(p.stem for p in FIXTURES.glob("*.json"))


@pytest.mark.parametrize("fixture_id", sorted(GATES))
def test_documented_example_matches_its_type(fixture_id: str) -> None:
    data = json.loads((FIXTURES / f"{fixture_id}.json").read_text())["response"]["data"]
    assert check(data, GATES[fixture_id]) == []


def test_validator_catches_contradictions() -> None:
    assert check({"username": 1}, t.LinktreeProfile) != []
    assert check({}, t.LinktreeProfile) != []


def test_literal_types_are_public() -> None:
    from scrapingisnotacrime.types import GithubTrendingSince, HackernewsFeed

    assert get_args(GithubTrendingSince) == ("daily", "weekly", "monthly")
    assert get_args(HackernewsFeed) == ("top", "new", "best", "ask", "show", "job")
