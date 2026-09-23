"""Real-API smoke test: one cheap call per platform (9 credits)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from scrapingisnotacrime import ScrapingIsNotACrime
from scrapingisnotacrime import types as t

from ..typecheck import check

FIXTURES = Path(__file__).parent.parent / "fixtures"
_needs_api_key = pytest.mark.skipif(not os.environ.get("SCRAPINGISNOTACRIME_API_KEY"), reason="no API key")


@_needs_api_key
def test_one_call_per_platform() -> None:
    with ScrapingIsNotACrime() as client:
        calls: list[tuple[Any, Any]] = [
            (client.instagram.profile("nasa"), t.InstagramProfile),
            (client.tiktok.profile("tiktok"), t.TiktokProfile),
            (client.youtube.videos("youtube"), t.YoutubeChannelVideos),
            (client.appstore.search("instagram", limit=1), t.AppstoreSearch),
            (client.github.profile("torvalds"), t.GithubProfile),
            (client.hackernews.item(8863), t.HackernewsItem),
            (client.bluesky.profile("bsky.app"), t.BlueskyProfile),
            (client.twitch.profile("ninja"), t.TwitchProfile),
            (client.linktree.profile("linktree"), t.LinktreeProfile),
        ]
        for data, hint in calls:
            assert check(data, hint) == [], hint.__name__


def test_fixtures_exist() -> None:
    assert json.loads((FIXTURES / "lt-profile.json").read_text())
