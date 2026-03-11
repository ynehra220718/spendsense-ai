"""
Tests for user_tools.py — profile loading and validation.
Runs entirely offline, no API keys required.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.user_tools import load_user_profile, list_user_profiles


class TestListUserProfiles:
    def test_returns_list(self):
        profiles = list_user_profiles()
        assert isinstance(profiles, list)

    def test_contains_all_three_personas(self):
        profiles = list_user_profiles()
        assert "priya" in profiles
        assert "marcus" in profiles
        assert "destiny" in profiles


class TestLoadUserProfile:
    def test_priya_loads(self):
        p = load_user_profile("priya")
        assert p is not None
        assert p["name"] == "Priya"

    def test_marcus_loads(self):
        p = load_user_profile("marcus")
        assert p is not None
        assert p["name"] == "Marcus"

    def test_destiny_loads(self):
        p = load_user_profile("destiny")
        assert p is not None
        assert p["name"] == "Destiny"

    def test_nonexistent_returns_none(self):
        assert load_user_profile("nobody") is None

    def test_all_profiles_have_required_fields(self):
        required = ["monthly_income", "monthly_expenses", "savings", "total_debt",
                    "financial_goals", "persona_type", "behavioral_profile"]
        for pid in ["priya", "marcus", "destiny"]:
            profile = load_user_profile(pid)
            for field in required:
                assert field in profile, f"'{field}' missing from {pid} profile"

    def test_monthly_surplus_is_positive_for_all(self):
        """All personas should have positive monthly surplus — they're spending less than they earn."""
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            surplus = p["monthly_income"] - p["monthly_expenses"]
            assert surplus > 0, f"{pid} has negative surplus — check profile data"

    def test_savings_is_non_negative(self):
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            assert p["savings"] >= 0

    def test_total_debt_is_non_negative(self):
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            assert p["total_debt"] >= 0

    def test_persona_types_are_valid(self):
        valid_types = {"budget_guilt", "comparison_shopper", "rebuilding_finances"}
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            assert p["persona_type"] in valid_types

    def test_financial_goals_is_non_empty_list(self):
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            assert isinstance(p["financial_goals"], list)
            assert len(p["financial_goals"]) > 0

    def test_behavioral_profile_has_money_script(self):
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            bp = p.get("behavioral_profile", {})
            assert "money_script" in bp
            assert len(bp["money_script"]) > 10  # not empty

    def test_income_is_realistic(self):
        """Sanity check: monthly income should be between $2K and $20K for our personas."""
        for pid in ["priya", "marcus", "destiny"]:
            p = load_user_profile(pid)
            assert 2000 <= p["monthly_income"] <= 20000

    def test_priya_has_highest_income(self):
        priya = load_user_profile("priya")
        marcus = load_user_profile("marcus")
        destiny = load_user_profile("destiny")
        assert priya["monthly_income"] > marcus["monthly_income"] > destiny["monthly_income"]

    def test_destiny_has_lowest_savings(self):
        priya = load_user_profile("priya")
        marcus = load_user_profile("marcus")
        destiny = load_user_profile("destiny")
        assert destiny["savings"] < priya["savings"]
        assert destiny["savings"] < marcus["savings"]
