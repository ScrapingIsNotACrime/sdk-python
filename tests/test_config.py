import pytest

from scrapingisnotacrime._config import API_KEY_ENV, DEFAULT_BASE_URL, resolve_config


def test_defaults() -> None:
    config = resolve_config(api_key="sinac_x", env={})
    assert config.api_key == "sinac_x"
    assert config.base_url == DEFAULT_BASE_URL == "https://api.scrapingisnotacrime.com/v1"
    assert config.timeout == 30.0
    assert config.max_retries == 2


def test_reads_key_from_env_and_explicit_wins() -> None:
    assert API_KEY_ENV == "SCRAPINGISNOTACRIME_API_KEY"
    assert resolve_config(env={API_KEY_ENV: "sinac_env"}).api_key == "sinac_env"
    assert resolve_config(api_key="sinac_opt", env={API_KEY_ENV: "sinac_env"}).api_key == "sinac_opt"


@pytest.mark.parametrize("key", [None, "", "   "])
def test_missing_key_fails_fast(key: str | None) -> None:
    with pytest.raises(ValueError, match=r"api_key.*SCRAPINGISNOTACRIME_API_KEY"):
        resolve_config(api_key=key, env={})


def test_trailing_slash_in_base_url() -> None:
    assert resolve_config(api_key="k", base_url="https://x.test/v1/", env={}).base_url == "https://x.test/v1"


@pytest.mark.parametrize("timeout", [0, -1, float("inf"), float("nan"), True])
def test_invalid_timeout(timeout: float) -> None:
    with pytest.raises(ValueError, match="timeout"):
        resolve_config(api_key="k", timeout=timeout, env={})


@pytest.mark.parametrize("retries", [-1, 1.5, True])
def test_invalid_max_retries(retries: int) -> None:
    with pytest.raises(ValueError, match="max_retries"):
        resolve_config(api_key="k", max_retries=retries, env={})
