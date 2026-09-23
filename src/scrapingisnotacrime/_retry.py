from __future__ import annotations

import random as _random
import re
import time
from collections.abc import Callable
from email.utils import parsedate_to_datetime

MAX_RETRY_DELAY = 10.0
_BASE_DELAY = 0.5


def _parse_retry_after(value: str | None, now: Callable[[], float]) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if re.fullmatch(r"\d+(\.\d+)?", text):
        return float(text)
    try:
        moment = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    return max(0.0, moment.timestamp() - now())


def retry_delay(
    attempt: int,
    retry_after: str | None,
    random: Callable[[], float] = _random.random,
    now: Callable[[], float] = time.time,
) -> float:
    """Seconds to wait before retry number `attempt` (0 for the first retry)."""
    from_header = _parse_retry_after(retry_after, now)
    delay = from_header if from_header is not None else random() * _BASE_DELAY * 2**attempt
    return min(delay, MAX_RETRY_DELAY)
