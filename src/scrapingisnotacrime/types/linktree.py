from typing import TypedDict


class LinktreeLink(TypedDict):
    """One link in a Linktree profile."""

    id: str
    title: str
    url: str
    type: str


class LinktreeProfile(TypedDict):
    """GET /linktree/profiles/{handle}"""

    username: str
    title: str
    description: str
    avatar: str
    is_verified: bool
    url: str
    links: list[LinktreeLink]
