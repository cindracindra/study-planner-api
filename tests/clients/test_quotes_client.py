from unittest.mock import patch
import pytest

from app.clients.quotes_client import get_random_quote, get_random_excuse
from app.constants.static_quotes import FALLBACK_QUOTES, FALLBACK_EXCUSES


def test_get_random_quote_uses_external_api():
    with patch("app.clients.quotes_client.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"q": "Test quote"}]

        result = get_random_quote()

        mock_get.assert_called_once_with("https://zenquotes.io/api/random", timeout=5.0)
        assert result == "Test quote"


def test_get_random_quote_falls_back_when_api_fails():
    with patch("requests.get", side_effect=Exception("API down")):
        result = get_random_quote()
        assert result in FALLBACK_QUOTES 


def test_get_random_excuse_returns_from_fallback_list():
    result = get_random_excuse()
    assert result in FALLBACK_EXCUSES


@pytest.mark.integration
def test_get_random_quote_real_api():
    result = get_random_quote()
    assert isinstance(result, str)
    assert len(result) > 0
    assert result not in FALLBACK_QUOTES
    print(f"Got quote from API: {result}")
