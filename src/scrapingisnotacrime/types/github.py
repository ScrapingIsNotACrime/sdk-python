from typing import Literal, NotRequired, TypedDict

GithubTrendingSince = Literal["daily", "weekly", "monthly"]


class GithubProfile(TypedDict):
    """GET /github/profiles/{handle}"""

    username: str
    id: int
    # Null when the user has not set a display name.
    name: NotRequired[str | None]
    # Null when the user has not set a bio.
    bio: NotRequired[str | None]
    company: NotRequired[str | None]
    location: NotRequired[str | None]
    # Website URL; empty or null when the user has not set one.
    blog: NotRequired[str | None]
    public_repos: int
    followers: int
    following: int
    avatar: str
    created_at: str
    url: str


class GithubUser(TypedDict):
    """A user in a followers/following page."""

    username: str
    id: int
    avatar: str
    url: str


class GithubUserPage(TypedDict):
    """GET /github/profiles/{handle}/followers and /following"""

    items: list[GithubUser]
    # Always null: GitHub's REST API does not report a count for this collection.
    total: NotRequired[int | None]
    has_more: bool


class GithubRepository(TypedDict):
    """A repository, as returned by the profile repositories list, search, and trending endpoints."""

    name: str
    full_name: str
    # Null when the repository has no description.
    description: NotRequired[str | None]
    stars: int
    forks: int
    # Primary language; null when GitHub has not detected one.
    language: NotRequired[str | None]
    topics: list[str]
    is_fork: bool
    is_archived: bool
    created_at: str
    updated_at: str
    url: str


class GithubRepositoryPage(TypedDict):
    """GET /github/profiles/{handle}/repositories"""

    items: list[GithubRepository]
    # Always null: GitHub's REST API does not report a count for this collection.
    total: NotRequired[int | None]
    has_more: bool


class GithubRepositorySearchPage(TypedDict):
    """GET /github/repositories"""

    items: list[GithubRepository]
    total: int
    page: int
    has_more: bool


class GithubTrending(TypedDict):
    """GET /github/trending/repositories"""

    items: list[GithubRepository]
    total: int
    page: int
    has_more: bool
