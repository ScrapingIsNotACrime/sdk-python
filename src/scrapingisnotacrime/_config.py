from __future__ import annotations

import math
import os
from collections.abc import Mapping
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://api.scrapingisnotacrime.com/v1"
API_KEY_ENV = "SCRAPINGISNOTACRIME_API_KEY"


@dataclass(frozen=True)
class Config:
    api_key: str
    base_url: str
    timeout: float
    max_retries: int


def resolve_config(
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 30.0,
    max_retries: int = 2,
    env: Mapping[str, str] | None = None,
) -> Config:
    source = os.environ if env is None else env
    key = (api_key if api_key is not None else source.get(API_KEY_ENV, "")).strip()
    if not key:
        raise ValueError(f"Missing API key: pass api_key=... or set the {API_KEY_ENV} environment variable.")
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, int | float)
        or not math.isfinite(timeout)
        or timeout <= 0
    ):
        raise ValueError("timeout must be a positive, finite number of seconds.")
    if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer.")
    return Config(
        api_key=key,
        base_url=(base_url or DEFAULT_BASE_URL).rstrip("/"),
        timeout=float(timeout),
        max_retries=max_retries,
    )
