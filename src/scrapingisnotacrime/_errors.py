from __future__ import annotations

import builtins

PRICING_URL = "https://scrapingisnotacrime.com/#pricing"


class ScrapingIsNotACrimeError(Exception):
    """Base class of every error raised by the SDK."""

    def __init__(self, message: str, *, status: int | None = None, request_id: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.request_id = request_id


class BadRequestError(ScrapingIsNotACrimeError):
    """400 — invalid parameter."""


class AuthenticationError(ScrapingIsNotACrimeError):
    """401 — missing or invalid API key."""


class QuotaExceededError(ScrapingIsNotACrimeError):
    """402 — the plan's credits are used up."""


class NotFoundError(ScrapingIsNotACrimeError):
    """404 — profile, post or item does not exist."""


class RateLimitError(ScrapingIsNotACrimeError):
    """429 — the source platform rate-limited the request (retried; not charged)."""


class UpstreamError(ScrapingIsNotACrimeError):
    """502 — the source platform failed (retried; not charged)."""


class ConnectionError(ScrapingIsNotACrimeError):
    """Network failure or timeout (retried). Not the builtin ConnectionError."""


class APIError(ScrapingIsNotACrimeError):
    """Any other non-2xx response, or a 2xx response without the JSON envelope."""


_BY_STATUS: dict[int, type[ScrapingIsNotACrimeError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    402: QuotaExceededError,
    404: NotFoundError,
    429: RateLimitError,
    502: UpstreamError,
}


def error_from_status(status: int, message: str, request_id: str | None = None) -> ScrapingIsNotACrimeError:
    cls = _BY_STATUS.get(status, APIError)
    if cls is QuotaExceededError:
        message = f"{message} — see {PRICING_URL}"
    return cls(message, status=status, request_id=request_id)


def is_retryable(error: builtins.BaseException) -> bool:
    # 429 and 502 don't consume credits, so retrying them costs the customer nothing.
    return isinstance(error, RateLimitError | UpstreamError | ConnectionError)
