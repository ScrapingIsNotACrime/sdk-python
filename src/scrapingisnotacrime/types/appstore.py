from typing import TypedDict


class AppstoreApp(TypedDict):
    """One app in an App Store search result."""

    id: int
    bundleId: str
    name: str
    developer: str
    url: str
    iconUrl: str
    price: float
    currency: str
    rating: float
    ratingCount: int
    version: str
    genres: list[str]
    screenshots: list[str]


class AppstoreSearch(TypedDict):
    """GET /appstore/search"""

    term: str
    country: str
    resultCount: int
    apps: list[AppstoreApp]


class AppstoreReview(TypedDict):
    """One customer review of an app."""

    id: str
    author: str
    rating: float
    title: str
    content: str
    version: str
    updatedAt: str
    voteCount: int
    voteSum: int


class AppstoreReviewPage(TypedDict):
    """GET /appstore/reviews"""

    appId: str
    country: str
    page: int
    reviews: list[AppstoreReview]
