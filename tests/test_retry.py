from datetime import UTC, datetime
from email.utils import format_datetime

from scrapingisnotacrime._retry import MAX_RETRY_DELAY, retry_delay

NOW = datetime(2026, 9, 23, 10, 0, 0, tzinfo=UTC).timestamp()


def _date(seconds_from_now: float) -> str:
    return format_datetime(datetime.fromtimestamp(NOW + seconds_from_now, tz=UTC), usegmt=True)


def test_full_jitter_backoff() -> None:
    assert retry_delay(0, None, random=lambda: 0.5) == 0.25
    assert retry_delay(1, None, random=lambda: 0.5) == 0.5
    assert retry_delay(2, None, random=lambda: 0.999) < 2.0


def test_retry_after_seconds_and_date() -> None:
    assert retry_delay(0, "3", random=lambda: 0.0) == 3.0
    assert retry_delay(0, _date(4), random=lambda: 0.0, now=lambda: NOW) == 4.0


def test_caps_at_ten_seconds() -> None:
    assert MAX_RETRY_DELAY == 10.0
    assert retry_delay(0, "3600", random=lambda: 0.0) == 10.0
    assert retry_delay(0, _date(86400), random=lambda: 0.0, now=lambda: NOW) == 10.0
    assert retry_delay(12, None, random=lambda: 0.999) <= 10.0


def test_unparseable_or_past_retry_after() -> None:
    assert retry_delay(0, "soon", random=lambda: 0.5) == 0.25
    assert retry_delay(0, _date(-3600), random=lambda: 0.5, now=lambda: NOW) == 0.0
