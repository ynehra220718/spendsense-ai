"""
Price source router — auto-detects platform from product URL and routes to the right data source.

Supported platforms and their data sources:
  Amazon (amazon.com / amazon.in / etc.)  → CamelCamelCamel free API (requires free key)
                                             fallback: mock data
  Flipkart                                → mock data (no free public API exists)
  Any other URL / manual entry            → mock data

To enable live Amazon price history:
  1. Request a free CamelCamelCamel API key at https://camelcamelcamel.com/api
  2. Add to .env:  CAMELCAMELCAMEL_API_KEY=your-key-here
  Without a key the system silently falls back to mock data.
"""

import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

CCC_API_KEY = os.getenv("CAMELCAMELCAMEL_API_KEY", "")
MOCK_CATALOG_PATH = Path(__file__).parent.parent / "data" / "mock_product_catalog.json"


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

PLATFORM_PATTERNS = {
    "amazon": re.compile(
        r"amazon\.(com|in|co\.uk|de|fr|it|es|ca|com\.au|co\.jp|com\.br|nl|se|sg|ae|sa|pl|com\.mx)",
        re.IGNORECASE,
    ),
    "flipkart": re.compile(r"flipkart\.com", re.IGNORECASE),
    "myntra": re.compile(r"myntra\.com", re.IGNORECASE),
    "meesho": re.compile(r"meesho\.com", re.IGNORECASE),
    "snapdeal": re.compile(r"snapdeal\.com", re.IGNORECASE),
}

MOCK_ID_MAP = {
    "amazon": "dell-xps-15-laptop",       # demo fallback for Amazon URLs without CCC key
    "flipkart": "instant-pot-duo-7in1",   # demo fallback for Flipkart
    "myntra": "nike-air-max-270",
    "meesho": "nike-air-max-270",
    "snapdeal": "instant-pot-duo-7in1",
    "unknown": "instant-pot-duo-7in1",
}


def detect_platform(url: str) -> str:
    """Returns platform name ('amazon', 'flipkart', etc.) or 'unknown'."""
    for platform, pattern in PLATFORM_PATTERNS.items():
        if pattern.search(url):
            return platform
    return "unknown"


def extract_asin(url: str) -> str | None:
    """Extracts Amazon ASIN from a product URL."""
    match = re.search(r"/(?:dp|gp/product|product)/([A-Z0-9]{10})", url)
    return match.group(1) if match else None


def extract_flipkart_pid(url: str) -> str | None:
    """Extracts Flipkart product ID (pid) from a product URL."""
    match = re.search(r"pid=([A-Z0-9]+)", url)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def get_product_from_url(url: str) -> dict:
    """
    Auto-detects platform from URL, fetches product + price history
    from the best available zero-cost source for that platform.

    Returns a product dict in the standard catalog shape.
    """
    platform = detect_platform(url)

    if platform == "amazon":
        asin = extract_asin(url)
        if asin and CCC_API_KEY:
            try:
                product = _fetch_from_camelcamelcamel(asin)
                if product:
                    product["_source"] = "camelcamelcamel"
                    product["_platform"] = "amazon"
                    return product
            except Exception:
                pass  # fall through to mock
        # No ASIN, no key, or CCC failed → mock
        return _fetch_mock_for_platform(platform, url)

    elif platform == "flipkart":
        # No free Flipkart price history API exists — always mock
        return _fetch_mock_for_platform(platform, url)

    else:
        # Myntra, Meesho, Snapdeal, unknown → mock
        return _fetch_mock_for_platform(platform, url)


def get_product_by_id(product_id: str) -> dict | None:
    """Direct lookup by mock catalog ID (used in tests and demo scenarios)."""
    return _fetch_from_mock(product_id)


def get_all_mock_products() -> list[dict]:
    return _load_mock_catalog()


def get_platform_label(url: str) -> str:
    """Human-readable platform label for UI display."""
    labels = {
        "amazon": "Amazon",
        "flipkart": "Flipkart",
        "myntra": "Myntra",
        "meesho": "Meesho",
        "snapdeal": "Snapdeal",
        "unknown": "Unknown platform",
    }
    return labels.get(detect_platform(url), "Unknown platform")


# ---------------------------------------------------------------------------
# Mock source
# ---------------------------------------------------------------------------

def _load_mock_catalog() -> list[dict]:
    with open(MOCK_CATALOG_PATH) as f:
        return json.load(f)


def _fetch_from_mock(product_id: str) -> dict | None:
    for product in _load_mock_catalog():
        if product["id"] == product_id:
            return product
    return None


def _fetch_mock_for_platform(platform: str, url: str) -> dict:
    """Returns the most contextually relevant mock product for the platform."""
    mock_id = MOCK_ID_MAP.get(platform, MOCK_ID_MAP["unknown"])
    product = _fetch_from_mock(mock_id)
    product["_source"] = "mock"
    product["_platform"] = platform
    product["_original_url"] = url
    return product


# ---------------------------------------------------------------------------
# CamelCamelCamel source (Amazon only, free API key required)
# ---------------------------------------------------------------------------

def _fetch_from_camelcamelcamel(asin: str) -> dict | None:
    """
    Fetches Amazon price history for an ASIN from CamelCamelCamel's free API.
    Key request: https://camelcamelcamel.com/api
    """
    url = "https://api.camelcamelcamel.com/v1/products"
    params = {
        "apikey": CCC_API_KEY,
        "asin": asin,
        "history": 1,
        "offers": "amazon",
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("products"):
        return None

    raw = data["products"][0]

    price_history = [
        {"date": entry["date"], "price": entry["price"] / 100}
        for entry in raw.get("amazon", {}).get("prices", [])
        if entry.get("price")
    ]

    return {
        "id": asin,
        "name": raw.get("title", "Unknown Product"),
        "category": raw.get("category", "Unknown"),
        "brand": raw.get("manufacturer", "Unknown"),
        "current_price": raw.get("current_amazon_price", 0) / 100,
        "price_history": price_history,
    }
