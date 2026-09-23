from typing import NotRequired, TypedDict


class TwitchBroadcast(TypedDict):
    """A channel's most recent broadcast."""

    title: str
    started_at: str


class TwitchProfile(TypedDict):
    """GET /twitch/profiles/{handle}"""

    id: str
    login: str
    display_name: str
    description: str
    avatar: str
    followers: int
    is_partner: bool
    is_affiliate: bool
    created_at: str
    is_live: bool
    # Current viewer count while live; null whenever is_live is false.
    live_viewers: NotRequired[int | None]
    # Null when the channel has never broadcast (or the info is unavailable).
    last_broadcast: NotRequired[TwitchBroadcast | None]
    url: str


class TwitchVideo(TypedDict):
    """One video in a channel's published videos list."""

    id: str
    title: str
    duration_seconds: int
    views: int
    published_at: str
    thumbnail: str
    url: str


class TwitchVideos(TypedDict):
    """GET /twitch/profiles/{handle}/videos"""

    videos: list[TwitchVideo]
    count: int
