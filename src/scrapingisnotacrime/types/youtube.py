from typing import TypedDict


class YoutubeChannel(TypedDict):
    """The channel block in a channel-videos response."""

    title: str
    description: str
    externalId: str
    avatar: str


class YoutubeVideo(TypedDict):
    """One video in a channel's video list."""

    id: str
    title: str
    url: str
    thumbnail: str
    metadataText: list[str]


class YoutubeChannelVideos(TypedDict):
    """GET /youtube/channel/{handle}/videos"""

    channel: YoutubeChannel
    videos: list[YoutubeVideo]
