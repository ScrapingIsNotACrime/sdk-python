import json
from pathlib import Path

import scrapingisnotacrime

FIXTURES = Path(__file__).parent / "fixtures"


def test_version_is_exposed() -> None:
    assert isinstance(scrapingisnotacrime.__version__, str)
    assert scrapingisnotacrime.__version__


def test_fixtures_are_documented_envelopes() -> None:
    files = sorted(FIXTURES.glob("*.json"))
    assert len(files) == 30
    for file in files:
        fixture = json.loads(file.read_text())
        assert fixture["request"].startswith("/")
        assert isinstance(fixture["response"]["message"], str)
        assert "data" in fixture["response"]
        assert "hob_" not in file.read_text()
