from typing import Any, NotRequired, TypedDict


class InstagramProfile(TypedDict):
    """GET /instagram/profile/{username}"""

    id: str
    fbid: str
    username: str
    full_name: str
    bio: str
    bio_links: list[str]
    followers: int
    following: int
    medias: int
    highlight_reel_count: int
    profile_pic: str
    has_ar_effects: bool
    has_clips: bool
    has_guides: bool
    has_channel: bool
    has_blocked_viewer: bool
    is_business_account: bool
    # Null in every observed example; no evidence of its populated shape.
    business_address_json: NotRequired[Any | None]
    business_contact_method: str
    business_email: NotRequired[str | None]
    business_phone_number: NotRequired[str | None]
    business_category_name: str
    is_professional_account: bool
    category_name: str
    is_private: bool
    is_verified: bool


class InstagramContactAddress(TypedDict):
    """A profile's structured business address, from the contact endpoint."""

    street_address: str
    zip_code: str
    city_name: str
    region_name: str
    country_code: str


class InstagramFoundContact(TypedDict):
    """An email address or phone number found written into a profile's bio."""

    value: str
    source: str


class InstagramContact(TypedDict):
    """GET /instagram/profile/{username}/contact"""

    username: str
    full_name: str
    biography: str
    is_verified: bool
    is_business: bool
    category: str
    email: NotRequired[str | None]
    phone: NotRequired[str | None]
    external_url: str
    # Null for a profile with no contact info (per the endpoint's docs, all fields are null then).
    address: NotRequired[InstagramContactAddress | None]
    emails_found: list[InstagramFoundContact]
    phones_found: list[InstagramFoundContact]


class InstagramClipsMusicAttribution(TypedDict):
    """Music attribution for a video/reel; null for original audio."""

    artist_name: str
    song_name: str
    uses_original_audio: bool


class InstagramLatestPostImage(TypedDict):
    """An image post in a profile's latest-posts timeline."""

    id: str
    shortcode: str
    type: str
    comments: int
    likes: int
    # Null when the post has no caption.
    caption: NotRequired[str | None]
    location: NotRequired[Any | None]
    thumbnail_resources: NotRequired[Any | None]
    display_url: str
    taken_at_timestamp: str


class InstagramLatestPostVideo(TypedDict):
    """A video post in a profile's latest-posts timeline — carries extra fields
    (video_views, video_url, has_audio, clips_music_attribution_info) the image posts lack."""

    id: str
    shortcode: str
    type: str
    video_views: int
    comments: int
    likes: int
    # Null when the post has no caption.
    caption: NotRequired[str | None]
    location: NotRequired[Any | None]
    thumbnail_resources: NotRequired[Any | None]
    display_url: str
    video_url: str
    has_audio: bool
    clips_music_attribution_info: NotRequired[InstagramClipsMusicAttribution | None]
    taken_at_timestamp: str


# A post in a profile's latest-posts timeline — an image post or a video post; `type` tells them apart.
InstagramLatestPostMedia = InstagramLatestPostImage | InstagramLatestPostVideo


class InstagramLatestPosts(TypedDict):
    """GET /instagram/profile/{username}/timeline/latest"""

    count: int
    latest_count: int
    medias: list[InstagramLatestPostMedia]


class InstagramMedia(TypedDict):
    """A post, as returned by the paged timeline and the highlight-content endpoints."""

    id: str
    shortcode: str
    type: str
    # Null when the post has no caption.
    caption: NotRequired[str | None]
    likes: int
    comments: int
    preview_comments: list[Any]
    location: NotRequired[Any | None]
    display_url: str
    taken_at_timestamp: str


class InstagramTimelinePage(TypedDict):
    """GET /instagram/profile/{username}/timeline"""

    medias: list[InstagramMedia]
    has_more: bool
    next_cursor: NotRequired[str | None]


class InstagramHighlightSummary(TypedDict):
    """A highlight reel's summary, as listed on a profile."""

    id: str
    title: str
    cover: str


class InstagramHighlights(TypedDict):
    """GET /instagram/profile/{username}/highlights"""

    username: str
    user_id: str
    highlights: list[InstagramHighlightSummary]


class InstagramHighlight(TypedDict):
    """GET /instagram/highlights/{highlightId}"""

    id: str
    title: str
    items: list[InstagramMedia]


class InstagramMediaDetail(TypedDict):
    """GET /instagram/profile/{username}/media/{mediaId} — the same media object the timeline
    endpoints return, including the video-only fields when the media is a video."""

    id: str
    shortcode: str
    type: str
    comments: int
    likes: int
    # Null when the post has no caption.
    caption: NotRequired[str | None]
    location: NotRequired[Any | None]
    thumbnail_resources: NotRequired[Any | None]
    display_url: str
    taken_at_timestamp: str
    video_views: NotRequired[int]
    video_url: NotRequired[str]
    has_audio: NotRequired[bool]
    clips_music_attribution_info: NotRequired[InstagramClipsMusicAttribution | None]


class InstagramDownloadAsset(TypedDict):
    """One downloadable asset behind a post, reel, or carousel."""

    kind: str
    index: int
    url: str
    width: int
    height: int
    # Null for non-video assets (e.g. thumbnails).
    quality: NotRequired[str | None]
    expires_at: str


class InstagramDownload(TypedDict):
    """GET /instagram/media/{shortcode}/download — assets[0] is always the best primary asset."""

    shortcode: str
    type: str
    expires_at: str
    assets: list[InstagramDownloadAsset]


class InstagramShortcodeId(TypedDict):
    """GET /instagram/media/{shortcode}/id and /instagram/media/id/{mediaId}"""

    shortcode: str
    media_id: str


class InstagramReel(TypedDict):
    """GET /instagram/reels/{shortcode} — clips_music_attribution_info is null for original audio."""

    id: str
    shortcode: str
    type: str
    video_views: int
    comments: int
    likes: int
    # Null when the post has no caption.
    caption: NotRequired[str | None]
    location: NotRequired[Any | None]
    thumbnail_resources: NotRequired[Any | None]
    display_url: str
    video_url: str
    has_audio: bool
    clips_music_attribution_info: NotRequired[InstagramClipsMusicAttribution | None]
    taken_at_timestamp: str
