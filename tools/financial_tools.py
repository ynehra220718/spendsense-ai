"""
Financial calculation helpers used by the Financial Health Agent.
Pure functions — no API calls, no side effects.
"""


def compute_monthly_surplus(profile: dict) -> float:
    return profile.get("monthly_income", 0) - profile.get("monthly_expenses", 0)


def compute_debt_to_income_ratio(profile: dict) -> float:
    """Annual DTI: total debt / annual gross income."""
    annual_income = profile.get("income", {}).get("annual_gross", 0)
    if not annual_income:
        return 0.0
    return profile.get("total_debt", 0) / annual_income


def compute_purchase_as_pct_of_income(purchase_amount: float, monthly_income: float) -> float:
    if not monthly_income:
        return 100.0
    return (purchase_amount / monthly_income) * 100


def compute_savings_buffer_months(profile: dict) -> float:
    """How many months of expenses the user's savings covers."""
    monthly_expenses = profile.get("monthly_expenses", 0)
    if not monthly_expenses:
        return 0.0
    return profile.get("savings", 0) / monthly_expenses


def compute_financial_summary(profile: dict, purchase_amount: float) -> dict:
    """
    Returns a structured financial summary dict passed to the Financial Health Agent
    as supplementary context (in addition to the raw profile).
    """
    monthly_income = profile.get("monthly_income", 0)
    surplus = compute_monthly_surplus(profile)
    dti = compute_debt_to_income_ratio(profile)
    purchase_pct = compute_purchase_as_pct_of_income(purchase_amount, monthly_income)
    buffer_months = compute_savings_buffer_months(profile)
    purchase_vs_surplus = (purchase_amount / surplus * 100) if surplus > 0 else 100

    return {
        "monthly_surplus": round(surplus, 2),
        "debt_to_income_ratio": round(dti, 3),
        "purchase_as_pct_of_monthly_income": round(purchase_pct, 1),
        "purchase_as_pct_of_monthly_surplus": round(purchase_vs_surplus, 1),
        "savings_buffer_months": round(buffer_months, 1),
        "has_bnpl_exposure": _detect_bnpl_exposure(profile),
        "hidden_debt_flag": _flag_hidden_debt(profile),
    }


def _detect_bnpl_exposure(profile: dict) -> bool:
    debt = profile.get("debt_breakdown", {})
    bnpl = debt.get("bnpl_outstanding", 0)
    return isinstance(bnpl, (int, float)) and bnpl > 0


def _flag_hidden_debt(profile: dict) -> bool:
    """
    Flags profiles where BNPL outstanding > 10% of monthly income —
    a meaningful off-balance-sheet obligation the agent should factor in.
    """
    debt = profile.get("debt_breakdown", {})
    bnpl = debt.get("bnpl_outstanding", 0)
    monthly_income = profile.get("monthly_income", 1)
    return (bnpl / monthly_income) > 0.10
