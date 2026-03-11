"""
Tests for price_source.py — platform detection, ID extraction, and mock data routing.
These tests require no API keys and run entirely offline.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.price_source import (
    detect_platform,
    extract_asin,
    extract_flipkart_pid,
    get_platform_label,
    get_product_by_id,
    get_all_mock_products,
)


# ── Platform detection ──────────────────────────────────────────────────────

class TestDetectPlatform:
    def test_amazon_com(self):
        assert detect_platform("https://www.amazon.com/dp/B00FLYWNYQ") == "amazon"

    def test_amazon_in(self):
        assert detect_platform("https://www.amazon.in/dp/B09G9FPHY6") == "amazon"

    def test_amazon_co_uk(self):
        assert detect_platform("https://www.amazon.co.uk/dp/B00FLYWNYQ") == "amazon"

    def test_amazon_de(self):
        assert detect_platform("https://www.amazon.de/dp/B00FLYWNYQ") == "amazon"

    def test_flipkart(self):
        assert detect_platform("https://www.flipkart.com/apple-iphone-15/p/itm123?pid=MOBGTAGPAQNVFZZY") == "flipkart"

    def test_myntra(self):
        assert detect_platform("https://www.myntra.com/shoes/nike/nike-air-max/12345678/buy") == "myntra"

    def test_meesho(self):
        assert detect_platform("https://meesho.com/product/xyz/p/123") == "meesho"

    def test_snapdeal(self):
        assert detect_platform("https://www.snapdeal.com/product/some-item/123456") == "snapdeal"

    def test_unknown_url(self):
        assert detect_platform("https://www.walmart.com/ip/some-product/123") == "unknown"

    def test_empty_string(self):
        assert detect_platform("") == "unknown"

    def test_plain_text_no_url(self):
        assert detect_platform("Instant Pot 6Qt") == "unknown"


# ── ASIN extraction ─────────────────────────────────────────────────────────

class TestExtractAsin:
    def test_dp_url(self):
        assert extract_asin("https://www.amazon.com/dp/B00FLYWNYQ") == "B00FLYWNYQ"

    def test_dp_url_with_path_after(self):
        assert extract_asin("https://www.amazon.com/Instant-Pot-Duo/dp/B00FLYWNYQ/ref=sr_1_1") == "B00FLYWNYQ"

    def test_gp_product_url(self):
        assert extract_asin("https://www.amazon.com/gp/product/B09G9FPHY6") == "B09G9FPHY6"

    def test_amazon_in_url(self):
        assert extract_asin("https://www.amazon.in/dp/B09G9FPHY6?th=1") == "B09G9FPHY6"

    def test_no_asin_returns_none(self):
        assert extract_asin("https://www.amazon.com/s?k=instant+pot") is None

    def test_flipkart_url_returns_none(self):
        assert extract_asin("https://www.flipkart.com/product/p/itm123") is None


# ── Flipkart PID extraction ─────────────────────────────────────────────────

class TestExtractFlipkartPid:
    def test_pid_in_query(self):
        assert extract_flipkart_pid(
            "https://www.flipkart.com/apple-iphone-15/p/itm?pid=MOBGTAGPAQNVFZZY"
        ) == "MOBGTAGPAQNVFZZY"

    def test_no_pid_returns_none(self):
        assert extract_flipkart_pid("https://www.flipkart.com/search?q=iphone") is None


# ── Platform label ──────────────────────────────────────────────────────────

class TestGetPlatformLabel:
    def test_amazon_label(self):
        assert get_platform_label("https://www.amazon.com/dp/B00FLYWNYQ") == "Amazon"

    def test_flipkart_label(self):
        assert get_platform_label("https://www.flipkart.com/product") == "Flipkart"

    def test_unknown_label(self):
        assert get_platform_label("https://www.walmart.com/item") == "Unknown platform"


# ── Mock catalog ────────────────────────────────────────────────────────────

class TestMockCatalog:
    def test_all_products_loads(self):
        products = get_all_mock_products()
        assert isinstance(products, list)
        assert len(products) == 3

    def test_all_products_have_price_history(self):
        for p in get_all_mock_products():
            assert "price_history" in p
            assert len(p["price_history"]) > 0

    def test_price_history_entries_have_date_and_price(self):
        for p in get_all_mock_products():
            for entry in p["price_history"]:
                assert "date" in entry
                assert "price" in entry
                assert isinstance(entry["price"], (int, float))

    def test_get_product_by_id_instant_pot(self):
        product = get_product_by_id("instant-pot-duo-7in1")
        assert product is not None
        assert product["name"] == "Instant Pot Duo 7-in-1 (6 Qt)"
        assert product["current_price"] == 279.99

    def test_get_product_by_id_laptop(self):
        product = get_product_by_id("dell-xps-15-laptop")
        assert product is not None
        assert "Dell" in product["name"]

    def test_get_product_by_id_sneakers(self):
        product = get_product_by_id("nike-air-max-270")
        assert product is not None
        assert "Nike" in product["name"]

    def test_get_product_by_id_not_found(self):
        product = get_product_by_id("nonexistent-product")
        assert product is None


# ── Price history anomaly validation (data integrity) ──────────────────────

class TestPriceHistoryDataIntegrity:
    """
    Validates that the mock catalog contains the expected anomalies
    that the Product Intelligence Agent should filter out.
    """
    def test_instant_pot_has_anomalous_price(self):
        product = get_product_by_id("instant-pot-duo-7in1")
        prices = [e["price"] for e in product["price_history"]]
        # $79.99 anomaly should be present in raw data
        assert 79.99 in prices

    def test_laptop_has_anomalous_price(self):
        product = get_product_by_id("dell-xps-15-laptop")
        prices = [e["price"] for e in product["price_history"]]
        # $399.99 anomaly should be present in raw data
        assert 399.99 in prices

    def test_sneakers_have_no_anomaly(self):
        product = get_product_by_id("nike-air-max-270")
        prices = [e["price"] for e in product["price_history"]]
        median = sorted(prices)[len(prices) // 2]
        # No price should be more than 40% below median
        for p in prices:
            assert p >= median * 0.60, f"Anomalous price {p} found in sneakers history"
