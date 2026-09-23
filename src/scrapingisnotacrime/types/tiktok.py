from typing import TypedDict


class TiktokProfile(TypedDict):
    """GET /tiktok/profile/{username}"""

    id: str
    username: str
    nickname: str
    bio: str
    bio_link: str
    avatar: str
    sec_uid: str
    followers: int
    following: int
    hearts: int
    videos: int
    is_private: bool
    is_verified: bool


class TiktokVideo(TypedDict, total=False):
    """GET /tiktok/video/{videoId} — no documented example yet; refined from the smoke test."""

    id: str
    # Index signature ([key: string]: unknown) — any other key is accepted at runtime.
