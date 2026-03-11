import json
from pathlib import Path
from agents.base import client, DEFAULT_MODEL

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text()


def run_behavioral_coach_agent(
    user_profile: dict,
    product: dict,
    financial_result: dict,
    product_result: dict,
) -> dict:
    """
    Generates a persona-tailored coaching message using:
    - User's financial profile and persona type
    - Financial health agent output (score, verdict, opportunity cost)
    - Product intelligence output (price assessment, sensible lowest price)
    """
    verdict = financial_result.get("verdict", "CAUTION")
    health_score = financial_result.get("health_score", 50)
    persona_type = user_profile.get("persona_type", "budget_guilt")
    price_assessment = product_result.get("price_assessment", "FAIR_PRICE")
    sensible_low = product_result.get("sensible_lowest_price")
    current_price = product.get("current_price")

    price_context = ""
    if sensible_low and current_price:
        diff_pct = ((current_price - sensible_low) / sensible_low) * 100
        if diff_pct > 10:
            price_context = (
                f"The current price (${current_price}) is {diff_pct:.0f}% above the "
                f"sensible historical low (${sensible_low} on {product_result.get('sensible_lowest_date', 'a prior date')}). "
                f"This context may be relevant to coaching."
            )
        else:
            price_context = (
                f"The current price (${current_price}) is near the historical low of ${sensible_low}. "
                f"This is useful affirmation if the verdict is RECOMMENDED."
            )

    user_message = f"""
Generate a behavioral coaching message for this user and purchase situation.

User Profile:
- Name: {user_profile.get("name")}
- Persona Type: {persona_type}
- Monthly Income: ${user_profile.get("monthly_income", 0):,.0f}
- Monthly Surplus: ${user_profile.get("monthly_income", 0) - user_profile.get("monthly_expenses", 0):,.0f}
- Total Debt: ${user_profile.get("total_debt", 0):,.0f}
- Financial Goals: {user_profile.get("financial_goals", [])}
- Known Money Behavior: {user_profile.get("money_behavior", "not specified")}

Product: {product.get("name")} at ${current_price}
Category: {product.get("category")}

Financial Health Agent Output:
- Health Score: {health_score}/100
- Verdict: {verdict}
- Opportunity Cost: {financial_result.get("opportunity_cost")}
- Timing Recommendation: {financial_result.get("timing_recommendation")}
- Rationale: {financial_result.get("rationale")}

Product Intelligence Output:
- Price Assessment: {price_assessment}
- Value Score: {product_result.get("value_score")}/100
- Market Context: {product_result.get("market_context")}
- Red Flags: {product_result.get("red_flags", [])}
- {price_context}

Apply the psychological frameworks from your instructions.
Return exactly the JSON schema specified. No markdown, no explanation.
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": load_prompt("behavioral_coach_prompt.md")},
            {"role": "user", "content": user_message},
        ],
    )
    return json.loads(response.choices[0].message.content)
