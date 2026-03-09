import requests
import random

from app.constants.static_quotes import FALLBACK_EXCUSES, FALLBACK_QUOTES


def get_random_quote() -> str:
    """Fetch quote from external API, fall back to static list."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5.0)

        if response.status_code == 200:
            data = response.json()
            return data[0]["q"]
    except Exception:
        pass

    return random.choice(FALLBACK_QUOTES)


def get_random_excuse() -> str:
    """Return a random excuse from static list."""
    return random.choice(FALLBACK_EXCUSES)
