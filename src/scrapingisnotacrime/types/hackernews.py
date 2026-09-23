from typing import NotRequired, TypedDict


class HackernewsStory(TypedDict):
    """A story, as returned by feeds, search, and a user's submissions."""

    id: int
    title: str
    author: str
    points: int
    num_comments: int
    # External link; null for self-posts (Ask HN, etc.).
    url: NotRequired[str | None]
    # Self-post body as HTML; null for link posts.
    text: NotRequired[str | None]
    created_at: str
    hn_url: str


class HackernewsStoryPage(TypedDict):
    """GET /hackernews/feeds/{feed}, /hackernews/search, and /hackernews/users/{username}/submissions"""

    items: list[HackernewsStory]
    total: int
    page: int
    has_more: bool


class HackernewsComment(TypedDict):
    """A comment inside an item's comment tree; replies nest recursively."""

    id: int
    author: str
    text: str
    created_at: str
    replies: list["HackernewsComment"]


class HackernewsItem(TypedDict):
    """GET /hackernews/items/{id}"""

    id: int
    type: str
    # Null for comments and other untitled item types.
    title: NotRequired[str | None]
    author: str
    points: NotRequired[int | None]
    # External link; null for self-posts.
    url: NotRequired[str | None]
    # Self-post body as HTML; null for link posts.
    text: NotRequired[str | None]
    created_at: str
    hn_url: str
    comments: list[HackernewsComment]


class HackernewsUser(TypedDict):
    """GET /hackernews/users/{username}"""

    username: str
    karma: int
    # Profile bio as HTML; null when the user has not written one.
    about: NotRequired[str | None]
    created_at: str
    submission_count: int
    hn_url: str


class HackernewsUserComment(TypedDict):
    """A comment in a user's comment listing; unlike item-tree nodes, `replies` may be absent."""

    id: int
    author: str
    text: str
    created_at: str
    replies: NotRequired[list[HackernewsComment]]


class HackernewsUserCommentPage(TypedDict):
    """GET /hackernews/users/{username}/comments — same page envelope as the other listings."""

    items: list[HackernewsUserComment]
    total: int
    page: int
    has_more: bool
