import requests
import random

from app.constants.static_quotes import FALLBACK_EXCUSES, FALLBACK_QUOTES


def get_random_quote() -> dict:
    """Fetch quote from external API, fall back to static list."""
    try:
        response = requests.get("https://api.quotable.io/random", timeout=2.0)
        if response.status_code == 200:
            data = response.json()
            return {"text": data["content"]}
    except Exception:
        pass

    return random.choice(FALLBACK_QUOTES)


def get_random_excuse() -> str:
    """Return a random excuse from static list."""
    return random.choice(FALLBACK_EXCUSES)
