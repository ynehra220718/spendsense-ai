import json
from pathlib import Path
from agents.base import client, DEFAULT_MODEL

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
DEAL_HUNTER_THRESHOLD = 60  # fires when financial health score is below this


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def run_deal_hunter_agent(
    user_profile: dict,
    product: dict,
    financial_result: dict,
    product_result: dict,
) -> dict:
    """
    Finds 3 alternatives (best price / wait / creative) when health score < 60.
    Returns a non-triggered stub if health score >= 60 — orchestrator skips display.
    """
    health_score = financial_result.get("health_score", 100)

    if health_score >= DEAL_HUNTER_THRESHOLD:
        return {
            "triggered": False,
            "trigger_reason": f"Health score {health_score} >= {DEAL_HUNTER_THRESHOLD} — user is in good shape for this purchase.",
            "alternatives": [],
            "deal_hunter_summary": "",
        }

    verdict = financial_result.get("verdict", "CAUTION")
    current_price = product.get("current_price", 0)
    sensible_low = product_result.get("sensible_lowest_price", current_price)
    price_gap = current_price - sensible_low

    user_message = f"""
Find 3 alternatives for a user who should not buy this product at its current price.

User Profile:
- Name: {user_profile.get("name")}
- Monthly Income: ${user_profile.get("monthly_income", 0):,.0f}
- Monthly Surplus: ${user_profile.get("monthly_income", 0) - user_profile.get("monthly_expenses", 0):,.0f}
- Total Debt: ${user_profile.get("total_debt", 0):,.0f}
- Financial Goals: {user_profile.get("financial_goals", [])}

Product: {product.get("name")}
Category: {product.get("category")}
Brand: {product.get("brand")}
Current Price: ${current_price:,.2f}
Sensible Historical Low: ${sensible_low:,.2f} (gap: ${price_gap:,.2f})
Price Assessment: {product_result.get("price_assessment")}
Market Context: {product_result.get("market_context")}

Financial Health Score: {health_score}/100 (threshold: {DEAL_HUNTER_THRESHOLD})
Verdict: {verdict}
Opportunity Cost: {financial_result.get("opportunity_cost")}

Generate exactly 3 alternatives in the order: best_price, wait, creative.
Return exactly the JSON schema specified. No markdown, no explanation.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": load_prompt("deal_hunter_prompt.md")},
            {"role": "user", "content": user_message},
        ],
    )
    return json.loads(response.choices[0].message.content)
