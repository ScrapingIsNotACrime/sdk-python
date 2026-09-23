from typing import NotRequired, TypedDict


class BlueskyProfile(TypedDict):
    """GET /bluesky/profiles/{handle}"""

    did: str
    handle: str
    display_name: str
    # Null when the profile has no bio.
    description: NotRequired[str | None]
    # Null when the profile has no avatar set.
    avatar: NotRequired[str | None]
    # Banner image URL; null when the profile has none set.
    banner: NotRequired[str | None]
    followers: int
    following: int
    posts: int
    created_at: str
    url: str


class BlueskyPost(TypedDict):
    """One post in a profile's posts feed."""

    uri: str
    cid: str
    text: str
    author: str
    likes: int
    reposts: int
    replies: int
    quotes: int
    created_at: str
    indexed_at: str
    url: str


class BlueskyPostPage(TypedDict):
    """GET /bluesky/profiles/{handle}/posts"""

    posts: list[BlueskyPost]
    next_cursor: NotRequired[str | None]
    has_more: bool
