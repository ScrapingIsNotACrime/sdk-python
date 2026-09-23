import pytest

from scrapingisnotacrime._errors import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ScrapingIsNotACrimeError,
    UpstreamError,
    error_from_status,
    is_retryable,
)


@pytest.mark.parametrize(
    ("status", "cls"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (402, QuotaExceededError),
        (404, NotFoundError),
        (429, RateLimitError),
        (502, UpstreamError),
        (500, APIError),
        (418, APIError),
    ],
)
def test_error_from_status(status: int, cls: type[ScrapingIsNotACrimeError]) -> None:
    error = error_from_status(status, "boom", "req-1")
    assert type(error) is cls
    assert isinstance(error, ScrapingIsNotACrimeError)
    assert error.status == status
    assert error.request_id == "req-1"


def test_messages() -> None:
    assert error_from_status(404, "Profile not found.").message == "Profile not found."
    assert str(error_from_status(404, "Profile not found.")) == "Profile not found."
    assert (
        error_from_status(402, "plan.quota_exceeded").message
        == "plan.quota_exceeded — see https://scrapingisnotacrime.com/#pricing"
    )


def test_is_retryable() -> None:
    assert is_retryable(RateLimitError("x", status=429))
    assert is_retryable(UpstreamError("x", status=502))
    assert is_retryable(ConnectionError("x"))
    for status in (400, 401, 402, 404, 500):
        assert not is_retryable(error_from_status(status, "x"))
    assert not is_retryable(ValueError("x"))


def test_connection_error_has_no_status() -> None:
    assert ConnectionError("down").status is None
