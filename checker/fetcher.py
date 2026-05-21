
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AccessibilityChecker/1.0; "
        "+https://github.com/accessibility-checker)"
    )
}

TIMEOUT = 15


def fetch_page(url: str) -> tuple[BeautifulSoup, str]:
    """Fetch url and return (soup, final_url). Raises on network/HTTP errors."""
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
    resp.raise_for_status()

    encoding = resp.encoding or "utf-8"
    soup = BeautifulSoup(resp.content, "lxml", from_encoding=encoding)
    return soup, resp.url
